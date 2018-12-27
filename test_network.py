import numpy as np
import pickle
import os
import shutil
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LSTM, Flatten
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

dataX = []
dataY = []
cards = []

with open('deck_lists_x.pkl','rb') as f:
    dataX = np.asarray(pickle.load(f))

with open('deck_lists_y.pkl','rb') as f:
    dataY = np.asarray(pickle.load(f))

with open('cards_lists.pkl','rb') as f:
    cards = pickle.load(f)


print("Reshaping")

X = np.reshape(dataX, (len(dataX) * 74, 74, 1))
Y = np.reshape(dataY, (962740, 1136))

# define the LSTM model
model = Sequential()
# model.add(Embedding((len(cards) + 1), 128, input_length=74))
model.add(LSTM(256, input_shape=(74, 1)))

# Softmax
model.add(Dense(len(cards), kernel_initializer='uniform'))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

# load weights
model.load_weights("models/weights-improvement-01-5.1192.hdf5")

# Compile model (required to make predictions)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print("Created model and loaded weights from file")
