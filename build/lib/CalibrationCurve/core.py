# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['CalibrationModel']

# %% ../nbs/00_core.ipynb 5
class CalibrationModel:
    def __init__(self, data, response_variable, test_replicates):
        self.raw_data = self.load_data(data)
        self.response_variable = response_variable
        self.fit = None
        self.test_replicates = test_replicates
        self.cal_line_points = self.raw_data.shape[0]
        self.r2 = None

    def load_data(self, data):
        if ".csv" in data:
            raw_data = pd.read_csv(data)
        else:
            raw_data = data
        return raw_data

    def fit_ols(self):
        X = self.raw_data[["concentration"]]
        y = self.raw_data[self.response_variable]
        self.fit = LinearRegression().fit(X, y)
        self.r2 = self.fit.score(X, y)
        return self.fit

    def get_params(self):
        slope = self.fit.coef_[0]
        intercept = self.fit.intercept_
        return slope, intercept

    def get_r2(self):
        return self.r2

    def inverse_prediction(self, unknown: float):
        slope, intercept = self.get_params()
        return (unknown - intercept) / slope

    def calculate_sse(self):
        y_pred = self.fit.predict(self.raw_data[["concentration"]])
        return np.sum((y_pred - self.raw_data[self.response_variable]) ** 2)

    def calculate_syx(self):
        return np.sqrt((self.calculate_sse()) / (len(self.raw_data) - 2))

    def get_t_value(self, alpha):
        return t.ppf(1 - alpha / 2, len(self.raw_data) - 2)

    def calculate_uncertainty(self):
        return self.calculate_sxhat() * self.get_t_value(0.05)

    def calculate_sxhat(self):
        return (self.calculate_syx() / self.fit.coef_[0]) * np.sqrt(1 / self.test_replicates + self.cal_line_points)

    def fit_model(self):
        self.fit_ols()
        self.get_params()
        self.get_r2()
        self.calculate_uncertainty()
        self.tabulate_results()

    def plot_fit(self):
        sns.regplot(x="concentration", y=self.response_variable, data=self.raw_data)
        sns.despine()
        sns.set_context("paper")
        plt.title(f"Calibration curve of concentration versus {self.response_variable}")
        plt.xlabel("Concentration")
        plt.ylabel("Peak Value")
        plt.annotate(f"R-squared = {self.get_r2():.3f}", xy=(0.3, 0.8), xycoords="axes fraction", fontsize=9,
                     ha="center", va="center")
        plt.annotate(f"Regression formula: y = {self.get_params()[0]:.3f} * x + {self.get_params()[1]:.3f}",
                     xy=(0.3, 0.7), xycoords="axes fraction", fontsize=9, ha="center", va="center")
        plt.show()



    def tabulate_results(self):
        print(f"Calibration curve of {self.response_variable} versus concentration")
        print(f"R2 = {self.r2}")
        print(f"Slope = {self.get_params()[0]}")
        print(f"Intercept = {self.get_params()[1]}")
        print(f"Uncertainity = {self.calculate_uncertainty()}")
        # print(f"Prediction = {self.inverse_prediction()}")
    