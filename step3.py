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

X = np.reshape(dataX, (1, 74, len(dataX) * 74))
Y = dataY

print(np.shape(Y))

# define the LSTM model
model = Sequential()
# model.add(Embedding((len(cards) + 1), 128, input_length=74))
model.add(LSTM(256, input_shape=(74, len(dataX) * 74)))

# Softmax
model.add(Dense(len(cards), kernel_initializer='uniform'))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

# Delete the existing decks dir
models_path = './models'

if os.path.isdir(models_path):
    shutil.rmtree(models_path)

# Create new decks dir
os.makedirs(models_path)

# define the checkpoint
filepath = models_path + "/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# fit the model
model.fit(X, Y, epochs=20, callbacks=callbacks_list, verbose=1)
