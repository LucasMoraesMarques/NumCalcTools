import math
from sympy import *
import numpy
def evaluate(equation, **params):
    # Evaluate the equation
    try:
        value = eval(equation, params)
    except Exception as Error:
        print(Error)
        raise SyntaxError
    else:
        return value


params = {'math': math}


def Bissection(equation, a0, b0, x0, error_type, error_value):
    try:
        precision = len(str(error_value).split('.')[1]) + 3

        params['x'] = a0
        fa0 = evaluate(equation, **params)

        params['x'] = b0
        fb0 = evaluate(equation, **params)

        params['x'] = x0
        fx0 = evaluate(equation, **params)
        if fx0 == 0:
            raise Exception('[INPUT ERROR] X0 provided is a solution')

        error = 100
        iterations = 0
        x_values = [x0]
        if fa0 * fb0 < 0:
            while error > error_value:
                params['x'] = a0
                fa0 = evaluate(equation, **params)

                params['x'] = x0
                fx0 = evaluate(equation, **params)

                if fa0 * fx0 < 0:
                    a0 = a0
                    b0 = x0

                else:
                    a0 = x0
                    b0 = b0

                x1 = (a0 + b0) / 2

                if error_type == 'absolute':
                    error = abs(x1 - x0)
                else:
                    error = abs((x1 - x0) / x1)

                iterations += 1
                x_values.append(x1)
                x0 = x1
        else:
            raise Exception('[METHOD ERROR] f(a0) * f(b0) >= 0')
    except (SyntaxError, ValueError) as Error:
        return "[SYNTAX ERROR] Please follow the syntax rules", None, None
    except Exception as Error:
        return Error.__str__(), None, None
    else:
        xsol = round(x1, precision)
        params['x'] = x0
        fx0 = evaluate(equation, **params)
        fx0 = round(fx0, precision)
        if len(x_values) > 5:
            x_values = x_values[:5]
        return f'x = {xsol}, com {iterations + 1} iterações e erro {error_type} menor que E = {error_value}' \
               f'\n First x values: {list(map(lambda x: round(x, precision), x_values))}', xsol, fx0


def Newton(equation, a0, b0, x0, error_type, error_value):
    try:
        precision = len(str(error_value).split('.')[1]) + 3
        error = 100
        iterations = 0
        x_values = []

        params['x'] = x0
        fx0 = sympify(equation).evalf(subs={symbols('x'): x0, symbols('e'): E})
        f_diff = diff(sympify(equation), symbols('x'))
        fx0_diff = sympify(f_diff).evalf(subs={symbols('x'): x0, symbols('e'): E})

        if fx0_diff == 0:
            raise Exception("[METHOD ERROR] f'(x0) = 0")

        while error > error_value:
            params['x'] = x0
            fx0 = sympify(equation).evalf(subs={symbols('x'):x0, symbols('e'): E})
            f_diff = diff(sympify(equation), symbols('x'))
            fx0_diff = sympify(f_diff).evalf(subs={symbols('x'):x0, symbols('e'): E})

            x1 = x0 - fx0/fx0_diff

            if error_type == 'absolute':
                error = abs(x1 - x0)
            else:
                error = abs((x1 - x0) / x1)

            iterations += 1
            x_values.append(x0)
            x0 = x1
    except (SyntaxError, ValueError) as Error:
        return "[SYNTAX ERROR] Please follow the syntax rules", None, None
    except Exception as Error:
        return Error.__str__(), None, None
    else:
        xsol = round(x1, precision)
        params['x'] = x0
        fx0 = sympify(equation).evalf(subs={symbols('x'): x0, symbols('e'): E})
        fx0 = round(fx0, precision)
        if len(x_values) > 5:
            x_values = x_values[:5]
        return f'x = {xsol}, com {iterations + 1} iterações e erro {error_type} menor que E = {error_value}' \
               f'\n First x values: {list(map(lambda x: round(x, precision), x_values))}', xsol, fx0


def AproxSuc(equation,a0, b0, x0, error_type, error_value):
    try:
        precision = len(str(error_value).split('.')[1]) + 3
        values = [ ]
        error = 100
        iterations = 0
        while error > error_value:
            params['x'] = x0
            x1 = evaluate(equation, **params)
            values.append(x1)
            if error_type == 'absolute':
                error = abs(x1 - x0)
            else:
                error = abs((x1 - x0) / x1)

            if len(values) > 2 and abs(values[-1] - values[-2]) > abs(b0 - a0) or len(values) > 200:
                raise Exception('[METHOD ERROR] Values not converging to a solution')
            iterations += 1
            x0 = x1
    except (SyntaxError, ValueError) as Error:
        return "[SYNTAX ERROR] Please follow the syntax rules", None, None
    except Exception as Error:
        return Error.__str__(), None, None
    else:
        params['x'] = x1
        fx1 = evaluate(equation, **params) - x1
        xsol = round(x1, precision) # TODO
        fx1 = round(fx1, precision)
        if len(values) > 5:
            values = values[:5]
        return f'x = {xsol}, com {iterations + 1} iterações e erro {error_type} menor que E = {error_value}' \
               f'\n First x values: {list(map(lambda x: round(x, precision), values))}', xsol, fx1


x = [1970, 1980, 1990, 2000]
y = [3710, 4450, 5280, 6080]

def NewtonsPolynomio(x, y, x0):
    coeficients = [y[0]]
    polynomio = ''
    for i in range(0,len(x)-1):
        lista = []
        for j in range(1, len(y)):
            lista.append((y[j]-y[j-1])/(x[j+i]-x[j-1]))
            print(lista)
        y = [round(i, 8) for i in lista]
        coeficients.append(lista[0])
    coeficients = [round(i, 8) for i in coeficients]

    for i in range(len(x)):
        if i == 0:
            polynomio += f'{coeficients[i]}+'
        else:
            polynomio += f'{coeficients[i]}'
        for value in x[:i]:
            if value == 0:
                polynomio += f'*(x)'
            else:
                polynomio += f'*(x+{-1*value})'
        if i != len(x) - 1:
            polynomio += '+'

    while '+-' in polynomio:
        polynomio = polynomio.replace('+-', '-')

    while '++' in polynomio:
        polynomio = polynomio.replace('++', '+')

    print(polynomio)
    y0 = sympify(polynomio).evalf(subs={symbols('x'): x0})

    return f"Polynomio: {polynomio}\n" \
           f"P({x0}) = {round(y0, 8)}", polynomio, x, x0, y0


def PolynomioInterpolator(x, y, x0=0):
    coeff_matrix = []
    polynomio = ''
    for i in range(len(x)):
        coeff_matrix.append([x[i]**j for j in range(len(x))])
    print(coeff_matrix)
    sol = numpy.linalg.solve(coeff_matrix, y)
    for i in range(len(x)):
        polynomio += f'+{round(sol[i],8)}*x**{i}'
    while '+-' in polynomio:
        polynomio = polynomio.replace('+-', '-')

    while '++' in polynomio:
        polynomio = polynomio.replace('++', '+')
    y0 = sympify(polynomio).evalf(subs={symbols('x'): x0})
    return f"Polynomio: {polynomio}\n" \
           f"P({x0}) = {round(y0, 8)}", polynomio, x, x0, y0

print(NewtonsPolynomio(x, y, 1985))