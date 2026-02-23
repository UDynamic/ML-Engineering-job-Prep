import torch
from torch.utils.data import Dataset
import torchvision
import torchvision.transforms as transforms
import numpy as np

class CIFAR10Dataset(Dataset):
    """Custom Dataset for CIFAR-10."""
    def __init__(self, root='./data', train=True, transform=None):
        self.data = torchvision.datasets.CIFAR10(
            root=root, train=train, download=True, transform=transform
        )
        # If you want to truly customise, you can load the raw data and apply transforms manually.
        # But here we simply wrap the built-in dataset for simplicity.
        # For a genuine custom example, you could override __getitem__ to load images from disk.
        # However, the built-in already does that.

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image, label = self.data[idx]
        # image is already a PIL image, and transform was applied in __init__
        return image, label