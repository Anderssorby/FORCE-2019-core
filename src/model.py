import keras.layers as KL
from sklearn import linear_model


def fit_linear(x, y):
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    return reg

def feed_forward(n_inputs, n_outputs):
    inputs = KL.Input((x.shape[1],))
    h = KL.Dense(128, activation="relu")(inputs)
    h = KL.Dense(128, activation="relu")(h)
    h = KL.Dense(128, activation="relu")(h)
    outputs = KL.Dense(5, activation="softmax")(h)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    model.summary()
    return model
    model.fit(x_train, y_train, epochs=4)
    accuracy = np.mean(model.predict(x_test).argmax(1) == y_test.argmax(1))
print(f"Got accuracy {accuracy}")
