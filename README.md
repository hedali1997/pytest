# PDF水印工具及窗口移动工具

## PDF水印工具

这个Python脚本可以在PDF文档中添加图片或文字水印，主要功能包括：

- 在PDF文档的每一页添加图片水印
- 支持自定义水印位置和透明度
- 支持添加文字水印，可使用自定义字体
- 支持OTF字体格式转换为TTF格式
- 可通过命令行参数批量处理PDF文件

### PDF水印功能特点

- 图片水印：将指定图片作为水印添加到PDF每一页
- 文字水印：使用自定义字体添加文字水印
- 位置控制：可自定义水印的位置坐标(x, y)
- 透明度调节：可设置水印透明度(alpha值)
- 批量处理：支持命令行参数方式批量处理PDF文件

### PDF水印使用方法

```bash
cd pdf_tools
python main.py <输入PDF路径> <水印图片路径> <输出PDF路径>
```

## 窗口移动工具

这个Python脚本可以移动指定exe程序的窗口位置，特别适用于无边框模式的程序窗口，这些窗口通常无法通过常规方式拖拽移动。

### 功能特点

- 可以根据进程名称或窗口标题定位窗口
- 支持设置窗口的新位置(x, y坐标)
- 支持设置窗口的新尺寸(宽度和高度)
- 适用于Windows系统上的任何应用程序窗口
- 可以移动已经打开的程序窗口，无需重新启动

## 依赖包

- pywin32: 提供Windows API接口
- psutil: 用于获取进程信息
- 其他标准库: ctypes, argparse等

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行方式

```bash
cd window_mover
python move_window.py <exe名称或窗口标题> <x坐标> <y坐标> [--width 宽度] [--height 高度]
```

### 示例

```bash
# 移动记事本窗口到坐标(100, 100)
cd window_mover
python move_window.py notepad.exe 100 100

# 移动记事本窗口并设置尺寸为800x600
cd window_mover
python move_window.py notepad.exe 100 100 --width 800 --height 600

# 根据窗口标题移动(如中文标题"记事本")
cd window_mover
python move_window.py "记事本" 200 200 --width 800 --height 600
```

### 交互式运行

直接运行脚本，按照提示进行操作：

```bash
cd window_mover
python move_window.py
```

## 窗口移动GUI工具

我们还提供了一个图形用户界面版本的窗口移动工具，使操作更加便捷。

### 启动GUI

1. 使用批处理文件启动：
   ```
   cd gui_app
   run_gui.bat
   ```

2. 或直接运行Python脚本：
   ```
   cd gui_app
   python gui_window_mover.py
   ```

### GUI功能特点

- 直观的图形界面，无需命令行操作
- 输入框用于设置目标窗口名称、坐标和尺寸
- 快速预设按钮，一键设置常用程序
- 实时结果显示在底部文本区域
- 支持使用默认窗口尺寸选项

GUI界面包含以下控件：
- 目标窗口名称/进程名输入框
- X和Y坐标输入框
- 宽度和高度输入框
- "使用窗口原始尺寸"复选框
- 针对常见程序的预设按钮
- 移动窗口按钮
- 结果显示区域

## 打包为EXE可执行文件

您可以将GUI应用打包为独立的exe文件，这样就可以在没有安装Python环境的机器上运行。

### 打包步骤

1. 安装PyInstaller（如果尚未安装）：
   ```
   pip install pyinstaller
   ```

2. 使用以下命令生成spec文件：
   ```
   cd gui_app
   pyi-makespec --onedir --windowed gui_window_mover.py
   ```

3. 编辑生成的spec文件，确保包含必要的依赖项

4. 使用spec文件构建exe：
   ```
   cd gui_app
   pyinstaller gui_window_mover.spec
   ```

### 直接运行EXE版本

打包完成后，在`dist/gui_app`目录下会生成exe文件，可以直接运行：
- 使用提供的批处理文件：`run_gui_exe.bat`
- 或直接双击 `gui_window_mover.exe`

## 注意事项

- 此脚本仅支持Windows系统
- 对于某些系统级应用或具有特殊权限的应用，可能需要以管理员身份运行
- 确保目标程序正在运行，否则无法移动其窗口
- 支持按窗口标题或进程名查找窗口