import math
import numpy as np
import tensorflow
from tensorflow.keras import applications, callbacks, layers, models, optimizers

batch_size = 64
image_size = [ 224, 240, 260, 300, 380, 456, 528, 600, 640 ]

class MeanAveragePrecision(callbacks.Callback):
    def __init__(self, k, val):
        self.k = k
        self.X = val[0]
        self.Y = val[1]
        self.score = [ 1.0 / (i + 1.0) for i in range(k) ]

    def on_epoch_end(self, epoch, logs = None):
        probabilities = self.model.predict(self.X)
        indices = probabilities.argsort(axis = -1)[:,-self.k:][:,::-1]
        totalScore = 0.0
        for i in range(indices.shape[0]):
            for j in range(indices.shape[1]):
                if (indices[i,j] == self.Y[i]):
                    totalScore += self.score[j]
                    break
        meanAveragePrecision = totalScore / indices.shape[0]
        print("\nmap: " + str(meanAveragePrecision) + "\n")
        logs["map"] = meanAveragePrecision

trnX = np.load("imagenet_trnX.npy")
trnY = np.load("imagenet_trnY.npy")
valX = np.load("imagenet_valX.npy")
valY = np.load("imagenet_valY.npy")
tstX = np.load("imagenet_tstX.npy")

# unusual: no preprocessing in preprocess_input():
# https://github.com/tensorflow/tensorflow/blob/v2.4.1/tensorflow/python/keras/applications/efficientnet.py#L735-L737
SIZE_INDEX = 0
input = layers.Input(shape = (64, 64, 3))
resizing = layers.experimental.preprocessing.Resizing(image_size[SIZE_INDEX + 1], image_size[SIZE_INDEX + 1])(input)
crop = layers.experimental.preprocessing.RandomCrop(image_size[SIZE_INDEX], image_size[SIZE_INDEX])(resizing)
flip = layers.experimental.preprocessing.RandomFlip("horizontal")(crop)
base = applications.EfficientNetB0(include_top = False, weights = "imagenet", input_tensor = flip, pooling = "avg")
base.trainable = False
output = layers.Dropout(0.2, name = "pool_dropout")(base.output)
output = layers.Dense(512, activation = "relu", name = "dense_features")(output)
output = layers.Dropout(0.2, name = "dense_dropout")(output)
output = layers.Dense(trnY.max() + 1, activation = "softmax", name = "classifier")(output)
model = models.Model(inputs = input, outputs = output, name = "transfer_model")

callbacks = [ MeanAveragePrecision(5, [ valX, valY ]),
              callbacks.EarlyStopping(monitor = "map", mode = "max", patience = 4, restore_best_weights = True) ]

steps_per_epoch = math.ceil(1.0 * trnX.shape[0] / batch_size)
schedule = tensorflow.keras.experimental.CosineDecayRestarts(0.001, first_decay_steps = steps_per_epoch, t_mul = 1, m_mul = 0.95)
model.compile(loss = "sparse_categorical_crossentropy", optimizer = optimizers.Adam(learning_rate = schedule), metrics =[ "accuracy" ])
model.summary(line_length = 135)
model.fit(trnX, trnY, epochs = 8, validation_data = (valX, valY), callbacks = callbacks)

base.trainable = True
schedule = tensorflow.keras.experimental.CosineDecayRestarts(0.0001, first_decay_steps = steps_per_epoch, t_mul = 1, m_mul = 0.95)
model.compile(loss = "sparse_categorical_crossentropy", optimizer = optimizers.Adam(learning_rate = schedule), metrics =[ "accuracy" ])
model.summary(line_length = 135)
model.fit(trnX, trnY, epochs = 2, validation_data = (valX, valY), callbacks = callbacks)

probabilities = model.predict(tstX)
indices = probabilities.argsort(axis = -1)[:,-5:][:,::-1]

predictions = open("predictions.csv", "w")
predictions.write("id,label\n")
for i in range(tstX.shape[0]):
    predictions.write(str(i).zfill(5) + "," + str(" ".join([ str(classIndex) for classIndex in indices[i,:] ])) + "\n")
predictions.close()
