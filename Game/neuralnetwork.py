import tensorflow as tf

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
n_classes = 100 #output but i don't know what the numeber should be. 


#input dataplace holders
X = tf.placeholder(tf.float32, [None, n_input])
#output dataplaceholder
Y = tf.placeholder(tf.float32, [None, n_classes])

#weights don't work yet idk why

#weight of hidden layer connect to input layer.
weight1 = tf.Variable(tf.random_normal([n_input, n_hidden_1]))
#weight of hidden neural network 1 connecting to hidden neural network 2.
weight2 = tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2]))
#weight of hidden neural network 2, connecting to output.
weight3 = tf.Variable(tf.random_normal([n_hidden_2, n_classes])
