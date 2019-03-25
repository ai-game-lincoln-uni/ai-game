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
log.debug('\tImported Keras')
import numpy as np
log.debug('\tImported Numpy')
#import matplotlib.pyplot as plt			# Just to see end result, not required for purpose
#print('\tImported Matplotlib.Pyplot')
log.info('\tImporting Done\n')


training_input = []
training_output = []
model = None
new_model = None


def _get_data():
    try:
        global training_input
        global training_output

        training_input = []
        training_output = []

        log.info('Fetching training data')

        number_of_files = int(len(os.listdir('trainingData')))

        for file_num in range(0, int(number_of_files/2)):
            file = 'trainingData/ExportedState{}.txt'.format(file_num)

            f = open(file, "r")
            data = list(f.read())
            # data = np.load(file)
            data = df._format_array_v2(file)
            training_input.append(data)


            file = 'trainingData/ExportedMove{}.txt'.format(file_num)

            f = open(file, "r")
            data = list(f.read())
            # data = np.load(file)
            data = df._format_array_v2(file)
            training_output.append(data)


        log.info('\tData fetched\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._get_data\n')
        return False


def _create_model():
    try:
        global model

        log.info('Creating network model')

        model = keras.models.Sequential()


        log.info('\tNetwork model created\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._create_model\n')
        return False


def _add_input_layer():
    try:
        global model

        log.info('Adding input layer')

        model.add(keras.layers.Flatten())


        log.info('\tInput layer added\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._add_input_layer\n')
        return False


def _add_hidden_layers(layers, nodes):
    try:
        global model

        log.info('Adding {} hidden layers'.format(layers))

        for _ in range(layers):
            model.add(keras.layers.Dense(nodes, activation=tf.nn.relu))


        log.info('\tHidden layers aadded\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._add_hidden_layers\n')
        return False


def _add_output_layer(size):
    try:
        global model

        log.info('Adding output layer')

        model.add(keras.layers.Dense(size, activation=tf.nn.softmax))


        log.info('\tOutput layer added\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._add_output_layer\n')
        return False


def _compile_model():
    try:
        global model

        log.info('Network compiling')

        model.compile(optimizer='adam', loss='sparse_catagorical_crossenthropy', metrics=['accuracy'])


        log.info('\tNetwork compiled\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._compile_model\n')
        return False


def _fit_model(epochs):
    try:
        global model
        global training_input
        global training_output

        log.info('Fitting model')

        model.fit(training_input, training_output, epochs=epochs)    #Not currently working


        log.info('\tModel fitted\n')
        return True

    except:
        log.error('\tUnknown error in NeuralNetwork._fit_model\n')
        return False


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
        global model

        log.info('Loading model "{}"'.format(name))

        name = name + '.model'

        try:
            new_model = keras.models.load_model(name)
            log.info('\tLoaded model "{}"\n'.format(name))
            return True

        except:
            log.error('\tModel "{}" failed to load\n'.format(name))

    except:
        log.error('\tUnknown error in NeuralNetwork._load_model\n')
        return False







if __name__ == "__main__":
    _get_data()
    #_create_model()
    #_add_input_layer()
    #_add_hidden_layers(3, 128)
    #_add_output_layer(10)
    #_compile_model()
    #_fit_model(3)


    log.info('Training_Output data:\t{} '.format(training_output[0][0]))
