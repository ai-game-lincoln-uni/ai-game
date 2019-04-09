import logging
from logManager import  log
import NeuralNetwork
import pytest

training_input = []
training_output = []
model = None
new_model = None


# All tests should return True unless an error occurs, except test__save_model, which returns None


def test__get_data(): # Done
    # This function should return True unless there is an error
    assert NeuralNetwork._get_data() == True

def test__create_model(): # Done
    # This function should return True unless an error occurs
    assert NeuralNetwork._create_model() == True

def test__add_input_layer(): # Done
    # This function should return True unless an error occurs
    assert NeuralNetwork._add_input_layer() == True

def test__add_hidden_layers(): # Done
    # This function should return True unless there is an error
    assert NeuralNetwork._add_hidden_layers(2, 2) == True
    assert NeuralNetwork._add_hidden_layers(5, 7) == True


def test__add_output_layer():
    # This function should return True unless an error occurs
    assert NeuralNetwork._add_output_layer(42) == True

def test__compile_model():
    # Return True unless an error occurs
    assert NeuralNetwork._compile_model() == True

def test__evaluate_model():
    # Return True unless an error occurs
    assert NeuralNetwork._evaluate_model() == True


def test__save_model():
    # Return None unless an error occurs
    assert NeuralNetwork._save_model("test") == None

def test__load_model():
    # Return True unless an error occurs
    assert NeuralNetwork._load_model("test") == True

def test__fit_model():
    assert NeuralNetwork._fit_model(42) == True

