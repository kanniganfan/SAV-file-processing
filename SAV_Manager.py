# -*- coding: utf-8 -*-
"""
Ready Or Not - SAV Manager v2.0
SAV 存档管理工具

GitHub: https://github.com/your-repo
License: MIT

功能：
- 安装第三方地图预渲染文件 (.sav)
- MD5 哈希值去重检测
- 自动备份与恢复
- 清理游戏目录
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    os.system('title Ready Or Not - SAV Manager v2.0')
    os.system('mode con cols=78 lines=42')
    os.system('color 0A')

# 目录设置
SCRIPT_DIR = Path(__file__).parent
TARGET_DIR = Path(os.environ['LOCALAPPDATA']) / 'ReadyOrNot' / 'Saved' / 'SaveGames'
BACKUP_DIR = SCRIPT_DIR / '_SAV_BACKUP'
HASH_LOG = SCRIPT_DIR / '_hash_log.txt'

# 颜色代码
class Color:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if sys.platform == 'win32' else 'clear')

def calculate_md5(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def print_header():
    """打印标题"""
    print(f"""
{Color.GREEN}  ╔═══════════════════════════════════════════════════════════════════════╗
  ║                                                                       ║
  ║   ██████╗ ███████╗ █████╗ ██████╗ ██╗   ██╗     ██████╗ ██████╗       ║
  ║   ██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔═══██╗██╔══██╗      ║
  ║   ██████╔╝█████╗  ███████║██║  ██║ ╚████╔╝     ██║   ██║██████╔╝      ║
  ║   ██╔══██╗██╔══╝  ██╔══██║██║  ██║  ╚██╔╝      ██║   ██║██╔══██╗      ║
  ║   ██║  ██║███████╗██║  ██║██████╔╝   ██║       ╚██████╔╝██║  ██║      ║
  ║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝        ╚═════╝ ╚═╝  ╚═╝      ║
  ║                                                                       ║
  ║                 ███╗   ██╗ ██████╗ ████████╗                          ║
  ║                 ████╗  ██║██╔═══██╗╚══██╔══╝                          ║
  ║                 ██╔██╗ ██║██║   ██║   ██║                             ║
  ║                 ██║╚██╗██║██║   ██║   ██║                             ║
  ║                 ██║ ╚████║╚██████╔╝   ██║                             ║
  ║                 ╚═╝  ╚═══╝ ╚═════╝    ╚═╝                             ║
  ║                                                                       ║
  ║                   < SAV Manager v2.0 >                                ║
  ║                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}
""")

def print_menu():
    """打印主菜单"""
    print(f"""
  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐
  │                          【 功 能 菜 单 】                           │
  ├───────────────────────────────────────────────────────────────────────┤
  │                                                                       │
  │     {Color.WHITE}[1] 安装存档{Color.CYAN}  -  复制 .sav 文件到游戏目录 (自动去重)          │
  │                                                                       │
  │     {Color.WHITE}[2] 恢复备份{Color.CYAN}  -  从备份文件夹恢复原始存档文件                 │
  │                                                                       │
  │     {Color.WHITE}[3] 查看状态{Color.CYAN}  -  显示当前目录和游戏目录的存档信息             │
  │                                                                       │
  │     {Color.WHITE}[4] 清理目录{Color.CYAN}  -  删除游戏目录中的所有存档文件                 │
  │                                                                       │
  │     {Color.WHITE}[0] 退出程序{Color.CYAN}                                                  │
  │                                                                       │
  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}
""")

def get_sav_files(directory, exclude_backup=True):
    """获取目录下的所有.sav文件"""
    sav_files = []
    for root, dirs, files in os.walk(directory):
        if exclude_backup and '_SAV_BACKUP' in root:
            continue
        for file in files:
            if file.lower().endswith('.sav'):
                sav_files.append(Path(root) / file)
    return sav_files

def install_sav():
    """安装存档功能"""
    clear_screen()
    print(f"\n{Color.GREEN}  ╔═══════════════════════════════════════════════════════════════════════╗")
    print(f"  ║                        安 装 存 档 文 件                              ║")
    print(f"  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    
    # 步骤1：检查目录
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【步骤 1/4】检查目录...                                            │")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    # 创建目标目录
    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True)
        print(f"  {Color.GREEN}>> 已创建游戏存档目录{Color.RESET}")
    else:
        print(f"  {Color.GREEN}>> 游戏存档目录已存在{Color.RESET}")
    
    # 创建备份目录
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True)
        print(f"  {Color.GREEN}>> 已创建备份目录{Color.RESET}")
    else:
        print(f"  {Color.GREEN}>> 备份目录已存在{Color.RESET}")
    
    print()
    
    # 步骤2：扫描文件
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【步骤 2/4】扫描 .sav 文件...                                      │")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    sav_files = get_sav_files(SCRIPT_DIR)
    total = len(sav_files)
    
    print(f"  {Color.GREEN}>> 发现 {total} 个存档文件{Color.RESET}\n")
    
    if total == 0:
        print(f"  {Color.YELLOW}┌───────────────────────────────────────────────────────────────────────┐")
        print(f"  │  【警告】当前目录未找到任何 .sav 文件!                              │")
        print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
        input("  按回车键返回主菜单...")
        return
    
    # 步骤3：计算哈希并处理
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【步骤 3/4】计算哈希值并检测重复...                                │")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    # 写入哈希日志
    with open(HASH_LOG, 'w', encoding='utf-8') as log:
        log.write(f"# SAV 文件哈希记录 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write("# " + "=" * 60 + "\n\n")
    
    copied = 0
    skipped = 0
    backed = 0
    
    for sav_file in sav_files:
        filename = sav_file.name
        print(f"  {Color.WHITE}>> 处理: {filename}{Color.RESET}")
        
        # 计算源文件哈希
        source_hash = calculate_md5(sav_file)
        print(f"     哈希值: {Color.CYAN}{source_hash}{Color.RESET}")
        
        # 记录哈希
        with open(HASH_LOG, 'a', encoding='utf-8') as log:
            log.write(f"[源文件] {filename} = {source_hash}\n")
        
        target_file = TARGET_DIR / filename
        duplicate = False
        
        # 检查目标是否已存在同名文件
        if target_file.exists():
            target_hash = calculate_md5(target_file)
            if source_hash == target_hash:
                print(f"     状态: {Color.YELLOW}文件已存在且内容相同, 跳过{Color.RESET}")
                skipped += 1
                duplicate = True
            else:
                print(f"     状态: {Color.YELLOW}文件名相同但内容不同, 将覆盖{Color.RESET}")
        
        if not duplicate:
            try:
                # 复制文件到游戏目录
                shutil.copy2(sav_file, target_file)
                copied += 1
                print(f"     状态: {Color.GREEN}复制成功 [OK]{Color.RESET}")
                
                # 创建备份
                backup_file = BACKUP_DIR / f"{filename}.bak"
                shutil.move(str(sav_file), str(backup_file))
                backed += 1
                print(f"     备份: {Color.GREEN}已备份原文件 [OK]{Color.RESET}")
            except Exception as e:
                print(f"     状态: {Color.RED}操作失败 [FAIL] ({e}){Color.RESET}")
        
        print()
    
    # 步骤4：显示结果
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【步骤 4/4】安装完成                                               │")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    if copied > 0:
        print(f"""
  {Color.GREEN}╔═══════════════════════════════════════════════════════════════════════╗
  ║                                                                       ║
  ║   ███████╗██╗   ██╗ ██████╗ ██████╗███████╗███████╗███████╗██╗        ║
  ║   ██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝██║        ║
  ║   ███████╗██║   ██║██║     ██║     █████╗  ███████╗███████╗██║        ║
  ║   ╚════██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║╚═╝        ║
  ║   ███████║╚██████╔╝╚██████╗╚██████╗███████╗███████║███████║██╗        ║
  ║   ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝╚═╝        ║
  ║                                                                       ║
  ║                 [OK] 存档安装完成! 游戏存档已就绪!                    ║
  ║                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}
""")
    else:
        print(f"  {Color.YELLOW}┌───────────────────────────────────────────────────────────────────────┐")
        print(f"  │  【提示】所有文件已存在, 无需重复安装                               │")
        print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    # 统计报告
    print(f"""
  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐
  │  【统计报告】                                                        │
  │                                                                       │
  │    * 扫描文件:      {str(total).ljust(4)} 个                                       │
  │    * 成功复制:      {str(copied).ljust(4)} 个                                       │
  │    * 已存在跳过:    {str(skipped).ljust(4)} 个                                       │
  │    * 已备份:        {str(backed).ljust(4)} 个                                       │
  │                                                                       │
  │  【路径信息】                                                        │
  │    游戏目录: {str(TARGET_DIR)[:55]}
  │    备份目录: {str(BACKUP_DIR)[:55]}
  │    哈希日志: {str(HASH_LOG)[:55]}
  │                                                                       │
  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}
""")
    
    input("  按回车键返回主菜单...")

def restore_backup():
    """恢复备份功能"""
    clear_screen()
    print(f"\n{Color.CYAN}  ╔═══════════════════════════════════════════════════════════════════════╗")
    print(f"  ║                        恢 复 备 份 文 件                              ║")
    print(f"  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    
    if not BACKUP_DIR.exists():
        print(f"  {Color.YELLOW}┌───────────────────────────────────────────────────────────────────────┐")
        print(f"  │  【警告】备份目录不存在!                                            │")
        print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
        input("  按回车键返回主菜单...")
        return
    
    # 获取备份文件
    backup_files = list(BACKUP_DIR.glob('*.bak'))
    
    if not backup_files:
        print(f"  {Color.YELLOW}┌───────────────────────────────────────────────────────────────────────┐")
        print(f"  │  【警告】备份目录中没有找到任何备份文件!                            │")
        print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
        input("  按回车键返回主菜单...")
        return
    
    print(f"  >> 发现 {len(backup_files)} 个备份文件\n")
    
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【备份文件列表】                                                    │")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    for idx, bak_file in enumerate(backup_files, 1):
        # 去掉 .bak 后缀显示原文件名
        original_name = bak_file.stem
        print(f"    {idx}. {original_name}")
    
    print(f"""
  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐
  │  【操作选项】                                                        │
  │                                                                       │
  │    [A] 恢复所有备份文件                                               │
  │    [B] 返回主菜单                                                     │
  │                                                                       │
  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}
""")
    
    choice = input("  请输入选项: ").strip().upper()
    
    if choice == 'A':
        print(f"\n  >> 正在恢复所有备份文件...\n")
        
        restored = 0
        for bak_file in backup_files:
            original_name = bak_file.stem  # 去掉 .bak 后缀
            print(f"  >> 恢复: {original_name}")
            
            try:
                # 复制回原目录
                target_path = SCRIPT_DIR / original_name
                shutil.copy2(bak_file, target_path)
                restored += 1
                print(f"     状态: {Color.GREEN}恢复成功 [OK]{Color.RESET}")
            except Exception as e:
                print(f"     状态: {Color.RED}恢复失败 [FAIL] ({e}){Color.RESET}")
        
        print(f"""
  {Color.GREEN}╔═══════════════════════════════════════════════════════════════════════╗
  ║                         [OK] 备份恢复完成!                            ║
  ║                                                                       ║
  ║               已恢复 {str(restored).ljust(4)} 个文件到当前目录                        ║
  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}
""")
        input("  按回车键返回主菜单...")

def view_status():
    """查看状态功能"""
    clear_screen()
    print(f"\n{Color.CYAN}  ╔═══════════════════════════════════════════════════════════════════════╗")
    print(f"  ║                        存 档 状 态 信 息                              ║")
    print(f"  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    
    # 当前目录状态
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【当前目录】                                                        │")
    print(f"  │  {str(SCRIPT_DIR)[:65]}")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    local_files = get_sav_files(SCRIPT_DIR)
    if local_files:
        for f in local_files:
            print(f"    * {f.name}")
        print(f"\n    共 {len(local_files)} 个存档文件\n")
    else:
        print(f"    {Color.YELLOW}(无 .sav 文件){Color.RESET}\n")
    
    # 游戏目录状态
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【游戏目录】                                                        │")
    print(f"  │  {str(TARGET_DIR)[:65]}")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    if TARGET_DIR.exists():
        game_files = list(TARGET_DIR.glob('*.sav'))
        if game_files:
            for f in game_files:
                md5 = calculate_md5(f)
                print(f"    * {f.name}")
                print(f"      {Color.CYAN}MD5: {md5}{Color.RESET}")
            print(f"\n    共 {len(game_files)} 个存档文件\n")
        else:
            print(f"    {Color.YELLOW}(无 .sav 文件){Color.RESET}\n")
    else:
        print(f"    {Color.YELLOW}(目录不存在){Color.RESET}\n")
    
    # 备份目录状态
    print(f"  {Color.CYAN}┌───────────────────────────────────────────────────────────────────────┐")
    print(f"  │  【备份目录】                                                        │")
    print(f"  │  {str(BACKUP_DIR)[:65]}")
    print(f"  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}\n")
    
    if BACKUP_DIR.exists():
        backup_files = list(BACKUP_DIR.glob('*.bak'))
        if backup_files:
            for f in backup_files:
                print(f"    * {f.name}")
            print(f"\n    共 {len(backup_files)} 个备份文件\n")
        else:
            print(f"    {Color.YELLOW}(无备份文件){Color.RESET}\n")
    else:
        print(f"    {Color.YELLOW}(目录不存在){Color.RESET}\n")
    
    input("  按回车键返回主菜单...")

def clean_game_dir():
    """清理游戏目录功能"""
    clear_screen()
    print(f"\n{Color.RED}  ╔═══════════════════════════════════════════════════════════════════════╗")
    print(f"  ║                         清 理 游 戏 目 录                             ║")
    print(f"  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    
    print(f"""  {Color.YELLOW}┌───────────────────────────────────────────────────────────────────────┐
  │  【警告】此操作将删除游戏存档目录中的所有 .sav 文件!                 │
  │                                                                       │
  │  目标目录: {str(TARGET_DIR)[:55]}
  │                                                                       │
  │  这通常用于解决因存档冲突导致游戏无法启动的问题。                     │
  │                                                                       │
  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}
""")
    
    if not TARGET_DIR.exists():
        print(f"  >> 游戏存档目录不存在, 无需清理\n")
        input("  按回车键返回主菜单...")
        return
    
    game_files = list(TARGET_DIR.glob('*.sav'))
    
    if not game_files:
        print(f"  >> 游戏目录中没有 .sav 文件, 无需清理\n")
        input("  按回车键返回主菜单...")
        return
    
    print(f"  >> 游戏目录中有 {len(game_files)} 个 .sav 文件\n")
    
    print(f"""  {Color.YELLOW}┌───────────────────────────────────────────────────────────────────────┐
  │  确认要删除这些文件吗?                                                │
  │                                                                       │
  │    [Y] 是, 删除所有存档                                               │
  │    [N] 否, 返回主菜单                                                 │
  │                                                                       │
  └───────────────────────────────────────────────────────────────────────┘{Color.RESET}
""")
    
    choice = input("  请输入选项 [Y/N]: ").strip().upper()
    
    if choice == 'Y':
        print(f"\n  >> 正在删除...\n")
        
        deleted = 0
        for f in game_files:
            try:
                f.unlink()
                deleted += 1
                print(f"    删除: {f.name} {Color.GREEN}[OK]{Color.RESET}")
            except Exception as e:
                print(f"    删除: {f.name} {Color.RED}[FAIL] ({e}){Color.RESET}")
        
        print(f"""
  {Color.GREEN}╔═══════════════════════════════════════════════════════════════════════╗
  ║                           [OK] 清理完成!                              ║
  ║                                                                       ║
  ║               已删除 {str(deleted).ljust(4)} 个存档文件                               ║
  ║               现在可以重新安装正确的存档了                            ║
  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}
""")
        input("  按回车键返回主菜单...")

def main():
    """主函数"""
    # 启用 Windows 终端的 ANSI 颜色支持
    if sys.platform == 'win32':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("  请输入选项 [0-4]: ").strip()
        
        if choice == '1':
            install_sav()
        elif choice == '2':
            restore_backup()
        elif choice == '3':
            view_status()
        elif choice == '4':
            clean_game_dir()
        elif choice == '0':
            clear_screen()
            print(f"""
  {Color.GREEN}╔═══════════════════════════════════════════════════════════════════════╗
  ║                                                                       ║
  ║                   感谢使用 SAV Manager                                ║
  ║                                                                       ║
  ║                          再见! ^_^                                    ║
  ║                                                                       ║
  ╚═══════════════════════════════════════════════════════════════════════╝{Color.RESET}
""")
            break

if __name__ == '__main__':
    main()
