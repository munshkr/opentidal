import codecs
import collections
import os
import random

import numpy as np


class DataProvider:
    def __init__(self, data_dir, batch_size, sequence_length):
        self.batch_size = batch_size
        self.data_path = os.path.join('data', data_dir, "input.txt")
        self.sequence_length = sequence_length
        with codecs.open(self.data_path, "r", encoding="utf-8") as file:
            data = file.read()
        count_pairs = sorted(collections.Counter(data).items(),
                             key=lambda x: -x[1])
        self.pointer = 0
        self.chars, _ = zip(*count_pairs)
        # FIXME usar vocabulario fijo para reutilizar modelo
        self.vocabulary_size = len(self.chars)
        self.vocabulary = dict(zip(self.chars, range(len(self.chars))))
        self.tensor = np.array(list(map(self.vocabulary.get, data)))
        self.batches_size = int(self.tensor.size /
                                (self.batch_size * self.sequence_length))
        if self.batches_size == 0:
            assert False, "Unable to generate batches. Reduce batch_size or sequence_length."

        self.tensor = self.tensor[:self.batches_size * self.batch_size *
                                  self.sequence_length]
        inputs = self.tensor
        targets = np.copy(self.tensor)

        targets[:-1] = inputs[1:]
        targets[-1] = inputs[0]
        self.input_batches = np.split(inputs.reshape(self.batch_size, -1),
                                      self.batches_size, 1)
        self.target_batches = np.split(targets.reshape(self.batch_size, -1),
                                       self.batches_size, 1)
        print("Tensor size: " + str(self.tensor.size))
        print("Batch size: " + str(self.batch_size))
        print("Sequence length: " + str(self.sequence_length))
        print("Batches size: " + str(self.batches_size))
        print("")

    def next_batch(self):
        inputs = self.input_batches[self.pointer]
        targets = self.target_batches[self.pointer]
        self.pointer += 1
        return inputs, targets

    def reset_batch_pointer(self):
        self.pointer = 0

    def append(self, sample):
        with codecs.open(self.data_path, 'a+') as f:
            f.write(sample.strip() + "\n")

    def get_samples(self, num_samples):
        with codecs.open(self.data_path, 'r') as f:
            dataset = f.read()
            samples = [s.strip() for s in dataset.split("\n")]
            return random.sample(samples, num_samples)
