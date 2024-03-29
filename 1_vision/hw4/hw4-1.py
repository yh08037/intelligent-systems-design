# ID: 2018115809 (undergraduate)
# NAME: Dohun Kim
# File name: hw4-1.py
# Platform: Python 3.7.4 on Ubuntu Linux 18.04
# Required Package(s): sys, os, gzip, numpy=1.19.2, matplotlib=3.3.4

'''
hw4-1.py :
    classification of Fashion MNIST dataset with `TwoLayerNet`
'''

############################## import required packages ##############################
# coding: utf-8
import sys, os
sys.path.append(os.pardir)

import numpy as np
from two_layer_net import TwoLayerNet

import matplotlib.pyplot as plt


############################# define data loader function ############################

def load_fashion_mnist(path, kind='train'):
    '''
    original code is found at:
    https://github.com/zalandoresearch/fashion-mnist/blob/master/utils/mnist_reader.py
    '''
    import os
    import gzip

    """Load Fashion MNIST data from `path`"""
    labels_path = os.path.join(path, '%s-labels-idx1-ubyte.gz' % kind)
    images_path = os.path.join(path, '%s-images-idx3-ubyte.gz' % kind)

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels


################################### preparing data ###################################

# load data from gzip files
x_train, t_train = load_fashion_mnist('./', 'train')
x_test,  t_test  = load_fashion_mnist('./', 't10k')

# normalization of input data
x_train = x_train / 255.
x_test  = x_test  / 255.

# one-hot encoding
num_label = np.unique(t_train, axis=0).shape[0]
t_train = np.eye(num_label)[t_train]
t_test  = np.eye(num_label)[t_test]


################################# train and test model ################################

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

iters_num = 3000
train_size = x_train.shape[0]
batch_size = 256
learning_rate = 0.1

iter_per_epoch = max(int(train_size / batch_size), 1)

train_loss_list = []
train_acc_list = []
test_acc_list = []


for i in range(iters_num):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]
    
    # 기울기 계산
    # grad = network.numerical_gradient(x_batch, t_batch) # 수치 미분 방식
    grad = network.gradient(x_batch, t_batch) # 오차역전파법 방식(훨씬 빠르다)
    
    # 갱신
    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate * grad[key]
    
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)
    
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)

        print('iter %-5d\ttrain_acc: %-3.2f%%\ttest_acc: %-3.2f%%' 
              %(i, train_acc*100, test_acc*100))


################################# plot learning curve #################################

plt.title('Accuracy - Train vs Test')
plt.plot(train_acc_list, label='train accuracy')
plt.plot(test_acc_list, label='test_accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()