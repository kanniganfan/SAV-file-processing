# Ready Or Not - SAV Manager / SAV 存档管理工具

[English](#english) | [中文](#中文)

---

## English

### Description

One-click SAV manager for Ready Or Not custom maps. This tool helps you manage pre-rendered `.sav` files for third-party maps.

**Note:** Not all map authors provide `.sav` files. This tool works with existing `.sav` files only.

### Features

- **Auto Install** - Copy `.sav` files to game directory with MD5 hash duplicate detection
- **Backup & Restore** - Automatically backup original files, restore anytime
- **Status View** - Display all `.sav` files with MD5 hash values
- **Conflict Cleanup** - Delete all `.sav` files to fix game launch issues

### What is a .sav file?

`.sav` files contain pre-rendered/pre-calculated data for custom maps, including:
- Lighting and shadow data
- Navigation mesh
- Other pre-calculated information

Installing the correct `.sav` file can:
- Speed up map loading
- Ensure proper lighting and shadows
- Avoid long loading times

### Installation

1. Download `SAV_Manager.exe`
2. Place it in your maps folder
3. Put `.sav` files in the same directory
4. Run `SAV_Manager.exe`

### Usage

1. **[1] Install** - Scan and install `.sav` files to game directory
2. **[2] Restore** - Restore backed up files
3. **[3] Status** - View all `.sav` files and their MD5 hashes
4. **[4] Clean** - Delete all `.sav` files from game directory
5. **[0] Exit** - Exit the program

### Game Directory

```
%LocalAppData%\ReadyOrNot\Saved\SaveGames
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Game won't start after install | Use [4] Clean to delete all `.sav` files |
| No `.sav` file from map author | Game will generate data on first load (slower) |
| "File already exists" message | File is already installed, skipped automatically |

---

## 中文

### 简介

Ready Or Not 第三方地图预渲染文件（.sav）一键管理工具。

**注意：** 并非所有地图作者都会提供 .sav 文件，本工具仅处理已有的 .sav 文件。

### 功能特性

- **一键安装** - 复制 .sav 文件到游戏目录，自动 MD5 哈希去重
- **备份恢复** - 自动备份原始文件，随时可恢复
- **状态查看** - 显示所有 .sav 文件及其 MD5 哈希值
- **冲突清理** - 删除游戏目录中的 .sav 文件，修复无法启动问题

### 什么是 .sav 文件？

.sav 文件包含第三方地图的预渲染/预计算数据：
- 光照和阴影数据
- 导航网格
- 其他预计算信息

安装正确的 .sav 文件可以：
- 加快地图加载速度
- 确保光照阴影正确显示
- 避免首次加载的长时间等待

### 安装方法

1. 下载 `SAV_Manager.exe`
2. 放到地图文件夹中
3. 将 .sav 文件放在同一目录
4. 运行 `SAV_Manager.exe`

### 使用说明

1. **[1] 安装存档** - 扫描并安装 .sav 文件到游戏目录
2. **[2] 恢复备份** - 恢复已备份的文件
3. **[3] 查看状态** - 查看所有 .sav 文件及其 MD5 哈希值
4. **[4] 清理目录** - 删除游戏目录中的所有 .sav 文件
5. **[0] 退出程序** - 退出

### 游戏目录

```
%LocalAppData%\ReadyOrNot\Saved\SaveGames
```

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 安装后游戏无法启动 | 使用 [4] 清理目录删除所有 .sav 文件 |
| 地图作者没提供 .sav 文件 | 游戏会在首次加载时自动生成（较慢） |
| 提示"文件已存在" | 表示文件已安装，自动跳过 |

---


Free to use / 免费使用

## KANNI

2026 - Ready Or Not Community
