from torch.utils.data import DataLoader
from src.dataset import CIFAR10Dataset
from src.config import train_transform, test_transform

train_dataset = CIFAR10Dataset(root='./data', train=True, transform=train_transform)
test_dataset  = CIFAR10Dataset(root='./data', train=False, transform=test_transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=2)
test_loader  = DataLoader(test_dataset, batch_size=64, shuffle=False, num_workers=2)