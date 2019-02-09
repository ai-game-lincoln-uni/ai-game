#works if someone finds out how to fix the input size, I can't figure it out.
#sources of information: https://keras.io/


import numpy as np
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense, Dropout

dataset = read_csv("connect4.csv", delimiter=",") #reads in file. http://archive.ics.uci.edu/ml/datasets/connect-4

X = dataset.iloc[:,0:2].values #this bit I am having problems with!
Y = dataset.iloc[:,1].values
encoder = LabelEncoder()
encoder.fit(X)
encoded_X = encoder.transform(X)
encoder.fit(Y)
encoded_Y = encoder.transform(Y)

#binary classification because it is a neural network, read keras documention for more knoweldge.
model = Sequential()
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))


model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=20,batch_size=128)

score = model.evaluate(encoded_X, encoded_Y, batch_size=128)
