import re
from typing import Tuple
from src.config.config_manager import ConfigManager

def process_image_url(image_url: str) -> Tuple[str, str]:
    """
    处理图片URL，生成高清和预览版本
    :param image_url: 原始图片URL
    :return: (高清URL, 预览URL)的元组
    """
    if not image_url:
        return "", ""
        
    # 从图片URL中提取图片ID
    match = re.search(r"id=([^&]+)", image_url)
    if not match:
        return "", ""
        
    image_id = match.group(1)
    # 从图片ID中提取基础名称（不包含尺寸信息）
    base_image_id = re.sub(r"_\d+x\d+\.webp$", "", image_id)
    
    # 获取配置
    config = ConfigManager()
    base_url = config.get("image.base_url")
    uhd_suffix = config.get("image.uhd_suffix")
    preview_suffix = config.get("image.preview_suffix")
    
    # 生成高清和预览URL
    uhd_url = f"{base_url}/th?id={base_image_id}{uhd_suffix}"
    preview_url = f"{base_url}/th?id={base_image_id}{preview_suffix}"
    
    return uhd_url, preview_url 