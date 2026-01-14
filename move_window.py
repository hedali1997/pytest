import sys
import time
import subprocess
import argparse
from ctypes import windll, Structure, c_long, byref
import win32gui
import win32process
import psutil


class RECT(Structure):
    _fields_ = [
        ('left', c_long),
        ('top', c_long),
        ('right', c_long),
        ('bottom', c_long)
    ]


def get_window_rect(hwnd):
    """获取窗口矩形信息"""
    rect = RECT()
    windll.user32.GetWindowRect(hwnd, byref(rect))
    return rect


def move_window(hwnd, x, y, width=None, height=None):
    """
    移动窗口到指定位置
    :param hwnd: 窗口句柄
    :param x: 新的x坐标
    :param y: 新的y坐标
    :param width: 新的宽度（可选，默认保持原宽度）
    :param height: 新的高度（可选，默认保持原高度）
    :return: 成功返回True，否则返回False
    """
    # 获取当前窗口大小
    current_rect = get_window_rect(hwnd)
    current_width = current_rect.right - current_rect.left
    current_height = current_rect.bottom - current_rect.top
    
    # 如果没有提供新尺寸，则使用当前尺寸
    if width is None:
        width = current_width
    if height is None:
        height = current_height
        
    # 调用API移动窗口
    success = windll.user32.MoveWindow(
        hwnd,           # 窗口句柄
        x,              # 新的x坐标
        y,              # 新的y坐标
        width,          # 新的宽度
        height,         # 新的高度
        True            # 是否重绘窗口
    )
    
    if success:
        print(f"窗口已移动到 ({x}, {y})，大小: {width}x{height}")
    else:
        print("移动窗口失败")
    
    return success


def find_window_by_title(window_title):
    """
    根据标题查找窗口
    :param window_title: 窗口标题或标题的一部分
    :return: 匹配的窗口句柄列表
    """
    def enum_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_title.lower() in window_text.lower():
                windows.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(enum_callback, windows)
    return windows


def find_window_by_process_name(process_name):
    """
    根据进程名查找窗口
    :param process_name: 进程名称，如"notepad.exe"
    :return: 窗口句柄列表
    """
    def enum_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                if process.name().lower() == process_name.lower():
                    windows.append(hwnd)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return True
    
    windows = []
    win32gui.EnumWindows(enum_callback, windows)
    return windows


def move_exe_to_position(target, x, y, width=None, height=None):
    """
    将指定exe的窗口移动到指定位置
    :param target: exe名称或窗口标题
    :param x: 目标x坐标
    :param y: 目标y坐标
    :param width: 目标宽度（可选）
    :param height: 目标高度（可选）
    """
    # 首先尝试按标题查找窗口
    windows = find_window_by_title(target)
    
    # 如果按标题没有找到，再尝试按进程名查找
    if not windows:
        # 只有当target看起来像一个进程名（例如包含.exe或全是英文字母）时才按进程查找
        if '.' in target or target.encode('utf-8').isalpha():  # 包含扩展名或全英文
            process_name = target if target.endswith('.exe') else f"{target}.exe"
            windows = find_window_by_process_name(process_name)
        else:  # 中文或混合名称，直接尝试对应的exe进程
            # 对于中文名称，尝试对应的exe名称，如"记事本"可能是"notepad.exe"
            # 或者尝试是否以.exe结尾
            if not target.endswith('.exe'):
                # 尝试常见的中文名对应的exe
                chinese_to_exe = {
                    "记事本": "notepad.exe",
                    "计算器": "calc.exe",
                    "画图": "mspaint.exe",
                    "写字板": "wordpad.exe"
                }
                
                if target in chinese_to_exe:
                    windows = find_window_by_process_name(chinese_to_exe[target])
                else:
                    # 如果不是已知的中文名称，就不尝试按进程查找
                    pass
            else:
                windows = find_window_by_process_name(target)
    
    if windows:
        for hwnd in windows:
            move_window(hwnd, x, y, width, height)
    else:
        print(f"找不到名为 '{target}' 的窗口或进程")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='移动指定exe程序窗口到指定位置')
    parser.add_argument('target', help='目标exe名称或窗口标题')
    parser.add_argument('x', type=int, help='目标x坐标')
    parser.add_argument('y', type=int, help='目标y坐标')
    parser.add_argument('--width', type=int, help='目标窗口宽度')
    parser.add_argument('--height', type=int, help='目标窗口高度')
    
    args = parser.parse_args()
    
    # 检查是否为Windows系统
    if sys.platform != 'win32':
        print("此脚本仅支持Windows系统")
        return
    
    move_exe_to_position(args.target, args.x, args.y, args.width, args.height)


if __name__ == "__main__":
    # 如果直接运行脚本且没有命令行参数，则显示帮助信息
    if len(sys.argv) == 1:
        print("窗口移动工具")
        print("="*30)
        print("功能：移动指定exe程序窗口到指定位置")
        print("说明：特别适用于无边框模式的程序窗口")
        print("\n使用方法:")
        print("  python move_window.py <exe名称或窗口标题> <x坐标> <y坐标> [--width 宽度] [--height 高度]")
        print("\n示例:")
        print("  python move_window.py notepad.exe 100 100")
        print("  python move_window.py 记事本 200 200 --width 800 --height 600")
        
        print("\n" + "="*30)
        response = input("是否要尝试移动屏幕上已打开的记事本窗口？(y/n): ")
        if response.lower() == 'y':
            # 不启动新的记事本，只寻找已存在的窗口
            move_exe_to_position("记事本", 100, 100, 800, 600)
    else:
        main()