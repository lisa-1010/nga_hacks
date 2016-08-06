import tensorflow as tf
import prettytensor as pt
import numpy as np

def import_model(_num_timesteps, _len_feats, _batch_size):
    global num_timesteps
    global len_feats
    global batch_size
    num_timesteps = _num_timesteps
    len_feats = _len_feats
    batch_size = _batch_size
    return network()

def fc_layers(input_tensor):
    return (pt.wrap(input_tensor).
            fully_connected(100, name='fc1').
            fully_connected(1, name='fc2')).tensor

def rnn(rnn_inputs):
    return (pt.wrap(rnn_inputs).
            cleave_sequence(num_timesteps).
            sequence_lstm(128).
            squash_sequence())[num_timesteps - 1,:]

def network(): 
    gt = tf.placeholder(tf.float32, [batch_size, 1])     
    input_tensor = tf.placeholder(tf.float32,
                                    [batch_size, num_timesteps, len_feats])

    assert(num_timesteps > 1)
    with tf.variable_scope("model") as scope:
        with pt.defaults_scope(activation_fn=tf.nn.relu,
                               batch_normalize=True,
                               learned_moments_update_rate=0.0003,
                               variance_epsilon=0.001,
                               scale_after_normalization=True):
            rnn_feats = rnn(input_tensor) # dim = [batch_size, hidden]
    pred = fc_layers(rnn_feats)

    return input_tensor, pred, gt
