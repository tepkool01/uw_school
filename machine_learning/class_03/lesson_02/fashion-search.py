import math
import numpy as np
from io import TextIOWrapper
from PIL import Image
from zipfile import ZipFile

trnX = np.zeros((60000, 28, 28), dtype = "float32")
trnY = np.zeros((60000), dtype = "int32")
tstX = np.zeros((10000, 28, 28), dtype = "float32")
with ZipFile("ml410-20-sp-fashion.zip", "r") as archive:
    index = 0
    for i in range(trnX.shape[0]):
        with archive.open("fashion_trn/fashion_trn_" + str(i).zfill(5) + ".png") as file:
            img = Image.open(file)
            trnX[i] = np.asarray(img)
        index = index + 1
    with TextIOWrapper(archive.open("fashion_trn.csv", "r")) as file:
        header = file.readline()
        for i in range(trnY.shape[0]):
            trnY[i] = np.int32(file.readline().strip("\r\n").split(",")[1])
    index = 0
    for i in range(tstX.shape[0]):
        with archive.open("fashion_tst/fashion_tst_" + str(i).zfill(5) + ".png") as file:
            img = Image.open(file)
            tstX[i] = np.asarray(img)
        index = index + 1

trnX = trnX / 255
tstX = tstX / 255

from tensorflow import keras
from tensorflow.keras import activations, callbacks, experimental, layers, models, optimizers, regularizers
from kerastuner.tuners import Hyperband

class CustomTuner(Hyperband):
    def run_trial(self, trial, *args, **kwargs):
        batch_size = trial.hyperparameters.values["batch_size"]
        kwargs["batch_size"] = batch_size
        kwargs["steps_per_epoch"] = math.ceil(0.9 * trnX.shape[0] / batch_size)
        super(CustomTuner, self).run_trial(trial, *args, **kwargs)

def leaky(x):
    return activations.relu(x, alpha = 0.3)

def build_model(hp):
    dense_depth = hp.Int("dense_depth", min_value = 0, max_value = 2, step = 1)
    dense_width = hp.Choice("dense_width", values = [ 64, 128, 256, 512 ])
    activation_name = hp.Choice("activation", values = [ "linear", "relu", "sigmoid", "tanh", "leaky", "elu", "selu" ])
    convolution_block_count = hp.Choice("convolution_block_count", values = [ 0, 1, 2, 3 ])
    if (activation_name == "leaky"):
        activation = leaky
    else:
        activation = activation_name
    regularization_function = hp.Choice("regularization_function", values = [ "none", "l1", "l2", "l1_l2" ])
    regularization_penalty = hp.Choice("regularization_penalty", values = [ 0.0001, 0.00001 ])
    regularizer = None
    if (regularization_function == "l1"):
        regularizer = regularizers.l1(regularization_penalty)
    elif (regularization_function == "l2"):
        regularizer = regularizers.l2(regularization_penalty)
    elif (regularization_function == "l1_l2"):
        regularizer = regularizers.l1_l2(regularization_penalty, regularization_penalty)
    dropout = hp.Choice("dropout", values = [ "none", "0.1", "0.2", "0.5" ])
    optimizer = hp.Choice("optimizer", values = [ "adam", "rmsprop", "sgd" ])
    initial_learning_rate = hp.Choice("learning_rate", values = [ 0.01, 0.001, 0.0001 ])
    learning_rate_schedule = hp.Choice("learning_rate_schedule", values = [ "none", "exponential", "cosine" ])
    batch_size = hp.Choice("batch_size", values = [ 512, 1024, 2048 ])

    model = keras.Sequential()
    model.add(layers.Input(shape = (trnX.shape[1], trnX.shape[2])))

    if (convolution_block_count == 0):
        model.add(layers.Reshape((trnX.shape[1] * trnX.shape[2],)))
    else:
        model.add(layers.Reshape((trnX.shape[1], trnX.shape[2], 1)))

    filter_count = 64
    for block in range(convolution_block_count):
        model.add(layers.Conv2D(filters = filter_count, kernel_size = (3, 3), activation = "relu", padding = "same", kernel_regularizer = regularizer))
        model.add(layers.Conv2D(filters = filter_count, kernel_size = (3, 3), activation = "relu", padding = "same", kernel_regularizer = regularizer))
        model.add(layers.MaxPooling2D(pool_size = (2, 2)))
        filter_count += 64
    if (convolution_block_count > 0):
        model.add(layers.Flatten())

    for layer in range(dense_depth):
        model.add(layers.Dense(units = dense_width, activation = activation, kernel_regularizer = regularizer))
        if (dropout != "none"):
            if (activation_name == "selu"):
                model.add(layers.AlphaDropout(float(dropout)))
            else:
                model.add(layers.Dropout(float(dropout)))

    model.add(layers.Dense(trnY.max() + 1, activation = "softmax"))
    steps_per_epoch = math.ceil(0.9 * trnX.shape[0] / batch_size)
    learning_rate = initial_learning_rate
    if (learning_rate_schedule == "exponential"):
        learning_rate = optimizers.schedules.ExponentialDecay(initial_learning_rate = initial_learning_rate, decay_steps = steps_per_epoch, decay_rate = 0.95)
    elif (learning_rate_schedule == "cosine"):
        learning_rate = experimental.CosineDecayRestarts(initial_learning_rate = initial_learning_rate, first_decay_steps = steps_per_epoch)
    optimizer = optimizers.Adam(learning_rate = learning_rate)
    if (optimizer == "rmsprop"):
        optimizer = optimizers.RMSprop(learning_rate = learning_rate)
    elif (optimizer == "sgd"):
        optimizer = optimizers.SGD(learning_rate = learning_rate)
    model.compile(optimizer = optimizer, loss = "sparse_categorical_crossentropy", metrics = [ "accuracy" ])

    return model

tuner = CustomTuner(build_model,
                    objective = "val_accuracy",
                    max_epochs = 32,
                    hyperband_iterations = 1,
                    directory = "fashion",
                    project_name = "bandit")

callbacks = [ callbacks.EarlyStopping(monitor = "val_accuracy", patience = 16, restore_best_weights = True) ]

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
