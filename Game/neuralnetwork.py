#from __future__ import print_function
#import data !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#maybe make a matrix of possible outcomes to import and learn from.
#example?
#  |
#  |
#  |
#  |x
#  |x
#  |x 0
#  |x 0          0
#   _ _ _ _ _ _ _
#reward X + 1 0 -1
#from ? import input_data
#? = input_data.read_data_sets("/tmp/data", one_hot=False)





import tensorflow as tf

#construction phase
boardRow = 6
boardHeight = 7

# Traning Prams
#learn rate
learning_rate = 0.3

#steps of training to rn
#num_steps = 2000
batch_size = 100
num_steps = int(np.ceil(m / batch_size))

#network parameters.
n_hidden_1 = 256
n_hidden_2 = 100
#2 hidden layers, 356 neurons. 
n_input = boardRow * boardHeight
# n_input = 42
n_classes = 100 #output but i don't know what the number should be. 


#input dataplace holders
X = tf.placeholder(tf.float32, [None, n_input])
#output dataplaceholder
Y = tf.placeholder(tf.float32, [None, n_classes])



model = n_input * X + Y
error = tf.square(model - model)


#
#
#
#
#
#     GPU1                    GPU2
#            _______                 ________
#           |   X   |     |          |  Y   |
#           |______|      |          | _____|
#               |         |             |
#               |         |             |
#              42(X)                   100(Y)
#
#
#
#
#
#

#namescope loss




#weights don't work yet idk why

#weight of hidden layer connect to input layer.
weight1 = tf.Variable(tf.random_normal([n_input, n_hidden_1]))
#weight of hidden neural network 1 connecting to hidden neural network 2.
weight2 = tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2]))
#weight of hidden neural network 2, connecting to output.
weight3 = tf.Variable(tf.random_normal([n_hidden_2, n_classes])
                      

#bias

#                    Y 
#                  ______
#                    |  
#                    |  
#                    |  
#                    |  
#                 ___|______ 
#       Bias -----  |____|
#      bias1         |
#      bias2         |
#      bias3         |
#                    | 
#                    |
#     weights      __|___   
#     weight1  --  |____|   
#     weight2        |
#     weight3        |
#                  __|____
#                  | X  |               
#                  |____|
                      
#learn with graident descent                     
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate) 
opt_op = opt.minmize(error)
opt_op.run() #initalize varaibles
                      
                      

                      
                      
#execution phase
                      
                      
#fetch mini-batch
                      
#def fetch_batch(epoch, batch_index, batch_size):
