import logging
from logManager import log

log.info('Program Begin\n')


log.info('Importing Packages')
import tensorflow as tf
log.debug('\tImported TensorFlow')			#TensorFlow 1.5
import keras
log.debug('\tImported Keras')
import numpy as np
log.debug('\tImported Numpy')
#import matplotlib.pyplot as plt			#Just to see end result, not required for purpose
#print('\tImported Matplotlib.Pyplot')
log.info('\tImporting Done\n')


log.debug('Setting Initial Variables')
bannerChar = '¬'
log.debug('\tVariables Set\n')



log.debug('Creating Dataset')
mnist = keras.datasets.mnist			#In practice, would probably be replaced with X000 possible game states
log.debug('\tDataset Created\n')


log.debug('Loading Data')
(xTrain, yTrain), (xTest, yTest) = mnist.load_data()
log.debug('\tData Loaded\n')


log.debug('Normalising Data')
xTrain = keras.utils.normalize(xTrain, axis=1)			#In this example, reduces pix values [0-255] to [0-1]
xTest = keras.utils.normalize(xTest, axis=1)			#Probably not necessary if board values [0-2]
log.debug('\tData Normalised\n')


log.info('Creating Model')
model = keras.models.Sequential()
log.info('\tModel Created\n')


log.debug('Adding to Model')
model.add(keras.layers.Flatten())
log.debug('\tInput Nodes Added')
model.add(keras.layers.Dense(128, activation=tf.nn.relu))
log.debug('\tNode Layer Added')
model.add(keras.layers.Dense(128, activation=tf.nn.relu))
log.debug('\tNode Layer Added')
model.add(keras.layers.Dense(10, activation=tf.nn.softmax))			#10 to be replaced with 7, for possible moves
log.debug('\tOutput Layer Added\n')


log.info('Compiling Model')
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',				#Still need to look into this
              matrics=['accuracy'])
log.info('\tModel Compiled\n')


log.info('Fitting Model')
model.fit(xTrain, yTrain, epochs=3)
log.info('\tModel Fitted\n')


log.info('Evaluating Model')
print(model.evaluate(xTest, yTest))
log.info('\tModel Evaluated\n')


log.info('Saving Model')
model.save('first.model')						#Would be the model actually used to play the game, once trained
log.info('\tModel Saved\n')


log.info('Loading Model')
newModel = keras.models.load_model('first.model')
log.info('\tModel Loaded\n')


log.info('Predicting')
predictions = newModel.predict([xTest])		#Where xTest might be a board, still needs looking into
print('\tPrediction of val 19: ', np.argmax(predictions[19]))
#plt.imshow(xTest[19])						#Used for testing to see accuracy
#plt.show()
log.info('\tPredicted\n')



log.info('Program End')
for _ in range (0, 50): print(bannerChar, end='')