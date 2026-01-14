import os
import sys
from pathlib import Path

# 添加上级目录到Python路径，确保可以导入window_mover模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import PyInstaller.__main__
except ImportError:
    print("PyInstaller未安装，请先运行: pip install pyinstaller")
    sys.exit(1)

# 构建PyInstaller命令
pyinstaller_command = [
    '--name=WindowMoverTool',  # 可执行文件名
    '--onefile',               # 打包成单个exe文件
    '--windowed',              # 不显示控制台窗口
    '--add-data=../window_mover;window_mover',  # 包含window_mover模块
    '--icon=NONE',             # 不设置图标（如果有的话可以用--icon=path/to/icon.ico）
    '--clean',                 # 清理临时文件
    'gui_window_mover.py'
]

print("开始打包WindowMoverTool...")
print(f"执行命令: pyinstaller {' '.join(pyinstaller_command)}")

# 运行PyInstaller
PyInstaller.__main__.run(pyinstaller_command)

print("打包完成！生成的exe文件位于dist文件夹中。")