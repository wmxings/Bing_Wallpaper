import re
from typing import Dict, Tuple
from src.config.config_manager import ConfigManager


def process_image_url(url: str) -> Tuple[str, str, Dict[str, str]]:
    """
    处理图片URL，生成不同尺寸的URL
    :param url: 原始图片URL
    :return: (UHD URL, 预览URL, 尺寸URL字典)
    """
    if not url:
        return "", "", {}

    # 从图片URL中提取图片ID
    match = re.search(r"id=([^&]+)", url)
    if not match:
        return "", "", {}

    image_id = match.group(1)
    # 从图片ID中提取基础名称（不包含尺寸信息）
    base_image_id = re.sub(r"_\d+x\d+\.webp$", "", image_id)

    config = ConfigManager()
    base_url = config.get("image.base_url")
    uhd_suffix = config.get("image.uhd_suffix")
    preview_suffix = config.get("image.preview_suffix")

    # 生成UHD和预览URL
    uhd_url = f"{base_url}/th?id={base_image_id}{uhd_suffix}"
    preview_url = f"{base_url}/th?id={base_image_id}{preview_suffix}"

    # 生成不同尺寸的URL
    sizes = {
        "UHD": uhd_url,  # 添加UHD尺寸
        "1920x1200": f"{base_url}/th?id={base_image_id}_1920x1200.jpg",
        "1920x1080": f"{base_url}/th?id={base_image_id}_1920x1080.jpg",
        "1080x1920": f"{base_url}/th?id={base_image_id}_1080x1920.jpg",
        "1366x768": f"{base_url}/th?id={base_image_id}_1366x768.jpg",
        "1280x768": f"{base_url}/th?id={base_image_id}_1280x768.jpg",
        "1024x768": f"{base_url}/th?id={base_image_id}_1024x768.jpg",
        "800x600": f"{base_url}/th?id={base_image_id}_800x600.jpg",
        "800x480": f"{base_url}/th?id={base_image_id}_800x480.jpg",
        "768x1280": f"{base_url}/th?id={base_image_id}_768x1280.jpg",
        "720x1280": f"{base_url}/th?id={base_image_id}_720x1280.jpg",
        "640x480": f"{base_url}/th?id={base_image_id}_640x480.jpg",
        "480x800": f"{base_url}/th?id={base_image_id}_480x800.jpg",
        "400x240": f"{base_url}/th?id={base_image_id}_400x240.jpg",
        "320x240": f"{base_url}/th?id={base_image_id}_320x240.jpg",
        "240x320": f"{base_url}/th?id={base_image_id}_240x320.jpg"
    }

    return uhd_url, preview_url, sizes
