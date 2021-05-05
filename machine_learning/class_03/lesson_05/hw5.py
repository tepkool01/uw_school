# python mnist-cnn.py sgd
# python mnist-cnn.py rmsprop
# python mnist-cnn.py adam

import sys
from tensorflow.keras import callbacks, datasets, layers, models, optimizers

optimizer_name = sys.argv[1]
model_name = "mnist-" + optimizer_name

(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], x_train.shape[2],
                          1)).astype("float32") / 255.0
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2],
                        1)).astype("float32") / 255.0

model = models.Sequential()
model.add(layers.Conv2D(filters = 16, kernel_size = (3, 3), activation = "relu",
                        input_shape = (28,28,1)))
model.add(layers.Conv2D(filters = 32, kernel_size = (3, 3), activation = "relu"))
model.
model.add(layers.MaxPooling2D(pool_size = (2, 2)))
model.add(layers.Dropout(0.25))
model.add(layers.Flatten())
model.add(layers.Dense(units = 128, activation = "relu"))
model.add(layers.Dropout(0.50))
model.add(layers.Dense(y_train.max() + 1, activation = "softmax"))
model.compile(loss = "sparse_categorical_crossentropy", optimizer = optimizer_name,
              metrics = ["accuracy"])

# model.fit(x_train, y_train, batch_size = 128, epochs = 16, validation_split = 0.1,
#           callbacks = [ callbacks.EarlyStopping(monitor = "val_accuracy", patience = 8,
#                                                 restore_best_weights = True) ])
model.summary()
model.save(model_name)

model = models.load_model(model_name)
model.evaluate(x_test, y_test)