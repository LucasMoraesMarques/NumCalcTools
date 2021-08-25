from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.config import Config
from methods import Bissection, Newton, AproxSuc, evaluate, NewtonsPolynomio, PolynomioInterpolator
import numpy as np
import math
import matplotlib.pyplot as plt
import re
Config.set('graphics', 'resizable', 1)
Config.write()


class CalcLayout(Widget):

    def __init__(self, **kwargs):
        super(CalcLayout, self).__init__(**kwargs)
        self.figId = 0
        plt.style.use('seaborn')

    def run(self, method, equation, x0, lower_limit, higher_limit, error):
        xsol = None
        ysol = None
        if method=='Métodos' or not equation or not x0 or not lower_limit or not higher_limit or not error:
            result_text = 'Please provide all inputs'
        else:
            equation = self.parseEquation(equation)
            eqStr = self.ids.input.text
            self.method = method
            if self.ids.abs_error.active:
                error_type = 'absolute'
            else:
                error_type = 'relative'

            if method == 'Bisseção':
                result_text, xsol, ysol = Bissection(equation,
                                                   float(lower_limit),
                                                   float(higher_limit),
                                                   float(x0),
                                                   error_type,
                                                   float(error)
                                                    )

            elif method == 'Aproximações \nSucessivas':
                result_text, xsol, ysol = AproxSuc(equation,
                                                   float(lower_limit),
                                                   float(higher_limit),
                                                   float(x0),
                                                   error_type,
                                                   float(error)
                                                     )
                eqStr +=  '- x'
            elif method == 'Newton':
                result_text, xsol, ysol = Newton(eqStr,
                                                 float(lower_limit),
                                                 float(higher_limit),
                                                 float(x0),
                                                 error_type,
                                                 float(error)
                                                 )
            elif method == "Newton's Polynomio":
                x = [float(i) for i in lower_limit.split(',')]
                y = [float(i) for i in higher_limit.split(',')]
                result_text, polynomio, x, x0, y0 = NewtonsPolynomio(x, y, x0)
                self.ids.result_box.add_widget(
                    Label(text=result_text,
                          color=(0, 1, 0, 1),
                          font_size=15,
                          size_hint=(1, None),
                          height=40,
                          pos_hint={'top': 1}
                          ))
                self.generatePlot(polynomio, polynomio, float(x0), float(y0), x[0], x[-1])
                self.ids.plot.source = f'figure{self.figId}.png'
                self.figId += 1
            elif method == 'Polynomial Interpolation':
                x = [float(i) for i in lower_limit.split(',')]
                y = [float(i) for i in higher_limit.split(',')]
                result_text, polynomio, x, x0, y0 = PolynomioInterpolator(x, y, x0)
                self.ids.result_box.add_widget(
                    Label(text=result_text,
                          color=(0, 1, 0, 1),
                          font_size=15,
                          size_hint=(1, None),
                          height=40,
                          pos_hint={'top': 1}
                          ))
                self.generatePlot(polynomio, polynomio, float(x0), float(y0), x[0], x[-1])
                self.ids.plot.source = f'figure{self.figId}.png'
                self.figId += 1

        if xsol != None and ysol != None:
            self.generatePlot(equation, eqStr, xsol, ysol, lower_limit, higher_limit)
            self.ids.plot.source = f'figure{self.figId}.png'
            self.figId += 1
            self.ids.input.hint_text = 'Digite a equação no formato do método.'
            self.ids.result_box.add_widget(
                Label(text=result_text,
                      color=(0, 1, 0, 1),
                      font_size=15,
                      size_hint=(1, None),
                      height=40,
                      pos_hint={'top': 1}
                      )
            )
        elif method in ["Newton's Polynomio", 'Polynomial Interpolation']:
            pass
        else:
            self.ids.result_box.add_widget(
                Label(text=result_text,
                      color=(1, 0, 0, 1),
                      font_size=15,
                      size_hint=(1, None),
                      height=40,
                      pos_hint={'top': 1}
                      )
            )

    def parseEquation(self, equation):
        for op in ['e', 'log', 'ln', '√', 'sin', 'cos', 'tan', 'π', '^']:
            if op in equation and op != 'ln' and op != "^":
                equation = equation.replace(op, f'math.{op}')
            if op == 'ln':
                equation = re.sub(r'ln\((?P<inp>.*?)\)', r'math.log(\g<inp>,math.e)', equation)
            if op == "^":
                equation = equation.replace("^", "**")
        return equation

    def generatePlot(self, equation, eqStr, xsol, ysol, lower_limit, higher_limit):
        print(equation)
        lower_limit = float(lower_limit)
        higher_limit = float(higher_limit)
        step = abs(higher_limit-lower_limit)/100
        x = np.arange(lower_limit, higher_limit, step)
        y = []
        if self.method == 'Aproximações \nSucessivas':
            equation += '-x'
        for xval in x:
            params = {'math': math, 'x': xval}
            yval = evaluate(equation, **params)
            y.append(yval)

        plt.title(f"Plot for {eqStr} in [{lower_limit}, {higher_limit}]", fontsize='xx-large')
        plt.ylabel('Y')
        plt.xlabel('X')
        plt.plot(x, y)
        plt.plot(xsol, ysol, marker='o', color='r')
        plt.annotate(f'P({xsol}, {ysol})', xy=(xsol, ysol), xytext=(xsol, ysol), fontsize='x-large')

        plt.savefig(f'figure{self.figId}.png')
        plt.clf()

    def updateInput(self, op):
        prior = self.ids.input.text
        if op not in ['=', 'CE', 'C', '+/-', 'RUN']:
            if prior in ['0', '0.0']:
                prior = ''
            current = prior + op
        elif op == '+/-':
            if '-' in prior:
                current = prior.replace('-', '+')
            else:
                current = '-' + prior
        else:
            current = prior
        self.ids.input.text = current

    def delete(self):
        self.ids.input.text = self.ids.input.text[0:-1]

    def clearInput(self):
        self.ids.input.text = '0'

    def updateDisplay(self, method):
        if method in ["Newton's Polynomio", 'Polynomial Interpolation']:

            self.ids.err_box.size_hint_x = None
            self.ids.err_box.width = 0
            self.ids.err_box.opacity = 0

            self.ids.input.size_hint = None, None
            self.ids.input.height = 0
            self.ids.input.width = 0
            self.ids.input.text = 'x+1'

            self.ids.lower_limit.hint_text = 'Digite os valores de x separados por ,'
            self.ids.higher_limit.hint_text = 'Digite os valores de y separados por ,'
            self.ids.initial_value.hint_text = 'Digite o ponto para aproximação'
            self.ids.error.size_hint_y = None
            self.ids.error.height = 0
            self.ids.error.text = '0.1'
        else:
            self.ids.err_box.size_hint_x = 0.2
            self.ids.err_box.opacity = 1

            self.ids.input.size_hint = (0.8, 1)
            self.ids.input.text = ''

            self.ids.lower_limit.hint_text = 'Limite inferior do intervalo'
            self.ids.higher_limit.hint_text = 'Limite superior do intervalo'
            self.ids.initial_value.hint_text = 'Valor inicial de busca'
            self.ids.error.size_hint_y = 0.2
            self.ids.error.text = ''
            self.ids.error.hint_text = 'Erro percentual(0-1)'

class CalcApp(App):
    icon = 'calculating.ico'

    def build(self):
        return CalcLayout()


CalcApp().run()