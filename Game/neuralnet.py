#sources of information: https://keras.io/

#load data libaries
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense, Dropout

dataset = read_csv("connect4.csv", delimiter=",") #reads in file. http://archive.ics.uci.edu/ml/datasets/connect-4

#selecting data by row numbers, data set has 43 rows. Split it.
X = dataset.iloc[:,0:42].values 
Y = dataset.iloc[:,42:43].values 


# Encode categorical variables as numeric
labelencoder_X = LabelEncoder()
for _ in range(9):
    X[:, _] = labelencoder_X.fit_transform(X[:, _])

# Onehot encode all dependent categorical variables
onehotencoder = OneHotEncoder(categorical_features = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41])
X = onehotencoder.fit_transform(X).toarray()


x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = Sequential() #configure model for train
model.add(Dense(32, activation='relu', input_dim=100)) #relu activiation layer, better perfomance.
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid')) #output layer


model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy']) #trains it using tensoroflow

model.fit(x_train, y_train, epochs=20,batch_size=128) #Trains neural network

score = model.evaluate(x_test, y_test, batch_size=128) #evulates performance

pred = model.predict(x_test) #make predicitions on new data
