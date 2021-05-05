import numpy as np
from io import TextIOWrapper
from PIL import Image
from zipfile import ZipFile

with ZipFile("ml530-2021-sp-imagenet.zip", "r") as archive:
    trnX = np.zeros((100000, 64, 64, 3), dtype = "float32")
    index = 0
    for i in range(trnX.shape[0]):
        with archive.open("imagenet_trn/imagenet_trn/imagenet_trn_" + str(i).zfill(5) + ".png") as file:
            img = Image.open(file)
            trnX[i] = np.asarray(img)
        index = index + 1
    np.save("imagenet_trnX.npy", trnX)
    trnY = np.zeros((100000,), dtype = "int32")
    with TextIOWrapper(archive.open("imagenet_trn.csv", "r")) as file:
        header = file.readline()
        for i in range(trnY.shape[0]):
            trnY[i] = np.int32(file.readline().strip("\r\n").split(",")[1])
    np.save("imagenet_trnY.npy", trnY)
    valX = np.zeros((10000, 64, 64, 3), dtype = "float32")
    index = 0
    for i in range(valX.shape[0]):
        with archive.open("imagenet_val/imagenet_val/imagenet_val_" + str(i).zfill(5) + ".png") as file:
            img = Image.open(file)
            valX[i] = np.asarray(img)
        index = index + 1
    np.save("imagenet_valX.npy", valX)
    valY = np.zeros((10000,), dtype = "int32")
    with TextIOWrapper(archive.open("imagenet_val.csv", "r")) as file:
        header = file.readline()
        for i in range(valY.shape[0]):
            valY[i] = np.int32(file.readline().strip("\r\n").split(",")[1])
    np.save("imagenet_valY.npy", valY)
    tstX = np.zeros((10000, 64, 64, 3), dtype = "float32")
    index = 0
    for i in range(tstX.shape[0]):
        with archive.open("imagenet_tst/imagenet_tst/imagenet_tst_" + str(i).zfill(5) + ".png") as file:
            img = Image.open(file)
            tstX[i] = np.asarray(img)
        index = index + 1
    np.save("imagenet_tstX.npy", tstX)
