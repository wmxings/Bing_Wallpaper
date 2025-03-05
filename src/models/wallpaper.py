from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from src.utils.date_utils import extract_date_from_trivia_id
from src.services.image_processor import process_image_url


@dataclass
class WallpaperImage:
    """壁纸图片数据模型"""
    date: str
    head_line: str
    title: str
    copyright: str
    desc: str
    image_url: str
    preview_url: str
    main_text: str
    sizes: Dict[str, str]

    @classmethod
    def from_api_response(cls, image_content: dict) -> 'WallpaperImage':
        """从API响应创建实例"""
        trivia_id = image_content.get("TriviaId", "")
        image_url = image_content.get("Image", {}).get("Url", "")

        # 处理图片URL
        uhd_url, preview_url, sizes = process_image_url(image_url)

        return cls(
            date=extract_date_from_trivia_id(trivia_id),
            head_line=image_content.get("Headline", ""),
            title=image_content.get("Title", ""),
            copyright=image_content.get("Copyright", ""),
            desc=image_content.get("Description", ""),
            image_url=uhd_url,
            preview_url=preview_url,
            main_text=image_content.get("QuickFact", {}).get("MainText", ""),
            sizes=sizes
        )

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "date": self.date,
            "head_line": self.head_line,
            "title": self.title,
            "copyright": self.copyright,
            "desc": self.desc,
            "image_url": self.image_url,
            "preview_url": self.preview_url,
            "main_text": self.main_text,
            "sizes": self.sizes
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'WallpaperImage':
        """从字典创建实例"""
        return cls(**data)
