import math
from sympy import *


def evaluate(equation, **params):
    # Evaluate the equation
    try:
        value = eval(equation, params)
    except Exception as Error:
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

        error = 100
        iterations = 0
        if fa0 * fb0 < 0:
            while error > error_value:
                params['x'] = a0
                fa0 = evaluate(equation, **params)

                params['x'] = x0
                fx0 = evaluate(equation, **params)
                if fx0 == 0:
                    raise Exception('[INPUT ERROR] X0 provided is a solution') # TODO

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
                x0 = x1
        else:
            raise Exception('[METHOD ERROR] f(a0) * f(b0) >= 0')
    except (SyntaxError, ValueError) as Error:
        return "[SYNTAX ERROR] Please follow the syntax rules", None, None
    except Exception as Error:
        return Error.__str__(), None, None
    else:
        xsol = round(x1, precision)
        fx0 = round(fx0, precision)
        return f'x = {xsol}, com {iterations + 1} iterações e erro {error_type} menor que E = {error_value}', xsol, fx0


def Newton(equation, a0, b0, x0, error_type, error_value):
    try:
        precision = len(str(error_value).split('.')[1]) + 3
        error = 100
        iterations = 0

        while error > error_value:
            params['x'] = x0
            fx0 = sympify(equation).evalf(subs={symbols('x'):x0, symbols('e'): E})
            f_diff = diff(sympify(equation), symbols('x'))
            fx0_diff = sympify(f_diff).evalf(subs={symbols('x'):x0, symbols('e'): E})
            if fx0_diff == 0:
                raise Exception("[METHOD ERROR] f'(x0) = 0")  # TODO

            x1 = x0 - fx0/fx0_diff

            if error_type == 'absolute':
                error = abs(x1 - x0)
            else:
                error = abs((x1 - x0) / x1)

            iterations += 1
            x0 = x1
    except (SyntaxError, ValueError) as Error:
        return "[SYNTAX ERROR] Please follow the syntax rules", None, None
    except Exception as Error:
        return Error.__str__(), None, None
    else:
        xsol = round(x1, precision)
        fx0 = round(fx0, precision)
        return f'x = {xsol}, com {iterations + 1} iterações e erro {error_type} menor que E = {error_value}', xsol, fx0


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

            if len(values) > 2 and abs(values[-1] - values[-2]) > abs(b0 - a0):
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
        return f'x = {xsol}, com {iterations + 1} iterações e erro {error_type} menor que E = {error_value}', xsol, fx1


