import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 8 * 8, 512)   # after two poolings: 32 -> 16 -> 8
        self.fc2 = nn.Linear(512, num_classes)
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)               # flatten
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
    
    
""" Option B: Transfer Learning (ResNet18)

import torchvision.models as models

def get_resnet18(pretrained=True, num_classes=10):
    model = models.resnet18(pretrained=pretrained)
    # Replace the final fully connected layer for CIFAR-10 (10 classes)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model

"""