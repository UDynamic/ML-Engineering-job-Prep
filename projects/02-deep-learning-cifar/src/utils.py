from torch.utils.data import DataLoader
from src.dataset import CIFAR10Dataset
from src.config import train_transform, test_transform

train_dataset = CIFAR10Dataset(root='./data', train=True, transform=train_transform)
test_dataset  = CIFAR10Dataset(root='./data', train=False, transform=test_transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=2)
test_loader  = DataLoader(test_dataset, batch_size=64, shuffle=False, num_workers=2)

# 
import torch

def accuracy(outputs, labels):
    _, preds = torch.max(outputs, 1)
    return torch.sum(preds == labels).item() / len(labels)

def save_checkpoint(model, optimizer, epoch, filename):
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, filename)
    print(f"Checkpoint saved to {filename}")