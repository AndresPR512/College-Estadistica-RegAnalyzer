import numpy as np

class RegressionEngine:
    def fit_all(self, x, y):
        results = {}

        try:
            results["Linear"] = self._fit_linear(x, y)
        except Exception:
            pass

        if np.all(y > 0):
            try:
                results["Exponential"] = self._fit_exponential(x, y)
            except Exception:
                pass

        if np.all(x > 0):
            try:
                results["Logarithmic"] = self._fit_logarithmic(x, y)
            except Exception:
                pass

        try:
            results["Quadratic"] = self._fit_quadratic(x, y)
        except Exception:
            pass

        if np.all(x > 0) and np.all(y > 0):
            try:
                results["Power"] = self._fit_power(x, y)
            except Exception:
                pass
        
        return results

    # Ajuste de regresión lineal
    def _fit_linear(self, x, y):
        b, a = np.polyfit(x, y, 1)
        
        y_pred = a + b * x
        r2, adjusted_r2, standard_error, press, predicted_r2 = self._compute_all_metrics(x, y, y_pred, 2, self._linear_fit_predict)
        r = np.corrcoef(x, y)[0, 1]
                
        return {
            "a": a, "b": b, "r": r,
            "r2": r2, "adjusted_r2": adjusted_r2,
            "standard_error": standard_error, "press": press,
            "predicted_r2": predicted_r2,
            "equation": rf"y = {a:.4f} {self._latex_term(b, 'x')}",
            "predict_y": lambda xv: a + b * xv,
            "predict_x": lambda yv: self._predict_x_linear(yv, a, b),
            "curve": lambda xv: a + b * xv,
        }

    # Ajuste de regresión exponencial
    def _fit_exponential(self, x, y):
        ln_y = np.log(y)
        b, ln_a = np.polyfit(x, ln_y, 1)
        a = np.exp(ln_a)
        
        y_pred = a * np.exp(b * x)
        r2, adjusted_r2, standard_error, press, predicted_r2 = self._compute_all_metrics(x, y, y_pred, 2, self._exponential_fit_predict)
        r = np.corrcoef(x, ln_y)[0, 1]
        
        return {
            "a": a, "b": b, "r": r,
            "r2": r2, "adjusted_r2": adjusted_r2,
            "standard_error": standard_error, "press": press,
            "predicted_r2": predicted_r2,
            "equation": rf"y = {a:.4f}e^{{{b:.4f}x}}",
            "predict_y": lambda xv: a * np.exp(b * xv),
            "predict_x": lambda yv: self._predict_x_exponential(yv, a, b),
            "curve": lambda xv: a * np.exp(b * xv),
        }

    # Ajuste de regresión logarítmica
    def _fit_logarithmic(self, x, y):
        ln_x = np.log(x)
        b, a = np.polyfit(ln_x, y, 1)
        
        y_pred = a + b * ln_x
        r2, adjusted_r2, standard_error, press, predicted_r2 = self._compute_all_metrics(x, y, y_pred, 2, self._logarithmic_fit_predict)
        r = np.corrcoef(ln_x, y)[0, 1]
        
        logarithmic_term = self._latex_term(b, r"\ln(x)")
        
        return {
            "a": a, "b": b, "r": r,
            "r2": r2, "adjusted_r2": adjusted_r2,
            "standard_error": standard_error, "press": press,
            "predicted_r2": predicted_r2,
            "equation": rf"y = {a:.4f} {logarithmic_term}",
            "predict_y": lambda xv: a + b * np.log(xv),
            "predict_x": lambda yv: self._predict_x_logarithmic(yv, a, b),
            "curve": lambda xv: a + b * np.log(xv),
        }

    # Ajuste de regresión cuadrática
    def _fit_quadratic(self, x, y):
        coeffs = np.polyfit(x, y, 2)
        c, b, a = coeffs
        
        c_equals_zero = np.isclose(c, 0.0, atol=1e-8)
        b_equals_zero = np.isclose(b, 0.0, atol=1e-8)
        a_equals_zero = np.isclose(a, 0.0, atol=1e-8)

        if c_equals_zero:
            raise ValueError
        if b_equals_zero and a_equals_zero and np.all(x > 0) and np.all(y > 0):
            raise ValueError
        
        y_pred = a + b * x + c * x**2
        r2, adjusted_r2, standard_error, press, predicted_r2 = self._compute_all_metrics(x, y, y_pred, 3, self._quadratic_fit_predict)
        r = np.sqrt(max(0.0, r2))
        
        linear_term = self._latex_term(b, "x")
        quadratic_term = self._latex_term(c, "x^2")
        
        return {
            "a": a, "b": b, "c": c, "r": r,
            "r2": r2, "adjusted_r2": adjusted_r2,
            "standard_error": standard_error, "press": press,
            "predicted_r2": predicted_r2,
            "equation": rf"y = {a:.4f} {linear_term} {quadratic_term}",
            "predict_y": lambda xv: a + b * xv + c * xv**2,
            "predict_x": lambda yv: self._predict_x_quadratic(yv, a, b, c),
            "curve": lambda xv: a + b * xv + c * xv**2,
        }

    # Ajuste de regresión potencial
    def _fit_power(self, x, y):
        ln_x = np.log(x)
        ln_y = np.log(y)
        b, ln_a = np.polyfit(ln_x, ln_y, 1)
        a = np.exp(ln_a)
        
        b_equals_one = np.isclose(b, 1.0, atol=1e-6)
        if b_equals_one:
            raise ValueError
        
        y_pred = a * x**b
        r2, adjusted_r2, standard_error, press, predicted_r2 = self._compute_all_metrics(x, y, y_pred, 2, self._power_fit_predict)
        r = np.corrcoef(ln_x, ln_y)[0, 1]
        
        return {
            "a": a, "b": b, "r": r,
            "r2": r2, "adjusted_r2": adjusted_r2,
            "standard_error": standard_error, "press": press,
            "predicted_r2": predicted_r2,
            "equation": rf"y = {a:.4f}x^{{{b:.4f}}}",
            "predict_y": lambda xv: a * xv**b,
            "predict_x": lambda yv: self._predict_x_power(yv, a, b),
            "predict": lambda xv: a * xv**b,
            "curve": lambda xv: a * xv**b,
        }
        
    def _compute_all_metrics(self, x, y, y_pred, p_value, fit_predict_function):
        n = len(y)
        SSE = self._compute_SSE(y, y_pred)
        SST = self._compute_SST(y)
        
        r2 = self._compute_r2(SSE, SST)
        adjusted_r2 = self._compute_adjusted_r2(n, p_value, r2)
        standard_error = self._compute_standard_error(n, p_value, SSE)
        press = self._compute_press(x, y, fit_predict_function)
        predicted_r2 = self._compute_predicted_r2(SST, press)
        
        return r2, adjusted_r2, standard_error, press, predicted_r2

    def _compute_r2(self, SSE, SST):
        if SST == 0:
            return 1.0
        return 1 - SSE / SST

    def _compute_adjusted_r2(self, n, p_value, r2):
        if n <= p_value:
            return np.nan
        return 1 - ((1 - r2) * (n - 1) / (n - p_value))
    
    def _compute_standard_error(self, n, p_value, SSE):
        if (n - p_value) <= 0:
            return np.nan
        return np.sqrt(SSE / (n - p_value))
    
    def _compute_press(self, x, y, fit_predict_function):
        press = 0.0
        n = len(x)

        for i in range(n):
            # Elimina temporalmente el dato ubicado en la posición i
            x_train = np.delete(x, i)
            y_train = np.delete(y, i)

            # Dato que se utilizará para comprobar la predicción
            x_test = x[i]
            y_test = y[i]

            # Ajusta el modelo sin el dato i y lo predice
            y_pred = fit_predict_function(x_train, y_train, x_test)

            # Acumula el error cuadrático
            press += (y_test - y_pred) ** 2

        return press
    
    def _compute_predicted_r2(self, SST, press):
        if SST == 0:
            return np.nan
        return 1 - press / SST

    def _compute_SSE(self, y, y_pred):
        return np.sum((y - y_pred) ** 2)

    def _compute_SST(self, y):
        return np.sum((y - np.mean(y)) ** 2)
    
    # --- Funciones de predicción para PRESS ---
    def _linear_fit_predict(self, x_train, y_train, x_test):
        b, a = np.polyfit(x_train, y_train, 1)
        return a + b * x_test
        
    def _exponential_fit_predict(self, x_train, y_train, x_test):
        ln_y = np.log(y_train)
        b, ln_a = np.polyfit(x_train, ln_y, 1)
        a = np.exp(ln_a)
        return a * np.exp(b * x_test)

    def _logarithmic_fit_predict(self, x_train, y_train, x_test):
        ln_x = np.log(x_train)
        b, a = np.polyfit(ln_x, y_train, 1)
        return a + b * np.log(x_test)

    def _quadratic_fit_predict(self, x_train, y_train, x_test):
        c, b, a = np.polyfit(x_train, y_train, 2)
        return a + b * x_test + c * x_test**2

    def _power_fit_predict(self, x_train, y_train, x_test):
        ln_x = np.log(x_train)
        ln_y = np.log(y_train)
        b, ln_a = np.polyfit(ln_x, ln_y, 1)
        a = np.exp(ln_a)
        return a * x_test**b
    
    def _latex_term(self, coefficient, variable):
        sign = "+" if coefficient >= 0 else "-"
        return rf"{sign} {abs(coefficient):.4f}{variable}"
    
    def _predict_x_linear(self, y_value, a, b):
        if np.isclose(b, 0.0):
            raise ValueError("No se puede despejar X porque b es igual a 0.")
        return (np.asarray(y_value, dtype=float) - a) / b

    def _predict_x_exponential(self, y_value, a, b):
        if np.isclose(b, 0.0):
            raise ValueError("No se puede despejar X porque b es igual a 0.")
        y_value = np.asarray(y_value, dtype=float)
        ratio = y_value / a

        if np.any(ratio <= 0):
            raise ValueError("Para esta regresión, Y debe ser mayor que 0.")
        return np.log(ratio) / b

    def _predict_x_logarithmic(self, y_value, a, b):
        if np.isclose(b, 0.0):
            raise ValueError("No se puede despejar X porque b es igual a 0.")
        y_value = np.asarray(y_value, dtype=float)
        return np.exp((y_value - a) / b)

    def _predict_x_quadratic(self, y_value, a, b, c):
        if np.isclose(c, 0.0):
            raise ValueError("El modelo cuadrático se redujo a uno lineal.")
        y_value = np.asarray(y_value, dtype=float)

        discriminant = b**2 - 4 * c * (a - y_value)

        if np.any(discriminant < 0):
            raise ValueError("No existen valores reales de X para ese valor de Y.")

        discriminant_root = np.sqrt(discriminant)

        x1 = (-b + discriminant_root) / (2 * c)
        x2 = (-b - discriminant_root) / (2 * c)

        return x1, x2

    def _predict_x_power(self, y_value, a, b):
        if np.isclose(a, 0.0) or np.isclose(b, 0.0):
            raise ValueError("No se puede despejar X con estos coeficientes.")

        y_value = np.asarray(y_value, dtype=float)
        ratio = y_value / a

        if np.any(ratio <= 0):
            raise ValueError("Para esta regresión, Y debe ser mayor que 0.")

        return ratio ** (1 / b)