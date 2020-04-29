import math


class GoldenSectionSearch:
    def __init__(self):
        self.precision = None
        self.a = None
        self.b = None

    def set_parameters(self, a, b, precision):
        """Sets parameters for range values and desired precision"""
        self.a = a
        self.b = b
        self.precision = precision

    def get_extremum(self, f):
        """Gets extremum of given function f"""

        """Golden ratio"""
        k = (math.sqrt(5) - 1) / 2

        x1 = self.a + k * (self.b - self.a)
        x2 = self.b - k * (self.b - self.a)

        while (self.b - self.a) <= 2 * self.precision:
            if f(x1) <= f(x2):
                self.a = self.a
                self.b = x2
                x2 = x1
                x1 = self.a + k * (self.b - self.a)
            elif f(x1) > f(x2):
                b = b
                a = x1
                x1 = x2
                x2 = self.b - k * (self.b - self.a)

        return (self.a + self.b) / 2


gss = GoldenSectionSearch()
gss.set_parameters(-1, 1, 0.001)

f = lambda x: math.exp(x) - x

extremum = gss.get_extremum(f)
print(extremum)

# --- EXAMPLE USAGE ---

# gss = GoldenSectionSearch()             # create directional minimizer object
# gss.set_parameters(-100, 100, 0.001)    # set parameters of directional minimizer
#
# f = lambda x: 3x^2 + 2x                 # test lambda function that is to be minimized
# extremum = gss.get_extremum(f)          # compute extremum
# print(extremum)
