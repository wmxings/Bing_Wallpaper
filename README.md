# Bing Wallpaper Downloader

这是一个自动获取Bing每日壁纸的Python脚本。它会从Bing的API获取壁纸数据，并将其保存为结构化的文件。

## 功能特点

- 自动获取Bing每日壁纸数据
- 支持多个国家地区的壁纸
- 生成Markdown格式的壁纸展示页面
- 保存完整的JSON格式元数据
- 自动更新README文件
- 支持历史存档浏览

## 目录结构

```
.
├── archives/              # 存档目录
│   └── zh-CN/            # 按国家代码分类
│       ├── wallpaper/    # 壁纸展示页面
│       └── json/         # 元数据JSON文件
├── src/                  # 源代码
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
python src/bing_wallpaper.py
```

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

## 许可证

MIT 