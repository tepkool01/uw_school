# pip install keras-tuner

import math
import numpy as np
from io import TextIOWrapper
from PIL import Image
from zipfile import ZipFile

trnX = np.zeros((60000, 28, 28), dtype = "float32")
trnY = np.zeros((60000), dtype = "int32")
tstX = np.zeros((10000, 28, 28), dtype = "float32")
with ZipFile("ml530-2021-sp-mnist.zip", "r") as archive:
    index = 0
    for i in range(trnX.shape[0]):
        with archive.open("mnist_trn_images/mnist_trn_" + str(i).zfill(5) + ".png") as file:
            img = Image.open(file)
            trnX[i] = np.asarray(img)
        index = index + 1
    with TextIOWrapper(archive.open("mnist_trn.csv", "r")) as file:
        header = file.readline()
        for i in range(trnY.shape[0]):
            trnY[i] = np.int32(file.readline().strip("\r\n").split(",")[1])
    index = 0
    for i in range(tstX.shape[0]):
        with archive.open("mnist_tst_images/mnist_tst_" + str(i).zfill(5) + ".png") as file:
            img = Image.open(file)
            tstX[i] = np.asarray(img)
        index = index + 1

trnX = trnX.reshape(trnX.shape[0], trnX.shape[1] * trnX.shape[2])
tstX = tstX.reshape(tstX.shape[0], tstX.shape[1] * tstX.shape[2])

trnX = trnX / 255
tstX = tstX / 255

from tensorflow import keras
from tensorflow.keras import callbacks, layers, optimizers
from kerastuner.tuners import RandomSearch, Hyperband, BayesianOptimization

class CustomTuner(Hyperband):
    def run_trial(self, trial, *args, **kwargs):
        batch_size = trial.hyperparameters.values["batch_size"]
        kwargs["batch_size"] = batch_size
        kwargs["steps_per_epoch"] = math.ceil(0.9 * trnX.shape[0] / batch_size)
        super(CustomTuner, self).run_trial(trial, *args, **kwargs)

def build_model(hp):
    depth = hp.Int("depth", min_value = 0, max_value = 4, step = 1)
    width = hp.Choice("width", values = [ 64, 128, 256, 512 ])
    activation = hp.Choice("activation", values = [ "linear", "relu", "sigmoid", "tanh" ])
    dropout = hp.Float("dropout", 0, 0.5, step = 0.1)
    optimizer = hp.Choice("optimizer", values = [ "adam", "rmsprop", "sgd" ])
    learning_rate = hp.Choice("learning_rate", values = [ 0.01, 0.001, 0.0001 ])
    batch_size = hp.Choice("batch_size", values = [ 512, 1024, 2048 ])
    model = keras.Sequential()
    for depth in range(depth):
        model.add(layers.Dense(units = width, activation = activation))
        model.add(layers.Dropout(dropout))
    optimizer = optimizers.Adam
    if (optimizer == "rmsprop"):
        optimizer = optimizers.RMSprop
    elif (optimizer == "sgd"):
        optimizer = optimizers.SGD
    model.add(layers.Dense(trnY.max() + 1, activation = "softmax"))
    model.compile(optimizer = optimizer(learning_rate = learning_rate), loss = "sparse_categorical_crossentropy", metrics = [ "accuracy" ])
    return model

#tuner = RandomSearch(build_model,
#            objective = "val_accuracy",
#            max_trials = 32,
#            executions_per_trial = 1,
#            directory = "tuning",
#            project_name = "random")
#tuner = BayesianOptimization(build_model,
#            objective = "val_accuracy",
#            max_trials = 32,
#            num_initial_points = 8,
#            directory = "tuning",
#            project_name = "bayesian")
#tuner = Hyperband(build_model,
#            objective = "val_accuracy",
#            max_epochs = 32,
#            hyperband_iterations = 1,
#            directory = "tuning",
#            project_name = "bandit")
tuner = CustomTuner(build_model,
                    objective = "val_accuracy",
                    max_epochs = 32,
                    hyperband_iterations = 1,
                    directory = "tuning",
                    project_name = "bandit")

callbacks = [ callbacks.ReduceLROnPlateau(monitor = "val_accuracy", patience = 2),
              callbacks.EarlyStopping(monitor = "val_accuracy", patience = 8, restore_best_weights = True) ]

tuner.search_space_summary()
tuner.search(trnX, trnY, validation_split = 0.1, callbacks = callbacks)
tuner.results_summary()

model = tuner.get_best_models(num_models = 1)[0]
hyperparameters = tuner.get_best_hyperparameters(num_trials = 1)[0].get_config()
print(hyperparameters["values"])

probabilities = model.predict(tstX)
classes = probabilities.argmax(axis = -1)
predictions = open("predictions.csv", "w")
predictions.write("id,label\n")
for i in range(tstX.shape[0]):
    predictions.write(str(i).zfill(5) + "," + str(classes[i]) + "\n")
predictions.close()
model.summary()
