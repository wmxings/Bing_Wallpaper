import os
import json
import logging
from typing import Any, Dict, Optional
from src.utils.exceptions import ConfigError

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器"""
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self.load_config()

    def load_config(self, config_file: str = "config.json") -> None:
        """
        加载配置文件
        :param config_file: 配置文件路径
        """
        try:
            # 首先尝试从配置文件加载
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                logger.info(f"从 {config_file} 加载配置")
            else:
                # 如果配置文件不存在，使用默认配置并创建配置文件
                self._config = self._get_default_config()
                self.save_config(config_file)
                logger.info(f"创建默认配置文件 {config_file}")
        except Exception as e:
            raise ConfigError(f"加载配置文件失败: {str(e)}")

    def save_config(self, config_file: str = "config.json") -> None:
        """
        保存配置到文件
        :param config_file: 配置文件路径
        """
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ConfigError(f"保存配置文件失败: {str(e)}")

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "api": {
                "url": "https://www.bing.com/hp/api/model",
                "max_retries": 3,      # API 最大重试次数
                "wait_time": 30        # API 重试等待时间（秒）
            },
            "process": {
                "wait_time": 1        # 处理国家之间的等待时间（秒）
            },
            "paths": {
                "archives_dir": "archives",
                "readme_dir": "readme",
                "json_dir": "archives/json",
                "wallpaper_dir": "archives/wallpaper",
                "log_dir": "src/log"   # 日志目录
            },
            "templates": {
                "json_file": "j_{year}_{month:02d}.json",
                "wallpaper_file": "w_{year}_{month:02d}.md",
                "readme_file": "{country_code}.md",
                "log_file": "log_{date}.log"  # 日志文件名模板
            },
            "image": {
                "base_url": "https://www.bing.com",
                "uhd_suffix": "_UHD.jpg",
                "preview_suffix": "_400x240.jpg"
            },
            "supported_countries": [
                "zh-CN",   # 中国
                "en-US",   # 美国
                "de-DE",   # 德国
                "en-CA",   # 加拿大（英语）
                "en-GB",   # 英国
                "en-IN",   # 印度
                "es-ES",   # 西班牙
                "fr-CA",   # 加拿大（法语）
                "fr-FR",   # 法国
                "it-IT",   # 意大利
                "ja-JP",   # 日本
                "pt-BR"    # 巴西
            ]
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        :param key: 配置键，支持点号分隔的多级键
        :param default: 默认值
        :return: 配置值
        """
        try:
            value = self._config
            for k in key.split('.'):
                value = value[k]
            return value
        except KeyError:
            if default is not None:
                return default
            raise ConfigError(f"配置项不存在: {key}")

    def set(self, key: str, value: Any) -> None:
        """
        设置配置项
        :param key: 配置键，支持点号分隔的多级键
        :param value: 配置值
        """
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
