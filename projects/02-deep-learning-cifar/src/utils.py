import torch
from torch.utils.data import DataLoader
from src.dataset import CIFAR10Dataset
from src.config import train_transform, test_transform

def get_data_loaders(batch_size=64, num_workers=2):
    """Create and return train and test DataLoaders."""
    train_dataset = CIFAR10Dataset(root='./data', train=True, transform=train_transform)
    test_dataset = CIFAR10Dataset(root='./data', train=False, transform=test_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return train_loader, test_loader

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