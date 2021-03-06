from function_handler import FunctionHandler
from msd import SteepestDescentMethod
from gss import GoldenSectionSearch
from pyqt_gui import FunctionOptimizer, QApplication


# example function
func = "sin(x^2 + 3y^2) / (0.1 + sqrt(x^2 + y^2)^2) + (x^2 + 5y^2) * (exp(1 - sqrt(x^2 + y^2)^2) / 2)"
# func = "sin(0.5x^2-0.25y^2+3)*cos(2x+1-e^y)"


# func = "5x^2 + 4y^2 + 3xy + 7x + 20" -5, 5 - ok
# func = "10x^2 + 5xy + 8y^2 - 14x - 6y + 10" 40, -100
# func = "5x^2 + y^2 + 4xy - 14x - 6y + 20" x0 = 0, 10 -    x -3, 3 - y 0, 11   BEST EXAMPLE
func = "(1-x)^2 + 100*(y-x^2)^2"

parser = FunctionHandler()
parser.parse_function(func)
parser.set_mesh_ranges((-1.0, 1.5), (-1.0, 1.5))

gss = GoldenSectionSearch()
gss.set_parameters(-1, 1, 0.000001)

msd = SteepestDescentMethod(gss, parser)
msd.set_function_handler(parser)
msd.set_parameters((-0.5, 0.5), 0.001)

if __name__ == '__main__':
    app = QApplication([])
    gui = FunctionOptimizer(parser=parser, msd=msd)

    gui.text_edit.setPlainText(func)
    gui.fig_canvas.set_data(parser.create_mesh())
    gui.update_figure()

    gui.show()
    app.exec_()
