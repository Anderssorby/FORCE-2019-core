from sklearn import linear_model


def fit_linear(x, y):
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    return reg
