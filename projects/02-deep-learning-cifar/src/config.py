# config.py
import torchvision.transforms as transforms

# Basic transforms (for baseline)
basic_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))  # CIFAR-10 stats
])

# Augmented transforms for training
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

# Test transform (no augmentation)
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])


config = {
    'model': 'resnet18',   # or 'simple_cnn'
    'pretrained': True,
    'batch_size': 64,
    'epochs': 20,
    'optimizer': 'adam',
    'lr': 0.001,
    'momentum': 0.9,
    'weight_decay': 5e-4,
    'augmentation': True,
    'log_dir': 'runs/exp1'
}