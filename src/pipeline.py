import tensorflow as tf
import prettytensor as pt
import numpy as np
import scipy.io as io
import argparse
import models
import sys
import os
import data_loader

from constants import *
from progressbar import ETA, Bar, Percentage, ProgressBar
from sklearn.metrics import precision_recall_curve, average_precision_score

np.random.seed(1234)
tf.set_random_seed(0)

parser = argparse.ArgumentParser(description='Epidemic Response System')
parser.add_argument('-wd', '--working_directory', help='directory for storing logs')
parser.add_argument('-sf', '--save_frequency', help='Number of epochs before saving')
parser.add_argument('--model_path', help='Stored model path')
parser.add_argument('mode', choices=('train', 'eval'), help='train or eval')
args = parser.parse_args()

# Training Constants
learning_rate = 1e-4
batch_size = 1
num_timesteps = 4
num_feats = 3
max_epoch = 601
dataset_size = 3726 
updates_per_epoch = int(np.ceil(float(dataset_size) / float(batch_size)))

if args.working_directory:
    working_directory = args.working_directory
else:
    working_directory = 'trial/'
if args.save_frequency:
    save_frequency = args.save_frequency
else:
    save_frequency = 200
if args.model_path:
    model_path = args.model_path
else:
    model_path = 'trial/checkpoints/model.ckpt-600'

def get_loss(pred, gt):
    return tf.div(tf.sqrt(tf.reduce_mean(tf.square(tf.sub(gt, pred)))),
                  tf.constant(float(batch_size)))

def train():
    with tf.device('/gpu:0'): # run on specific device
        input_tensor, pred, gt = models.import_model(num_timesteps, 
                                                     num_feats,
                                                     batch_size)
        loss = get_loss(pred, gt)
        optimizer = tf.train.AdamOptimizer(learning_rate, epsilon=1.0)
        train = optimizer.minimize(loss=loss)

    dataset = data_loader.read_datasets(PREPROCESSED_DATA)
    saver = tf.train.Saver()  # defaults to saving all variables

    # logging the loss function
    loss_placeholder = tf.placeholder(tf.float32)
    tf.scalar_summary('train_loss', loss_placeholder)

    merged = tf.merge_all_summaries()

    init = tf.initialize_all_variables()
    
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        writer = tf.train.SummaryWriter(os.path.join(working_directory, 'logs'),
                sess.graph_def)
        sess.run(init)

        for epoch in range(max_epoch):
            training_loss = 0.0

            widgets = ["epoch #%d|" % epoch, Percentage(), Bar(), ETA()]
            pbar = ProgressBar(updates_per_epoch, widgets=widgets)
            pbar.start()
            for i in range(updates_per_epoch):
                pbar.update(i)
                input_batch, gt_batch = dataset.next_batch(batch_size)
                _, loss_value = sess.run([train, loss], 
                                         {input_tensor : input_batch,
                                          gt : gt_batch})
                training_loss += np.sum(loss_value)

            training_loss = training_loss/(updates_per_epoch)
            print("Loss %f" % training_loss)
            
            # save model
            if epoch % save_frequency == 0:
                checkpoints_folder = os.path.join(working_directory, 'checkpoints')
                if not os.path.exists(checkpoints_folder):
                    os.makedirs(checkpoints_folder)
                saver.save(sess, os.path.join(checkpoints_folder, 'model.ckpt'),
                           global_step=epoch)

                # save summaries
                summary_str = sess.run(merged, 
                              feed_dict={input_tensor : input_batch,
                                         gt : gt_batch,
                                         loss_placeholder: training_loss})
                writer.add_summary(summary_str, global_step=epoch)
        writer.close()

def evaluate(print_grid=False):
    with tf.device('/gpu:0'): # run on specific device
        input_tensor, pred, gt = models.import_model(num_timesteps, 
                                                     num_feats,
                                                     batch_size)

    dataset = data_loader.read_datasets(PREPROCESSED_DATA, dataset_type='test')

    saver = tf.train.Saver() 
    
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        saver.restore(sess, model_path)

        all_pred, all_gt = [], []
        for i in range(updates_per_epoch):
            input_batch, gt_batch = dataset.next_batch(batch_size)
            pred_value = sess.run([pred], 
                                  {input_tensor : input_batch,
                                   gt : gt_batch})

            all_pred.append(pred_value)
            all_gt.append(gt_batch)

        num_align = 0
        for i in range(len(all_pred)):
            if all_pred[i] == all_gt[i]: num_align += 1
        print "Accuracy:", float(num_align)/len(all_pred)

if __name__ == "__main__":
    if args.mode == 'train':
        train()
    elif args.mode == 'eval':
        evaluate(print_grid=False)
