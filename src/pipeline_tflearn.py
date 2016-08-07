import tensorflow as tf
import tflearn
import numpy as np

import datetime

from data_utils import *


def train_model():
    X_train, X_test, y_train, y_test = np.load(PREPROCESSED_DATA)
    num_samples, num_timesteps, input_dim = X_train.shape
    net = tflearn.input_data(shape=[None, num_timesteps, input_dim])
    net = tflearn.lstm(net, 128)
    net = tflearn.fully_connected(net, 1, activation='relu')
    net = tflearn.regression(net, optimizer='sgd',
                             loss='mean_square', name="regression_output")
    model = tflearn.DNN(net, tensorboard_verbose=2, run_id=)
    model.fit(X_train, y_train, n_epoch=1, validation_set=0.1, show_metric=True,
              snapshot_step=100)



if __name__ == '__main__':
    train_model()