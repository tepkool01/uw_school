import math
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import activations, callbacks, experimental, layers, metrics, models, optimizers, regularizers
from kerastuner import Objective
from kerastuner.tuners import RandomSearch, Hyperband, BayesianOptimization

trnX = np.load("reuters_trnX.npy")
valX = np.load("reuters_valX.npy")
tstX = np.load("reuters_tstX.npy")
trnY = np.load("reuters_trnY.npy")
valY = np.load("reuters_valY.npy")

class CustomTuner(Hyperband):
    def run_trial(self, trial, *args, **kwargs):
        batch_size = trial.hyperparameters.values["batch_size"]
        kwargs["batch_size"] = batch_size
        super(CustomTuner, self).run_trial(trial, *args, **kwargs)

def leaky(x):
    return activations.relu(x, alpha = 0.3)

def build_model(hp):
    dense_depth = hp.Int("dense_depth", min_value = 0, max_value = 3, step = 1)
    dense_width = hp.Choice("dense_width", values = [ 32, 64, 128 ])
    activation_name = hp.Choice("activation", values = [ "linear", "relu", "sigmoid", "tanh", "leaky", "elu", "selu" ])
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

    input = layers.Input(shape = (trnX.shape[1],))
    x = input
    for layer in range(dense_depth):
        x = layers.Dense(units = dense_width, activation = activation, kernel_regularizer = regularizer)(x)
        if (dropout != "none"):
            if (activation_name == "selu"):
                x = layers.AlphaDropout(float(dropout))(x)
            else:
                x = layers.Dropout(float(dropout))(x)

    output = layers.Dense(3, activation = "sigmoid")(x)
    model = models.Model(inputs = input, outputs = output)
    steps_per_epoch = math.ceil(trnX.shape[0] / batch_size)
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
    model.compile(optimizer = optimizer, loss = "binary_crossentropy", metrics = [ metrics.AUC(multi_label = True) ])

    return model

tuner = CustomTuner(build_model,
                    objective = Objective("val_auc", direction = "max"),
                    max_epochs = 32,
                    hyperband_iterations = 1,
                    directory = "reuters",
                    project_name = "bandit")
tuner.search_space_summary()
tuner.search(trnX, trnY, validation_data = (valX, valY))
tuner.results_summary()

model = tuner.get_best_models(num_models = 1)[0]
hyperparameters = tuner.get_best_hyperparameters(num_trials = 1)[0].get_config()
print(hyperparameters["values"])

probabilities = model.predict(tstX)
predictions = open("predictions.csv", "w")
predictions.write("id,earnPrediction,acqPrediction,moneyfxPrediction\n")
for i in range(tstX.shape[0]):
    predictions.write(str(i).zfill(5) + "," + str(probabilities[i,0]) + "," + str(probabilities[i,1]) + "," + str(probabilities[i,2]) + "\n")
predictions.close()
