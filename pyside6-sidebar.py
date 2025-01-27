import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MathPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("數學函數繪圖應用")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        # 側邊欄
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #f0f0f0;")
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(200)

        functions = [
            ("正弦函數", lambda x: np.sin(x)),
            ("餘弦函數", lambda x: np.cos(x)),
            ("指數函數", lambda x: np.exp(x)),
            ("拋物線", lambda x: x**2),
            ("對數函數", lambda x: np.log(np.abs(x)))
        ]

        for name, func in functions:
            button = QPushButton(name)
            button.clicked.connect(lambda checked, f=func, n=name: self.update_plot(f, n))
            sidebar_layout.addWidget(button)

        # 用戶輸入
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("輸入 x 的範圍，例如: -10,10")
        sidebar_layout.addWidget(self.input_field)

        sidebar_layout.addStretch()

        # 主內容區域（圖形）
        content = QWidget()
        content_layout = QVBoxLayout()
        content.setLayout(content_layout)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        content_layout.addWidget(self.canvas)

        layout.addWidget(sidebar)
        layout.addWidget(content)

        self.current_func = None
        self.current_name = ""

    def update_plot(self, func, name):
        self.current_func = func
        self.current_name = name
        self.plot()

    def plot(self):
        if not self.current_func:
            return

        x_range = self.input_field.text().strip().split(',')
        try:
            x_min, x_max = map(float, x_range)
        except ValueError:
            x_min, x_max = -10, 10

        x = np.linspace(x_min, x_max, 1000)
        y = self.current_func(x)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_title(self.current_name)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathPlotter()
    window.show()
    sys.exit(app.exec())