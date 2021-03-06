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
        self.isolines = []

        self.steps_x, self.steps_y = None, None

    def set_data(self, data):
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]

    def set_levels(self, value):
        self.levels = value
        self.update_canvas()

    def set_points(self, points):
        self.steps_x = [p[0] for p in points]
        self.steps_y = [p[1] for p in points]

    def set_isolines(self, isolines):
        self.isolines = isolines

    def set_plot_type(self, toggled, plot_type):
        if not toggled:
            return

        if plot_type == 1:
            self.plot_type = 'contour'
        elif plot_type == 2:
            self.plot_type = 'contourf'
        elif plot_type == 3:
            self.plot_type = 'isolines'

        self.update_canvas()

    def update_canvas(self):
        self.figure.clear()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Wykres funkcji f(x, y)')

        if self.plot_type == 'contourf':
            cp = plt.contourf(self.x, self.y, self.z, levels=self.levels)
            plt.colorbar(cp)
        elif self.plot_type == 'contour':
            cp = plt.contour(self.x, self.y, self.z, colors='black', levels=self.levels, linewidths=0.1)
        elif self.plot_type == 'isolines':
            # cp = plt.contour(self.x, self.y, self.z, colors='black', levels=self.levels, linewidths=0.1)
            # cp = plt.contour(self.x, self.y, self.z, colors='black', levels=[i for i in range(2000)], linewidths=0.1)
            if len(self.isolines) > 0:
                print("Iso", self.isolines)
                cp = plt.contour(self.x, self.y, self.z, colors='black', levels=self.isolines, linewidths=0.1)
            else:
                cp = plt.contour(self.x, self.y, self.z, colors='black', levels=self.levels, linewidths=0.1)

        scat = None
        if self.steps_x is not None and self.steps_y is not None:
            print(self.steps_x, self.steps_y)
            scat = plt.scatter(self.steps_x, self.steps_y, s=[2 for _ in range(len(self.steps_y))])
            plt.plot(self.steps_x, self.steps_y, linewidth=1)

        self.draw()
        if scat is not None:
            scat.remove()


class FunctionOptimizer(QDialog):
    def __init__(self, parser=None, msd=None, parent=None):
        super(FunctionOptimizer, self).__init__(parent)
        self.setWindowTitle("Metody optymalizacji")
        QApplication.setStyle(QStyleFactory.create('windows'))

        self.parser = parser
        self.msd = msd

        self.create_parser_box()
        self.create_plot_box()
        self.create_function_info()

        main_layout = QGridLayout()
        fig = plt.figure(dpi=140)

        self.fig_canvas = Plot3D(fig)
        main_layout.addWidget(self.fig_canvas, 0, 0, 3, 1)
        main_layout.addWidget(self.parser_group_box, 0, 1)
        main_layout.addWidget(self.plot_group_box, 1, 1)
        main_layout.addWidget(self.info_group_box, 2, 1)
        self.setLayout(main_layout)

    def create_parser_box(self):
        self.parser_group_box = QGroupBox("Parser")

        self.text_edit = QTextEdit()
        button = QPushButton("Parsuj")
        button.clicked.connect(lambda: self.update_function())

        start_point_layout = QGridLayout()
        self.x1, self.x2 = QLineEdit('-0.5'), QLineEdit('0.5')
        start_point_layout.addWidget(self.x1, 0, 0)
        start_point_layout.addWidget(self.x2, 0, 1)
        start_point_box = QGroupBox("Punkt startowy")
        start_point_box.setLayout(start_point_layout)

        main_precision_layout = QGridLayout()
        self.p1 = QLineEdit('0.001')
        main_precision_layout.addWidget(self.p1)
        main_precision_box = QGroupBox("Precyzja")
        main_precision_box.setLayout(main_precision_layout)

        dir_precision_layout = QGridLayout()
        self.p2 = QLineEdit('0.000001')
        dir_precision_layout.addWidget(self.p2)
        dir_precision_box = QGroupBox("Prec. kier.")
        dir_precision_box.setLayout(dir_precision_layout)

        algorithm_details = QGridLayout()

        algorithm_details.addWidget(start_point_box, 0, 0, 1, 2)
        algorithm_details.addWidget(main_precision_box, 1, 0)
        algorithm_details.addWidget(dir_precision_box, 1, 1)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(button)
        layout.addLayout(algorithm_details)

        self.parser_group_box.setLayout(layout)

    def create_plot_box(self):
        self.plot_group_box = QGroupBox("Szczegóły wykresu")
        self.plot_group_box.setContentsMargins(2, 18, 2, 2)

        # set type of plot
        checkbox_iso = QRadioButton("&Linie")
        checkbox_iso.setChecked(True)
        checkbox_color = QRadioButton("&Kolory")
        checkbox_3 = QRadioButton('&Izolinie')
        checkbox_iso.toggled.connect(lambda x: self.fig_canvas.set_plot_type(x, 1))
        checkbox_color.toggled.connect(lambda x: self.fig_canvas.set_plot_type(x, 2))
        checkbox_3.toggled.connect(lambda x: self.fig_canvas.set_plot_type(x, 3))

        levels_slider = QSlider(Qt.Horizontal)
        levels_slider.setValue(20)
        levels_slider.setRange(5, 50)
        levels_slider.valueChanged.connect(lambda x: self.fig_canvas.set_levels(x))

        type_group_layout = QHBoxLayout()
        type_group_layout.addWidget(checkbox_iso)
        type_group_layout.addWidget(checkbox_color)
        type_group_layout.addWidget(checkbox_3)
        type_group_layout.addWidget(levels_slider)

        type_group = QGroupBox('Rodzaj wykresu')
        type_group.setLayout(type_group_layout)

        # set plot details
        self.x1_start_range, self.x1_end_range, self.x2_start_range, self.x2_end_range = QLineEdit('-10'), QLineEdit('10'), QLineEdit('-5'), QLineEdit('5')
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

    def create_function_info(self):
        self.info_group_box = QGroupBox("Wyniki")

        self.no_steps = QLabel('Liczba kroków: ...')
        self.found_arg = QLabel('Minimum w: (..., ...)')
        self.found_val = QLabel('Wartość minimum: ...')

        layout = QVBoxLayout()
        layout.addWidget(self.no_steps)
        layout.addWidget(self.found_arg)
        layout.addWidget(self.found_val)

        self.info_group_box.setLayout(layout)

    def update_range(self):
        try:
            x1 = (float(self.x1_start_range.text()), float(self.x1_end_range.text()))
            x2 = (float(self.x2_start_range.text()), float(self.x2_end_range.text()))
        except ValueError:
            print("Bad range values!")
            return
        self.parser.set_mesh_ranges(x1, x2)
        self.fig_canvas.set_data(self.parser.create_mesh())
        self.update_figure()

    def update_function(self, data=None):
        func_to_parse = self.text_edit.toPlainText()
        self.parser.parse_function(func_to_parse)

        if data is not None:
            self.parser.set_mesh_ranges(data[0], data[1])

        self.msd.set_parameters((float(self.x1.text()), float(self.x2.text())), float(self.p1.text()))

        self.msd.compute()
        self.fig_canvas.set_points(self.msd.get_steps())
        self.fig_canvas.set_isolines(self.msd.get_isolines())

        self.fig_canvas.set_data(self.parser.create_mesh())
        self.update_figure()

        n, arg, val = self.msd.get_results()
        self.no_steps.setText(f'Liczba krokow: <b>{n-1}</b>')
        self.found_arg.setText(f'Minimum w: <b>({round(arg[0], 5)}, {round(arg[1], 5)})</b>')
        self.found_val.setText(f'Minimum: <b>{round(val, 5)}</b>')

    def update_figure(self):
        self.fig_canvas.update_canvas()
