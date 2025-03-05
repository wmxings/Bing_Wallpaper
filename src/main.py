import logging
import time
import os
from datetime import datetime
from typing import List
from src.models.wallpaper import WallpaperImage
from src.services.bing_api import fetch_bing_data
from src.services.file_generator import FileGenerator
from src.utils.exceptions import BingWallpaperError, APIError
from src.config.config_manager import ConfigManager


# 添加一个空行，满足 E302 要求


def setup_logging():
    """设置日志记录"""
    # 创建一个基础的控制台日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)

    try:
        config = ConfigManager()
        log_dir = config.get("paths.log_dir")

        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)

        # 生成日志文件名
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(
            log_dir,
            config.get("templates.log_file").format(date=date_str)
        )

        # 添加文件处理器，明确指定 UTF-8 编码
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s][%(levelname)s][%(name)s] %(message)s'))
        logging.getLogger().addHandler(file_handler)

        logger.info(f"日志文件已创建: {log_file}")
    except Exception as e:
        logger.error(f"设置日志文件失败: {str(e)}")


# 移除空行中的空格


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


# 移除空行中的空格


def process_country(country_code: str, logger: logging.Logger) -> bool:
    """
    处理单个国家的数据
    :param country_code: 国家代码
    :param logger: 日志记录器
    :return: 处理是否成功
    """
    log_prefix = f"{country_code}:"

    try:
        logger.info(f"{log_prefix} 开始处理壁纸数据")

        # 获取数据
        data = fetch_bing_data(country_code)

        # 处理图片数据
        images = process_images(data)
        if not images:
            logger.warning(f"{log_prefix} 没有找到有效的图片数据")
            return False

        # 生成文件
        file_generator = FileGenerator(country_code)
        file_generator.update_files(images)

        logger.info(f"{log_prefix} 处理完成")
        return True

    except APIError as e:
        logger.error(f"{log_prefix} API调用失败 - {str(e)}")
        return False
    except Exception as e:
        logger.error(f"{log_prefix} 处理失败 - {str(e)}")
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
        wait_time = config.get("process.wait_time", 10)  # 获取等待时间，默认10秒

        logger.info(f"开始处理 {total_countries} 个国家的数据")

        # 处理每个国家的数据
        success_count = 0
        for index, country_code in enumerate(country_codes, 1):
            logger.info(f"[{index}/{total_countries}] 处理 {country_code}")

            if process_country(country_code, logger):
                success_count += 1

            # 如果不是最后一个国家，等待指定时间后继续
            if index < total_countries:
                logger.info(f"等待 {wait_time} 秒后继续处理下一个国家...")
                time.sleep(wait_time)

        # 输出总结信息
        success_rate = (success_count / total_countries) * 100
        logger.info(
            f"处理完成: 成功 {success_count}/{total_countries} ({success_rate:.1f}%)")

    except BingWallpaperError as e:
        logger.error(f"处理失败: {str(e)}")
        raise
    except Exception as e:
        logger.exception(f"发生未知错误: {str(e)}")
        raise


# 确保文件末尾有换行符
if __name__ == "__main__":
    main()
