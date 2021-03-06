import os
import sys
import time

import matplotlib
import numpy as np
import tensorflow as tf

from opentidal.data_provider import DataProvider
from opentidal.rnn_model import RNNModel

DEFAULT_MODEL_PATH = os.path.join('models', 'tidal.ckpt')
DEFAULT_DATASET_NAME = 'tidal'

LOGGING_FREQUENCY = 100

# Hyperparams
BATCH_SIZE = 32
SEQUENCE_LENGTH = 25
LEARNING_RATE = 0.01
DECAY_RATE = 0.97
HIDDEN_LAYER_SIZE = 256
CELLS_SIZE = 2


def train(model_path, num_epochs=1000, resume=True):
    data_provider = DataProvider(DEFAULT_DATASET_NAME, BATCH_SIZE,
                                 SEQUENCE_LENGTH)
    model = RNNModel(data_provider.vocabulary_size,
                     batch_size=BATCH_SIZE,
                     sequence_length=SEQUENCE_LENGTH,
                     hidden_layer_size=HIDDEN_LAYER_SIZE,
                     cells_size=CELLS_SIZE)

    with tf.Session() as sess:
        saver = tf.train.Saver()

        summaries = tf.summary.merge_all()
        #writer = tf.summary.FileWriter(tensorboard_dir)
        #writer.add_graph(sess.graph)
        sess.run(tf.global_variables_initializer())

        if resume and os.path.exists(model_path):
            saver.restore(sess, model_path)
            print("Model restored.")

        temp_losses = []
        smooth_losses = []

        for epoch in range(num_epochs):
            sess.run(
                tf.assign(model.learning_rate,
                          LEARNING_RATE * (DECAY_RATE**epoch)))
            data_provider.reset_batch_pointer()
            state = sess.run(model.initial_state)
            for batch in range(data_provider.batches_size):
                inputs, targets = data_provider.next_batch()
                feed = {model.input_data: inputs, model.targets: targets}
                for index, (c, h) in enumerate(model.initial_state):
                    feed[c] = state[index].c
                    feed[h] = state[index].h
                iteration = epoch * data_provider.batches_size + batch
                summary, loss, state, _ = sess.run(
                    [summaries, model.cost, model.final_state, model.train_op],
                    feed)
                #writer.add_summary(summary, iteration)
                temp_losses.append(loss)

                if iteration % LOGGING_FREQUENCY == 0:
                    smooth_loss = np.mean(temp_losses)
                    smooth_losses.append(smooth_loss)
                    temp_losses = []
                    #plot(smooth_losses, "iterations (thousands)", "loss")
                    print('{{"metric": "iteration", "value": {}}}'.format(
                        iteration))
                    print('{{"metric": "epoch", "value": {}}}'.format(epoch))
                    print('{{"metric": "loss", "value": {}}}'.format(
                        smooth_loss))

        # Save the variables to disk.
        path = saver.save(sess, model_path)
        print("Model saved in path: {}".format(path))


def predict(model_path, sample_length=500, num_samples=1):
    #if not os.path.exists(model_path):
    #raise RuntimeError("{} not found".format(model_path))

    tf.reset_default_graph()

    data_provider = DataProvider(DEFAULT_DATASET_NAME, BATCH_SIZE,
                                 SEQUENCE_LENGTH)
    model = RNNModel(data_provider.vocabulary_size,
                     batch_size=1,
                     sequence_length=1,
                     hidden_layer_size=HIDDEN_LAYER_SIZE,
                     cells_size=CELLS_SIZE,
                     training=False)

    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, model_path)

        res = []
        for _ in range(num_samples):
            text = model.sample(sess, data_provider.chars,
                                data_provider.vocabulary, sample_length)
            res.append(text)
        return res
