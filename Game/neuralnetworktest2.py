import tensorflow as tf
import keras
import numpy as np
from keras.models import Sequential
from keras.layer import dense
numpy.random.seed(10)

dataset = numpy.loadtxt('connect4.csv')


#split data into x and y, values to be changed.
X = dataset[:,0:10]
Y = dataset[:,10] 

#traindata
xTrain, yTrain, xTest, yTest = train_test_split(X, Y, test_size=0.4)


model = Sequential() #model for neural network
model.add(Dense(4, input_dim=16, activation='rulu')) #input
model.add(Dense(20, activiation='relu')) #second layer
model.add(Dense(1, activiation='sigmoid')) #output layer

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', matrics=['accuracy'])

model.fit(X, Y, batch_size=16, epochs=3)

scores = model.evaluate(X, Y)
model = model.predict(X)






