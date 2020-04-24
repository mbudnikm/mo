from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QCheckBox, QStyleFactory, QTextEdit, QPushButton, \
    QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QLineEdit, QLabel, QSlider
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt


class Plot3D(FigureCanvas):
    def __init__(self, fig):
        self.figure = fig
        FigureCanvas.__init__(self, self.figure)

        self.x, self.y, self.z = None, None, None

        self.plot_type = 'contour'
        self.levels = 20

    def set_data(self, data):
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]

    def set_levels(self, value):
        self.levels = value
        self.update_canvas()

    def set_plot_type(self, plot_type):
        if plot_type is True:
            self.plot_type = 'contourf'
        else:
            self.plot_type = 'contour'

        self.update_canvas()

    def update_canvas(self):
        self.figure.clear()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Wykres funkcji f(x, y)')

        if self.plot_type == 'contourf':
            cp = plt.contourf(self.x, self.y, self.z, levels=self.levels)
            plt.colorbar(cp)
        else:
            cp = plt.contour(self.x, self.y, self.z, colors='black', levels=self.levels, linewidths=0.1)

        self.draw()


class FunctionOptimizer(QDialog):
    def __init__(self, parser=None, parent=None):
        super(FunctionOptimizer, self).__init__(parent)
        self.setWindowTitle("Metody optymalizacji")
        QApplication.setStyle(QStyleFactory.create('windows'))

        self.parser = parser

        self.create_parser_box()
        self.create_plot_box()

        main_layout = QGridLayout()
        fig = plt.figure(dpi=100)

        self.fig_canvas = Plot3D(fig)
        main_layout.addWidget(self.fig_canvas, 0, 0, 2, 1)
        main_layout.addWidget(self.parser_group_box, 0, 1)
        main_layout.addWidget(self.plot_group_box, 1, 1)
        self.setLayout(main_layout)

    def create_parser_box(self):
        self.parser_group_box = QGroupBox("Parser")

        self.text_edit = QTextEdit()
        button = QPushButton("Parsuj")
        button.clicked.connect(lambda: self.update_function())

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(button)

        self.parser_group_box.setLayout(layout)

    def create_plot_box(self):
        self.plot_group_box = QGroupBox("Szczegóły wykresu")
        self.plot_group_box.setContentsMargins(2, 18, 2, 2)

        # set type of plot
        checkbox_iso = QRadioButton("&Izolinie")
        checkbox_iso.setChecked(True)
        checkbox_color = QRadioButton("&Kolory")
        checkbox_color.toggled.connect(lambda x: self.fig_canvas.set_plot_type(x))

        levels_slider = QSlider(Qt.Horizontal)
        levels_slider.setValue(20)
        levels_slider.setRange(5, 30)
        levels_slider.valueChanged.connect(lambda x: self.fig_canvas.set_levels(x))

        type_group_layout = QHBoxLayout()
        type_group_layout.addWidget(checkbox_iso)
        type_group_layout.addWidget(checkbox_color)
        type_group_layout.addWidget(levels_slider)

        type_group = QGroupBox('Rodzaj wykresu')
        type_group.setLayout(type_group_layout)

        # set plot details
        self.x1_start_range, self.x1_end_range, self.x2_start_range, self.x2_end_range = QLineEdit('-10'), QLineEdit('10'), QLineEdit('-10'), QLineEdit('10')
        lab1, lab2 = QLabel("-"), QLabel("-")

        # X ranges
        x1_layout = QGridLayout()
        x1_layout.addWidget(self.x1_start_range, 0, 0)
        x1_layout.addWidget(lab1, 0, 1)
        x1_layout.addWidget(self.x1_end_range, 0, 2)
        x1_box = QGroupBox("X")
        x1_box.setContentsMargins(2, 10, 2, 2)
        x1_box.setLayout(x1_layout)

        # Y ranges
        x2_layout = QGridLayout()
        x2_layout.addWidget(self.x2_start_range, 0, 0)
        x2_layout.addWidget(lab2, 0, 1)
        x2_layout.addWidget(self.x2_end_range, 0, 2)
        x2_box = QGroupBox("Y")
        x2_box.setContentsMargins(2, 10, 2, 2)
        x2_box.setLayout(x2_layout)

        ranges_layout = QGridLayout()
        ranges_layout.addWidget(x1_box)
        ranges_layout.addWidget(x2_box)
        button = QPushButton('Zmień zakres')
        button.clicked.connect(self.update_range)
        ranges_layout.addWidget(button)

        domain_group = QGroupBox('Zakres dziedziny wykresu')
        domain_group.setContentsMargins(2, 10, 2, 2)
        domain_group.setLayout(ranges_layout)

        # MAIN LAYOUT
        grid_layout = QGridLayout()
        grid_layout.addWidget(type_group, 0, 0)
        grid_layout.addWidget(domain_group, 1, 0)

        self.plot_group_box.setLayout(grid_layout)

    def update_range(self):
        x1 = (float(self.x1_start_range.text()), float(self.x1_end_range.text()))
        x2 = (float(self.x2_start_range.text()), float(self.x2_end_range.text()))
        self.parser.set_mesh_ranges(x1, x2)
        self.fig_canvas.set_data(self.parser.create_mesh())
        self.update_figure()

    def update_function(self, data=None):
        func_to_parse = self.text_edit.toPlainText()
        self.parser.parse_function(func_to_parse)

        if data is not None:
            self.parser.set_mesh_ranges(data[0], data[1])

        self.fig_canvas.set_data(self.parser.create_mesh())
        self.update_figure()

    def update_figure(self):
        self.fig_canvas.update_canvas()