"""
Name: NeuralNetwork.py
Version: 0.01
Purpose: Creates/Saves/Loads neural network for Connect-Four game
Author: Graham Mark Broadbent
Date: 12/03/19
"""

import logging
from logManager import log

log.info('Program Begin\n')

import DataFormatter as df    # Because I couldn't find an easier option, I made one


log.info('Importing Packages')
import os
log.debug('\tImported OS')
import tensorflow as tf
log.debug('\tImported TensorFlow')			# TensorFlow 1.5
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
log.debug('\tImported Keras')
import numpy as np
log.debug('\tImported Numpy')
log.info('\tImporting Done\n')


training_input = []
training_output = []
model = None
new_model = None
has_model = False
has_new_model = False


def _get_data():
    try:
        global training_input
        global training_output

        training_input = []
        training_output = []

        log.info('Fetching training data')

        number_of_files = int(len(os.listdir('trainingData')))

        for file_num in range(0, int(number_of_files/2)):

            state_file = 'trainingData/ExportedState{}.txt'.format(file_num)
            move_file = 'trainingData/ExportedMove{}.txt'.format(file_num)

            data = df._format_array_v2(state_file)

            if not data:
                log.error('Failed to load data')
                return False

            data = np.array(data)
            training_input.append(data)

            data = df._format_array_v2(move_file)

            if not data:
                log.error('Failed to load data')
                return False

            data = np.array(data)
            training_output.append(data)

        training_input = np.array(training_input)
        training_output = np.array(training_output)

        log.info("Input array shape: {}".format(training_input.shape))
        log.info("Input data array shape: {}".format(training_input[0].shape))

        log.info('\tData fetched')
        log.info('\t\tTraining_input length: {}'.format(len(training_input)))
        log.info('\t\tTraining_out length: {}\n'.format(len(training_output)))
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._get_data\n')
        return False


def _create_model():
    try:
        global model
        global vgg16_model

        log.info('Creating network model')

        model = keras.models.Sequential()
        # vgg16_model = VGG16(weights="imagent", include_top="false", input_shape=(1000,41,))


        log.info('\tNetwork model created\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._create_model\n')
        return False


def _add_input_layer():
    # try:
        global model

        log.info('Adding input layer')

        # model.add(keras.layers.Flatten(input_shape=(None, 42), output_size=42))

        # model.add(keras.layers.Flatten)
        model.add(keras.layers.Flatten(input_shape=(1000, 41, 1)))
        # model.add(keras.layers.Input( shape=(1000, 41, )))
        # model.add(keras.layers.Flatten(input_dim=41))


        log.info('\tInput layer added\n')
        return True

    # except:
        log.error('\tUnknown error in NeuralNetwork._add_input_layer\n')
        return False


def _add_hidden_layers(layers, nodes):
    # try:
        global model

        log.info('Adding {} hidden layers'.format(layers))

        for _ in range(layers):
            # model.add(keras.layers.Dense(nodes, activation=tf.nn.relu, output_size=42))
            model.add(keras.layers.Dense(nodes, activation=tf.nn.relu))
            model.add(keras.layers.Dropout(0.01))    # Prevents over-fitting the model while training (memorisation)
            # model.add(keras.layers.Flatten())

        log.info('\tHidden layers aadded\n')
        return True

    # except:
        log.error('\tUnknown error in NeuralNetwork._add_hidden_layers\n')
        return False


def _add_output_layer(size):
    # try:
        global model

        log.info('Adding output layer')
        print(model.summary())
        model.add(keras.layers.Flatten())    # todo: Currently cuts off here
        # todo: Flatten layer expecten min_ndim=3, got ndim=2

        # model.add(keras.layers.Dense(size, activation=tf.nn.softmax, output_size=6))
        model.add(keras.layers.Dense(size, activation=tf.nn.softmax))
        # todo: ValueError: Error when checking target: expected dense_4 to have shape (1,), but got array with shape (6,)    Sorted?


        log.info('\tOutput layer added\n')
        return True

    # except:
        log.error('\tUnknown error in NeuralNetwork._add_output_layer\n')
        return False


def _compile_model():
    try:
        global model

        log.info('Network compiling')

        # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        model.compile(optimizer='adam')


        log.info('\tNetwork compiled\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._compile_model\n')
        return False


def _fit_model(epochs):
    # try:
    #     global model
    #     global training_input
    #     global training_output
    #
    #     log.info('Fitting model')
    #
    #     model.fit(training_input, training_output, epochs=epochs)    #Not currently working
    #
    #
    #     log.info('\tModel fitted\n')
    #     return True
    #
    # except:
    #     log.error('\tUnknown error in NeuralNetwork._fit_model\n')
    #     return False

    global model
    global training_input
    global training_output

    # print(model.summary())

    log.info('Fitting model')
    model.fit(training_input, training_output, epochs=epochs)    # Not currently working


    log.info('\tModel fitted\n')
    return True


def _evaluate_model():
    try:
        global model
        global test_input    # Test data doesn't exist, not strictly required
        global test_output    # Unless you want to make 1,000 more data sets

        log.info('Evaluating model')

        accuracy = model.evaluate(test_input, test_output)


        log.info('\tModel evaluated at {}% loss\n'.format(accuracy))
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._evaluate_model\n')
        return False


def _save_model(name):
    try:
        global model

        log.info('Saving model')

        name = name + '.model'

        try:
            model.save(name)

            log.info('\tModel saved as {}'.format(name))

        except:
            log.error('\tFailed to save model as {}'.format(name))
            return False

    except:
        log.error('\tUnknown error in NeuralNetwork._save_model\n')
        return False


def _load_model(name):
    try:
        global new_model
        global has_new_model

        log.info('Loading model "{}"'.format(name))

        name = name + '.model'

        try:
            new_model = keras.models.load_model(name)
            log.info('\tLoaded model "{}"\n'.format(name))
            has_new_model = True
            # keras.plot_model(new_model, to_file='Model.png')    # Would be a nice idea
            return True

        except:
            log.error('\tModel "{}" failed to load\n'.format(name))

    except:
        log.error('\tUnknown error in NeuralNetwork._load_model\n')
        return False

def _create():
    global model
    model = None

    _get_data()
    _get_data()
    _create_model()
    _add_input_layer()
    _add_hidden_layers(1, 10)
    _add_output_layer(7)
    _compile_model()
    _fit_model(3)


def _construct():
    global model
    global new_model
    global has_model
    global has_new_model
    global training_input

    _get_data()
    model = Sequential()  # configure model for train
    # model.add(Dense(32, activation='relu', input_dim=100, input_shape=(54044, 42,))) #relu activiation layer, better perfomance.
    # model.add(Dense(32, activation='relu', input_shape=(54044, 42, 100))) #relu activiation layer, better perfomance.
    model.add(Dense(32, activation='relu', input_shape=(41,)))  # relu activiation layer, better perfomance.
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation='sigmoid'))  # output layer
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])  # trains it using tensoroflow

    model.fit(training_input, training_output, epochs=20, batch_size=128)  # Trains neural network

    has_model = True

    predict_array = []
    predict_array.append(training_input[0])
    predict_array = np.array(predict_array)

    # input("Press enter to continue to prediction on data:\n\t{}\n\tShape: ".format(training_input[0], training_input[0].shape))
    # input("Press enter to continue to prediction on data:\n\t{}\n\tShape: ".format(training_input, training_input.shape))
    input("Press enter to continue to prediction on data:\n\t{}\n\tShape: ".format(predict_array, predict_array.shape))

    # print(model.predict_on_batch(training_input))
    prediction = model.predict_on_batch(predict_array)
    print("Prediction on data:\n{}".format(predict_array))
    print(prediction)
    print('\tPrediction: ', np.argmax(prediction[0]))


    input("Press enter to continue")

    _save_model("Model_0")
    _load_model("Model_0")

    predict_array = []
    predict_array.append(training_input[105])
    predict_array = np.array(predict_array)
    prediction = new_model.predict_on_batch(predict_array)
    print("Prediction on data:\n{}".format(predict_array))
    print(prediction)
    print('\tPrediction from new_model: ', np.argmax(prediction[0]))


def _predict(input_data):
    global model
    global new_model
    global has_model
    global has_new_model

    input_data = np.array(input_data)

    input_array = []
    input_array.append(input_data)
    input_array = np.array(input_array)

    if has_new_model:
        prediction = new_model.predict_on_batch(input_array)    # Because I couldn't get model.predict(...) to work
    else:
        if has_model:
            prediction = model.predict_on_batch(input_array)
        else:
            log.error("No model found")
            return False

    prediction = prediction[0]
    move = np.argmax(prediction)    # returns location of highest array value

    return move







if __name__ == "__main__":
    _get_data()
    _create_model()
    _add_input_layer()
    _add_hidden_layers(1, 10)
    _add_output_layer(7)
    _compile_model()
    print(model.summary())
    _fit_model(3)


    # log.info('Training_Input data:\t{} '.format(training_input[5]))
    # log.info('Training_Output data:\t{} '.format(training_output[5]))
    # log.info('Testing_Input data:\t{} '.format(testing_input[0][0]))
    # log.info('Testing_Output data:\t{} '.format(testing_output[0][0]))
