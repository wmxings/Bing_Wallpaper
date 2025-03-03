import os
import logging
from typing import List
from src.models.wallpaper import WallpaperImage
from src.utils.date_utils import group_by_month
from src.utils.file_utils import write_json, write_text, list_files
from src.utils.exceptions import FileOperationError
from src.utils.decorators import retry
from src.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class FileGenerator:
    def __init__(self, country_code: str):
        self.country_code = country_code
        self.config = ConfigManager()
        
    def _get_json_path(self, year: int, month: int) -> str:
        """获取JSON文件路径"""
        return os.path.join(
            self.config.get("paths.archives_dir"),
            self.country_code,
            self.config.get("paths.json_dir"),
            self.config.get("templates.json_file").format(year=year, month=month)
        )
    
    def _get_wallpaper_path(self, year: int, month: int) -> str:
        """获取壁纸文件路径"""
        return os.path.join(
            self.config.get("paths.archives_dir"),
            self.country_code,
            self.config.get("paths.wallpaper_dir"),
            self.config.get("templates.wallpaper_file").format(year=year, month=month)
        )
    
    def _get_readme_path(self) -> str:
        """获取README文件路径"""
        return os.path.join(
            self.config.get("paths.readme_dir"),
            self.config.get("templates.readme_file").format(country_code=self.country_code)
        )
    
    def _generate_image_table(self, images: List[dict]) -> List[str]:
        """生成图片表格"""
        content = []
        content.append("|  |  |  |\n")
        content.append("|:---:|:---:|:---:|\n")
        
        # 每行显示3张图片
        for i in range(0, len(images), 3):
            row_images = images[i:i+3]
            row = []
            for img in row_images:
                preview_url = img['image_url'].replace(
                    self.config.get("image.uhd_suffix"),
                    self.config.get("image.preview_suffix")
                )
                cell = f"![]({preview_url} \"{img['head_line']}\") {img['date']}"
                row.append(cell)
            # 如果不足3个，补充空单元格
            while len(row) < 3:
                row.append("")
            content.append(f"| {' | '.join(row)} |\n")
        return content
    
    @retry(exceptions=(FileOperationError,), logger=logger)
    def update_files(self, images: List[WallpaperImage]) -> None:
        """更新所有文件"""
        try:
            # 转换为字典列表
            images_data = [img.to_dict() for img in images]
            
            # 按月份分组
            grouped_images = group_by_month(images_data)
            
            # 更新每个月的文件
            for (year, month), month_images in grouped_images.items():
                self._update_json_file(year, month, month_images)
                self._update_wallpaper_file(year, month, month_images)
            
            # 更新README文件
            self._update_readme_file(images_data)
            
            logger.info("所有文件更新完成")
        except Exception as e:
            raise FileOperationError(f"更新文件失败: {str(e)}")
    
    @retry(exceptions=(FileOperationError,), logger=logger)
    def _update_json_file(self, year: int, month: int, images: List[dict]) -> None:
        """更新JSON文件"""
        try:
            filepath = self._get_json_path(year, month)
            write_json(filepath, images)
            logger.debug(f"更新JSON文件: {filepath}")
        except Exception as e:
            raise FileOperationError(f"更新JSON文件失败: {str(e)}")
    
    @retry(exceptions=(FileOperationError,), logger=logger)
    def _update_wallpaper_file(self, year: int, month: int, images: List[dict]) -> None:
        """更新壁纸文件"""
        try:
            filepath = self._get_wallpaper_path(year, month)
            content = []
            
            # 添加标题
            content.append(f"# Bing Wallpaper ({year}-{month:02d})\n\n")
            
            # 生成表格
            content.extend(self._generate_image_table(images))
            
            write_text(filepath, "".join(content))
            logger.debug(f"更新壁纸文件: {filepath}")
        except Exception as e:
            raise FileOperationError(f"更新壁纸文件失败: {str(e)}")
    
    @retry(exceptions=(FileOperationError,), logger=logger)
    def _update_readme_file(self, images: List[dict]) -> None:
        """更新README文件"""
        try:
            content = []
            latest_image = images[0]
            
            # 第一部分：最新壁纸
            content.append("# Latest Wallpaper\n")
            content.append(f"![]({latest_image['image_url']})\n")
            content.append(f"[{latest_image['date']} {latest_image['head_line']} {latest_image['title']}({latest_image['copyright']})]({latest_image['image_url']})\n")
            content.append(f"{latest_image['main_text']}\n")
            content.append(f"{latest_image['desc']}\n")
            
            # 第二部分：最近30天
            content.append("# Recent 30 Days\n")
            content.extend(self._generate_image_table(images[:30]))
            
            # 第三部分：历史存档
            content.append("\n# History\n")
            archives_path = os.path.join(
                self.config.get("paths.archives_dir"),
                self.country_code,
                self.config.get("paths.wallpaper_dir")
            )
            
            if os.path.exists(archives_path):
                archive_files = list_files(archives_path, "w_")
                current_year = None
                year_months = []
                
                for file in archive_files:
                    year = file.split("_")[1]
                    month = file.split("_")[2].split(".")[0]
                    
                    if current_year != year:
                        if current_year is not None:
                            content.append(" | ".join(year_months) + "\n\n")
                        current_year = year
                        year_months = []
                    
                    link = f"[{year}-{month}](../archives/{self.country_code}/wallpaper/w_{year}_{month}.md)"
                    year_months.append(link)
                
                if year_months:
                    content.append(" | ".join(year_months) + "\n")
            
            write_text(self._get_readme_path(), "".join(content))
            logger.debug(f"更新README文件: {self._get_readme_path()}")
        except Exception as e:
            raise FileOperationError(f"更新README文件失败: {str(e)}") 