import logging
import time
from typing import List
from src.models.wallpaper import WallpaperImage
from src.services.bing_api import fetch_bing_data
from src.services.file_generator import FileGenerator
from src.utils.exceptions import BingWallpaperError
from src.config.config_manager import ConfigManager

def setup_logging():
    """设置日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # 输出到控制台
            logging.FileHandler('bing_wallpaper.log')  # 输出到文件
        ]
    )

def process_images(data: dict) -> List[WallpaperImage]:
    """
    处理API返回的图片数据
    :param data: API返回的数据
    :return: 壁纸图片列表
    """
    images = []
    media_contents = data.get("MediaContents", [])
    for item in media_contents:
        if "ImageContent" in item:
            image = WallpaperImage.from_api_response(item["ImageContent"])
            if image.date:  # 只添加有效的数据
                images.append(image)
    
    # 按日期排序
    return sorted(images, key=lambda x: x.date, reverse=True)

def process_country(country_code: str, logger: logging.Logger) -> bool:
    """
    处理单个国家的数据
    :param country_code: 国家代码
    :param logger: 日志记录器
    :return: 处理是否成功
    """
    try:
        logger.info(f"开始处理 {country_code} 的壁纸数据")
        
        # 获取数据
        data = fetch_bing_data(country_code)
        if not data:
            logger.error(f"{country_code}: 获取数据失败")
            return False
        
        # 处理图片数据
        images = process_images(data)
        if not images:
            logger.warning(f"{country_code}: 没有找到有效的图片数据")
            return False
        
        # 生成文件
        file_generator = FileGenerator(country_code)
        file_generator.update_files(images)
        
        logger.info(f"{country_code}: 处理完成")
        return True
        
    except Exception as e:
        logger.error(f"{country_code}: 处理失败 - {str(e)}")
        return False

def main():
    """主函数"""
    try:
        # 设置日志记录
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # 初始化配置
        config = ConfigManager()
        country_codes = config.get("supported_countries")
        total_countries = len(country_codes)
        
        logger.info(f"开始处理 {total_countries} 个国家的数据")
        
        # 处理每个国家的数据
        success_count = 0
        for index, country_code in enumerate(country_codes, 1):
            logger.info(f"[{index}/{total_countries}] 处理 {country_code}")
            
            if process_country(country_code, logger):
                success_count += 1
            
            # 如果不是最后一个国家，等待10秒后继续
            if index < total_countries:
                logger.info(f"等待10秒后继续处理下一个国家...")
                time.sleep(10)
        
        # 输出总结信息
        logger.info(f"处理完成: 成功 {success_count}/{total_countries}")
        
    except BingWallpaperError as e:
        logger.error(f"处理失败: {str(e)}")
    except Exception as e:
        logger.exception(f"发生未知错误: {str(e)}")

if __name__ == "__main__":
    main() 