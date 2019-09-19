import keras
import keras.layers as KL
from sklearn import linear_model


def fit_linear(x, y):
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    return reg


def make_feed_forward(n_inputs, n_outputs):
    inputs = KL.Input((n_inputs,))
    h = KL.Dense(128, activation="relu")(inputs)
    h = KL.Dense(128, activation="relu")(h)
    h = KL.Dense(128, activation="relu")(h)
    outputs = KL.Dense(n_outputs, activation="softmax")(h)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    model.summary()
    return model
