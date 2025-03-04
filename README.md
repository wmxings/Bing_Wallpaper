[Home]readme/(README.md) | [中文](readme/zh-CN.md) | [English (US)](readme/en-US.md) | [Deutsch](readme/de-DE.md) | [English (CA)](readme/en-CA.md) | [English (GB)](readme/en-GB.md) | [English (IN)](readme/en-IN.md) | [Español](readme/es-ES.md) | [Français (CA)](readme/fr-CA.md) | [Français (FR)](readme/fr-FR.md) | [Italiano](readme/it-IT.md) | [日本語](readme/ja-JP.md) | [Português](readme/pt-BR.md)

# Bing Wallpaper Downloader

这是一个自动获取Bing每日壁纸的Python脚本。它会从Bing的API获取壁纸数据，并将其保存为结构化的文件。

## 功能特点

- 自动获取Bing每日壁纸数据
- 支持多个国家地区的壁纸
- 生成Markdown格式的壁纸展示页面
- 保存完整的JSON格式元数据
- 自动更新README文件
- 支持历史存档浏览
- 提供多种尺寸的壁纸链接
- 结构化日志记录，支持UTF-8编码

## 目录结构

```
.
├── archives/              # 存档目录
│   └── zh-CN/            # 按国家代码分类
│       ├── wallpaper/    # 壁纸展示页面
│       └── json/         # 元数据JSON文件
├── src/                  # 源代码
│   ├── config/          # 配置管理
│   ├── log/             # 日志文件
│   ├── models/          # 数据模型
│   ├── services/        # 服务层
│   └── utils/           # 工具类
├── readme/              # 国家特定的README文件
└── requirements.txt     # 项目依赖
```

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/your-username/bing-wallpaper.git
cd bing-wallpaper
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

直接运行脚本：
```bash
python src/main.py
```

## 配置

程序首次运行时会自动创建 `config.json` 配置文件，您可以根据需要修改以下配置：

```json
{
  "supported_countries": ["zh-CN", "en-US"],
  "paths": {
    "archive_dir": "archives",
    "readme_dir": "readme",
    "log_dir": "src/log"
  },
  "image": {
    "base_url": "https://www.bing.com",
    "uhd_suffix": "_UHD.jpg",
    "preview_suffix": "_400x240.jpg"
  },
  "process": {
    "wait_time": 10
  },
  "templates": {
    "log_file": "log_{date}.log"
  }
}
```

## 日志

程序运行时会生成格式化的日志，存储在 `src/log` 目录下，日志格式为：

```
[时间戳][日志级别][模块名] 日志内容
```

## 壁纸尺寸

程序支持多种壁纸尺寸，包括：

- UHD (超高清)
- 1920x1200
- 1920x1080
- 1080x1920
- 1366x768
- 1280x768
- 1024x768
- 800x600
- 800x480
- 768x1280
- 720x1280
- 640x480
- 480x800
- 400x240
- 320x240
- 240x320

## 自动运行

可以设置GitHub Actions在每天早上6点自动运行脚本。

## 支持的国家/地区代码

- de-DE (德国)
- en-CA (加拿大英语)
- en-GB (英国)
- en-IN (印度)
- en-US (美国)
- es-ES (西班牙)
- fr-CA (加拿大法语)
- fr-FR (法国)
- it-IT (意大利)
- ja-JP (日本)
- pt-BR (巴西)
- zh-CN (中国) 