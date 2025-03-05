import requests
import logging
import time
from typing import Optional, Dict, Any
from src.config.config_manager import ConfigManager
from src.utils.exceptions import APIError

logger = logging.getLogger(__name__)


def fetch_bing_data(country_code: str = "zh-CN") -> Dict[str, Any]:
    """
    获取Bing壁纸数据
    :param country_code: 国家代码
    :return: JSON响应数据
    :raises: APIError 当API调用失败时
    """
    config = ConfigManager()
    api_url = config.get("api.url")
    max_retries = config.get("api.max_retries", 3)
    wait_time = config.get("api.wait_time", 30)
    params = {"mkt": country_code}

    for attempt in range(max_retries):
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt < max_retries - 1:  # 如果不是最后一次尝试
                logger.warning(
                    f"第 {attempt + 1} 次获取数据失败: {e}，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                logger.error(f"获取数据失败，已重试 {max_retries} 次: {e}")
                raise APIError(f"获取数据失败: {e}")

    return None
