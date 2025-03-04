import re
from datetime import datetime
from typing import Optional


def extract_date_from_trivia_id(trivia_id: str) -> Optional[str]:
    """
    从TriviaId中提取日期
    :param trivia_id: TriviaId字符串
    :return: 格式化的日期字符串 (YYYY-MM-DD)
    """
    match = re.search(r"(\d{8})", trivia_id)
    if match:
        date_str = match.group(1)
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return None


def group_by_month(items: list, date_key: str = 'date') -> dict:
    """
    将数据按月份分组
    :param items: 数据列表
    :param date_key: 日期字段的键名
    :return: 按月份分组的字典，格式为 {(year, month): [items]}
    """
    grouped = {}
    for item in items:
        date = datetime.strptime(item[date_key], '%Y-%m-%d')
        key = (date.year, date.month)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(item)
    return grouped
