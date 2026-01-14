import threading
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'window_mover'))

from move_window import move_exe_to_position


class WindowMoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("窗口移动工具")
        self.root.geometry("500x500")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 目标窗口名称输入
        ttk.Label(main_frame, text="目标窗口名称/进程名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.target_var = tk.StringVar()
        self.target_entry = ttk.Entry(main_frame, textvariable=self.target_var, width=30)
        self.target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.target_entry.insert(0, "skyrim")  # 默认值
        
        # X坐标输入
        ttk.Label(main_frame, text="X 坐标:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.x_var = tk.IntVar(value=200)
        self.x_entry = ttk.Entry(main_frame, textvariable=self.x_var, width=30)
        self.x_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Y坐标输入
        ttk.Label(main_frame, text="Y 坐标:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.y_var = tk.IntVar(value=200)
        self.y_entry = ttk.Entry(main_frame, textvariable=self.y_var, width=30)
        self.y_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 宽度输入
        ttk.Label(main_frame, text="宽度:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.IntVar(value=800)
        self.width_entry = ttk.Entry(main_frame, textvariable=self.width_var, width=30)
        self.width_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 高度输入
        ttk.Label(main_frame, text="高度:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.height_var = tk.IntVar(value=600)
        self.height_entry = ttk.Entry(main_frame, textvariable=self.height_var, width=30)
        self.height_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 使用默认尺寸复选框
        self.use_default_size = tk.BooleanVar(value=True)
        self.default_size_check = ttk.Checkbutton(
            main_frame, 
            text="使用窗口原始尺寸", 
            variable=self.use_default_size,
            command=self.toggle_size_fields
        )
        self.default_size_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 预设按钮区域
        presets_label = ttk.Label(main_frame, text="快速预设:")
        presets_label.grid(row=6, column=0, sticky=tk.W, pady=(15, 5))
        
        presets_frame = ttk.Frame(main_frame)
        presets_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=(15, 5), padx=(10, 0))
        presets_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        ttk.Button(presets_frame, text="记事本", command=lambda: self.load_preset("notepad.exe", 100, 100, 800, 600)).grid(row=0, column=0, padx=2)
        ttk.Button(presets_frame, text="计算器", command=lambda: self.load_preset("calc.exe", 500, 100, 400, 500)).grid(row=0, column=1, padx=2)
        ttk.Button(presets_frame, text="画图", command=lambda: self.load_preset("mspaint.exe", 200, 200, 1000, 800)).grid(row=0, column=2, padx=2)
        ttk.Button(presets_frame, text="CMD", command=lambda: self.load_preset("cmd.exe", 100, 100, 600, 400)).grid(row=0, column=3, padx=2)
        
        # 移动按钮
        self.move_button = ttk.Button(main_frame, text="移动窗口", command=self.move_window_threaded)
        self.move_button.grid(row=7, column=0, columnspan=2, pady=20)
        
        # 结果显示区域
        self.result_text = tk.Text(main_frame, height=8, width=50)
        self.result_text.grid(row=8, column=0, columnspan=2, pady=10)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=8, column=2, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 初始化禁用尺寸字段
        self.toggle_size_fields()
        
    def toggle_size_fields(self):
        """根据复选框状态启用/禁用尺寸字段"""
        state = "disabled" if self.use_default_size.get() else "normal"
        self.width_entry.config(state=state)
        self.height_entry.config(state=state)
    
    def load_preset(self, target, x, y, width, height):
        """加载预设配置"""
        self.target_var.set(target)
        self.x_var.set(x)
        self.y_var.set(y)
        self.width_var.set(width)
        self.height_var.set(height)
        self.use_default_size.set(False)  # 确保尺寸字段可用
        self.toggle_size_fields()
    
    def move_window_threaded(self):
        """在单独线程中执行窗口移动以避免UI冻结"""
        thread = threading.Thread(target=self.move_window)
        thread.daemon = True
        thread.start()
    
    def move_window(self):
        """执行窗口移动操作"""
        try:
            target = self.target_var.get()
            x = self.x_var.get()
            y = self.y_var.get()
            
            # 根据复选框决定是否使用默认尺寸
            if self.use_default_size.get():
                width = None
                height = None
            else:
                width = self.width_var.get()
                height = self.height_var.get()
            
            # 清空结果文本框
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"正在查找并移动窗口: {target}\n")
            self.result_text.update()
            
            # 执行移动操作
            move_exe_to_position(target, x, y, width, height)
            
            self.result_text.insert(tk.END, f"\n操作完成！窗口已移动到 ({x}, {y})")
            
        except ValueError as e:
            error_msg = f"输入错误: {str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, error_msg)
            messagebox.showerror("输入错误", error_msg)
        except Exception as e:
            error_msg = f"操作失败: {str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, error_msg)
            messagebox.showerror("错误", error_msg)


def main():
    root = tk.Tk()
    app = WindowMoverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()