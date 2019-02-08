#test 2 nearly works
from __future__ import print_function






import tensorflow as tf
import numpy as np

#construction phase
boardRow = 6
boardHeight = 7

# Traning Prams
#learn rate
learning_rate = 0.3

#steps of training to rn
num_steps = 2000
batch_size = 100

#network parameters.
n_hidden_1 = 256
n_hidden_2 = 100
#2 hidden layers, 356 neurons. 
n_input = boardRow * boardHeight
# n_input = 42
n_ouput = 42 #output & input must be equal for graph

#input dataplace holders
X = tf.placeholder(tf.float32, [None, n_input])
#output dataplaceholder
Y = tf.placeholder(tf.float32, [None, n_output])



model = n_input * X + Y
error = tf.square(model - Y)

#learn with graident descent                     
opt = tf.train.GradientDescentOptimizer(learning_rate=learning_rate) 
opt_op = opt.minmize(error)
opt_op.run() #initalize varaibles
                      

  
#weights don't work yet idk why

#weight of hidden layer connect to input layer.
weight1 = tf.Variable(tf.random_normal([n_input, n_hidden_1]))
#weight of hidden neural network 1 connecting to hidden neural network 2.
weight2 = tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2]))
#weight of hidden neural network 2, connecting to output.
weight3 = tf.Variable(tf.random_normal([n_hidden_2, n_classes])
                      



                      

                      
                      
#execution phase
                      
                      
#fetch mini-batch
                      
#def fetch_batch(epoch, batch_index, batch_size):
