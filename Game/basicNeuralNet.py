print ('Program Begin\n')


print('Importing Packages')
import tensorflow as tf
print('\tImported TensorFlow')			#TensorFlow 1.5
import keras
print('\tImported Keras')
import numpy as np
print('\tImported Numpy')
#import matplotlib.pyplot as plt			#Just to see end result, not required for purpose
#print('\tImported Matplotlib.Pyplot')
print('\tImporting Done\n')


print('Setting Initial Variables')
bannerChar = '¬'
print('\tVariables Set\n')



print('Creating Dataset')
mnist = keras.datasets.mnist			#In practice, would probably be replaced with X000 possible game states
print('\tDataset Created\n')


print('Loading Data')
(xTrain, yTrain), (xTest, yTest) = mnist.load_data()
print('\tData Loaded\n')


print('Normalising Data')
xTrain = keras.utils.normalize(xTrain, axis=1)			#In this example, reduces pix values [0-255] to [0-1]
xTest = keras.utils.normalize(xTest, axis=1)			#Probably not necessary if board values [0-2]
print('\tData Normalised\n')


print('Creating Model')
model = keras.models.Sequential()
print('\tModel Created\n')


print('Adding to Model')
model.add(keras.layers.Flatten())
print('\tInput Nodes Added')
model.add(keras.layers.Dense(128, activation=tf.nn.relu))
print('\tNode Layer Added')
model.add(keras.layers.Dense(128, activation=tf.nn.relu))
print('\tNode Layer Added')
model.add(keras.layers.Dense(10, activation=tf.nn.softmax))			#10 to be replaced with 7, for possible moves
print('\tOutput Layer Added\n')


print('Compiling Model')
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',				#Still need to look into this
              matrics=['accuracy'])
print('\tModel Compiled\n')


print('Fitting Model')
model.fit(xTrain, yTrain, epochs=3)
print('\tModel Fitted\n')


print('Evaluating Model')
print(model.evaluate(xTest, yTest))
print('\tModel Evaluated\n')


print('Saving Model')
model.save('first.model')						#Would be the model actually used to play the game, once trained
print('\tModel Saved\n')


print('Loading Model')
newModel = keras.models.load_model('first.model')
print('\tModel Loaded\n')


print('Predicting')
predictions = newModel.predict([xTest])		#Where xTest might be a board, still needs looking into
print('\tPrediction of val 19: ', np.argmax(predictions[19]))
#plt.imshow(xTest[19])						#Used for testing to see accuracy
#plt.show()
print('\tPredicted\n')



print('Program End')
for _ in range (0, 50): print(bannerChar, end='')