import tensorflow as tf
import tflearn
import numpy as np

from data_utils import *




def train_model():
    X_train, X_test, y_train, y_test = np.load(PREPROCESSED_DATA)
    net = tflearn.input_data(shape=[None, 28, 28])
    net = tflearn.lstm(net, 128, return_seq=True)
    net = tflearn.lstm(net, 128)
    net = tflearn.fully_connected(net, 10, activation='softmax')
    net = tflearn.regression(net, optimizer='adam',
                             loss='categorical_crossentropy', name="output1")
    model = tflearn.DNN(net, tensorboard_verbose=2)
    model.fit(X_train, y_train, n_epoch=1, validation_set=0.1, show_metric=True,
              snapshot_step=100)