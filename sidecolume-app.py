import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SidebarApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Math Function Teaching App")
        self.geometry("1000x600")

        # 創建主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 創建側邊欄
        sidebar = ttk.Frame(main_frame, width=200, relief="raised", borderwidth=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # 創建內容區
        self.content = ttk.Frame(main_frame)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 定義頁面
        self.pages = {
            "Home": HomePage,
            "Math Functions": MathFunctionsPage,
            "Frame 2": Frame2
        }

        # 創建側邊欄按鈕
        for page_name in self.pages:
            ttk.Button(sidebar, text=page_name, command=lambda name=page_name: self.show_frame(name)).pack(fill=tk.X, padx=5, pady=5)

        # 創建不同的框架
        self.frames = {}
        for page_name, F in self.pages.items():
            frame = F(self.content, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        if page_name in self.frames:
            frame = self.frames[page_name]
            frame.tkraise()
        else:
            print(f"Error: {page_name} is not a valid page name")

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text="Welcome to the Math Function Teaching App")
        label.pack(pady=10, padx=10)

class MathFunctionsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 創建一個Notebook來組織不同的函數
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 定義函數和它們的參數
        self.functions = {
            "Linear": (lambda x, a, b: a * x + b, {"a": 1, "b": 0}),
            "Quadratic": (lambda x, a, b, c: a * x**2 + b * x + c, {"a": 1, "b": 0, "c": 0}),
            "Sine": (lambda x, a, b, c: a * np.sin(b * x + c), {"a": 1, "b": 1, "c": 0}),
            "Exponential": (lambda x, a, b: a * np.exp(b * x), {"a": 1, "b": 1}),
            "Logarithmic": (lambda x, a, b: a * np.log(x) + b, {"a": 1, "b": 0})
        }

        # 為每個函數創建一個標籤頁
        for func_name, (func, params) in self.functions.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=func_name)
            self.create_function_tab(frame, func_name, func, params)

    def create_function_tab(self, parent, func_name, func, params):
        # 創建參數調整區
        param_frame = ttk.Frame(parent)
        param_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        param_vars = {}
        for param, value in params.items():
            ttk.Label(param_frame, text=f"{param}:").pack()
            var = tk.DoubleVar(value=value)
            ttk.Entry(param_frame, textvariable=var, width=10).pack()
            param_vars[param] = var

        # 創建繪圖區
        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 更新函數
        def update_plot():
            ax.clear()
            x = np.linspace(-10, 10, 1000)
            current_params = {k: v.get() for k, v in param_vars.items()}
            y = func(x, **current_params)
            ax.plot(x, y)
            ax.set_title(func_name)
            ax.grid(True)
            canvas.draw()

        # 創建更新按鈕
        ttk.Button(param_frame, text="Update Plot", command=update_plot).pack(pady=10)

        # 初始繪圖
        update_plot()

class Frame2(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text="This is Frame 2")
        label.pack(pady=10, padx=10)

if __name__ == "__main__":
    app = SidebarApp()
    app.mainloop()