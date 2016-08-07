import tensorflow as tf
import prettytensor as pt
import numpy as np

def import_model(_num_timesteps, _grid_size, _batch_size):
    global num_timesteps
    global grid_size
    global batch_size
    num_timesteps = _num_timesteps
    grid_size = _grid_size
    batch_size = _batch_size
    return network()

def fc_layers(input_tensor, size):
    return (pt.wrap(input_tensor).
            fully_connected(256, name='common_fc1').
            fully_connected(size*size, name='common_fc2').
            reshape([size, size])).tensor

def network_grid(input_tensor):    
    return (pt.wrap(input_tensor).
            conv2d(3, 2, stride=1).
            conv2d(5, 5, stride=1).
            flatten().
            fully_connected(128, name='grid_fc1')).tensor

def network_rnn(rnn_inputs):
    return (pt.wrap(rnn_inputs).
            cleave_sequence(num_timesteps).
            sequence_lstm(64).
            squash_sequence())[num_timesteps - 1,:]

def network(): 
    dim_0, dim_1, dim_2 = grid_size
    gt = tf.placeholder(tf.float32, [dim_0, dim_1])
    input_tensor = tf.placeholder(tf.float32, [num_timesteps, dim_0, dim_1, dim_2])
    mask = tf.placeholder(tf.float32, [dim_0, dim_1])

    assert(num_timesteps > 1)
    with tf.variable_scope("model") as scope:
        with pt.defaults_scope(activation_fn=tf.nn.relu,
                               batch_normalize=True,
                               learned_moments_update_rate=0.0003,
                               variance_epsilon=0.001,
                               scale_after_normalization=True):
            enc = network_grid(input_tensor)
            rnn_feats = network_rnn(enc)
            rnn_feats = tf.reshape(rnn_feats, [1, 64])
            pred = fc_layers(rnn_feats, dim_0)

    return input_tensor, pred, gt, mask
