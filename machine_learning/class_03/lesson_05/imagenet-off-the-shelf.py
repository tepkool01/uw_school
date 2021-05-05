# wget https://www.cross-entropy.net/ML530/tiny_imagenet_names.txt

import numpy as np
from tensorflow.keras import applications, layers, models, preprocessing

index2name = {}
input = open("tiny_imagenet_names.txt", "r")
header = input.readline()
for line in input:
    value = line.strip("\r\n").split("\t")
    if (value[0] != ""):
        index2name[int(value[0])] = value[1]
input.close()

valX = np.load("imagenet_valX.npy")
valY = np.load("imagenet_valY.npy")

input = layers.Input(shape = (64, 64, 3))
resizing = layers.experimental.preprocessing.Resizing(224, 224)(input)
base = applications.efficientnet.EfficientNetB0(include_top = True, weights = "imagenet", input_tensor = resizing)
model = models.Model(inputs = input, outputs = base.output, name = "off-the-shelf")

probabilities = model.predict(valX)
predictions = applications.efficientnet.decode_predictions(probabilities)

top1 = 0
top5 = 0
total = 0
for i in range(valY.shape[0]):
    actual = index2name[valY[i]]
    for j in range(5):
        if (predictions[i][j][0] == actual):
            if (j == 0):
                top1 += 1
            top5 += 1
            break
    total += 1
print(top1, top5, total, sep = "\t")
