import requests
import logging
from typing import Optional, Dict, Any
from src.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)

def fetch_bing_data(country_code: str = "zh-CN") -> Optional[Dict[str, Any]]:
    """
    获取Bing壁纸数据
    :param country_code: 国家代码
    :return: JSON响应数据
    """
    config = ConfigManager()
    api_url = config.get("api.url")
    params = {"mkt": country_code}
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"获取数据失败: {e}")
        return None 