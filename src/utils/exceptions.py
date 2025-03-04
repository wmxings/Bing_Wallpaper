class BingWallpaperError(Exception):
    """基础异常类"""
    pass


class FileOperationError(BingWallpaperError):
    """文件操作异常"""
    pass


class APIError(BingWallpaperError):
    """API调用异常"""
    pass


class ConfigError(BingWallpaperError):
    """配置相关异常"""
    pass
