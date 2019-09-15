from random import sample


class Dataset:
    def __init__(self, path):
        self.path = path

    def append(sample):
        with open(path, 'a+') as f:
            f.write(sample + "\n\n")

    def get_samples(num_samples):
        with open(path, 'r') as f:
            dataset = f.read()
            samples = dataset.split("\n\n")
            return sample(samples, num_samples)