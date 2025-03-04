# Bing API URL
BING_API_URL = "https://www.bing.com/hp/api/model"

# 支持的国家代码列表
COUNTRY_CODES = [
    "de-DE", "en-CA", "en-GB", "en-IN", "en-US", "es-ES",
    "fr-CA", "fr-FR", "it-IT", "ja-JP", "pt-BR", "zh-CN"
]

# 文件路径配置
ARCHIVES_DIR = "archives"
README_DIR = "readme"
JSON_DIR = "json"
WALLPAPER_DIR = "wallpaper"

# 文件名模板
JSON_FILE_TEMPLATE = "j_{year}_{month:02d}.json"
WALLPAPER_FILE_TEMPLATE = "w_{year}_{month:02d}.md"
README_FILE_TEMPLATE = "{country_code}.md"

# 图片URL配置
BASE_IMAGE_URL = "https://www.bing.com"
UHD_SUFFIX = "_UHD.jpg"
PREVIEW_SUFFIX = "_400x240.jpg"
