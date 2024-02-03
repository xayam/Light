import os.path

import numpy as np
import tensorflow as tf
import keras
from keras.src.layers import Input, Dense
from liner import create_raw, reorder

width = 256
file_name = "fb536381.txt"
model_h5 = "model.h5"
np_dtype= np.float32
tf_dtype= tf.float32

input_layer = Input(shape=(8, ), dtype=tf_dtype)
x = Dense(1500, activation="sigmoid",
          kernel_initializer=tf.keras.initializers.ones())(input_layer)
output_layer = Dense(1, activation=None)(x)

model = keras.Model(input_layer, output_layer)
model.summary()
model.compile(loss='mae', optimizer='adam',
              metrics=['accuracy'])

create_raw(file_name)
rangey = reorder(file_name + ".raw")
Y = np.asarray(rangey, dtype=np_dtype)
# Y = (Y - np.min(Y)) / (np.max(Y) - np.min(Y))
rangex = list(range(len(rangey)))
X = []
for data in rangex:
    X.append([
        (data // 256 // 16 // 4),
        (data // 256 // 16 % 4),
        (data // 256 % 16 // 4),
        (data // 256 % 16 % 4),
        (data % 256 // 16 // 4),
        (data % 256 // 16 % 4),
        (data % 256 % 16 // 4),
        (data % 256 % 16 % 4)
    ])
X = np.asarray(X, dtype=np_dtype)
# X = (data - np.min(data)) / (np.max(data) - np.min(data))
print(X)
print(Y)
if os.path.exists(model_h5):
    model.load_weights(model_h5)
    predict = model.predict(X.tolist())
    count = 0
    Y = Y.tolist()
    for p in range(len(predict)):
        print(predict[p][0], Y[p], sep=":")
        if round(predict[p][0]) == int(Y[p]):
            count += 1
    print(len(predict), len(Y), count)
    assert len(predict) == count
else:
    model.fit(X.tolist(), Y.tolist(),
              epochs=40000,
              use_multiprocessing=True,
              shuffle=False)
    model.save_weights(model_h5, save_format="h5")
