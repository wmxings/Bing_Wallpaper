import os
import json
from typing import List, Any


def ensure_dir(path: str) -> None:
    """确保目录存在，如果不存在则创建"""
    os.makedirs(path, exist_ok=True)


def write_json(filepath: str, data: Any) -> None:
    """
    写入JSON文件
    :param filepath: 文件路径
    :param data: 要写入的数据
    """
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json(filepath: str) -> Any:
    """
    读取JSON文件
    :param filepath: 文件路径
    :return: 读取的数据
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_text(filepath: str, content: str) -> None:
    """
    写入文本文件
    :param filepath: 文件路径
    :param content: 要写入的内容
    """
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def list_files(directory: str, pattern: str = None) -> List[str]:
    """
    列出目录中的文件
    :param directory: 目录路径
    :param pattern: 文件名模式（可选）
    :return: 文件名列表
    """
    if not os.path.exists(directory):
        return []

    files = os.listdir(directory)
    if pattern:
        files = [f for f in files if f.startswith(pattern)]
    return sorted(files, reverse=True)
