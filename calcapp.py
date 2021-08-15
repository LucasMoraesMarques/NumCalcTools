from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.config import Config
from methods import Bissection, Newton, AproxSuc, evaluate
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
        plt.annotate(f'P({xsol}, {ysol})', xy=(xsol, ysol), xytext=(xsol-0.08, ysol-0.08), fontsize='x-large')

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


class CalcApp(App):
    icon = 'calculating.ico'

    def build(self):
        return CalcLayout()


CalcApp().run()