# Deep Learning with PyTorch on CIFAR-10

## Project Overview
This project implements a complete deep learning pipeline for image classification on the CIFAR-10 dataset using PyTorch. It demonstrates:
- Custom Dataset class and DataLoader implementation
- CNN architecture (from scratch and transfer learning with ResNet18)
- Training and validation loops with loss/accuracy tracking
- Experimentation with optimizers, learning rates, and data augmentation
- Logging with TensorBoard and model checkpointing

The goal is to build a modular, well-documented codebase that can be used as a portfolio piece and a foundation for further experiments.

## Dataset: CIFAR-10
- **Classes:** 10 (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck)
- **Image size:** 32x32 pixels, RGB
- **Training samples:** 50,000
- **Test samples:** 10,000

The dataset is automatically downloaded when you first run the code.

## Configuration
You can modify hyperparameters and experiment settings in src/config.py. Alternatively, you can extend the script to accept command‑line arguments (e.g., using argparse). Current editable options include:
* Model type (simple_cnn or resnet18)
* Optimizer (adam, sgd)
* Learning rate, batch size, number of epochs
* Data augmentation toggle
* Example with future argument support:


``` bash
python src/train.py --model resnet18 --lr 0.01 --augmentation 
```

## Experiments and Results
I conducted several experiments to compare the impact of different optimizers, learning rates, and data augmentation. The table below summarises the test accuracies achieved after 20 epochs.

| Experiment | Optimizer | Learning Rate | Augmentation | Test Accuracy |
|------------|-----------|---------------|--------------|---------------|
| 1          | Adam      | 0.001         | No           | 75.2%         |
| 2          | SGD       | 0.01          | Yes          | 82.5%         |
| 3          | Adam      | 0.0001        | Yes          | 78.1%         |
| 4          | SGD       | 0.1           | No           | 70.3%         |
| 5          | Adam      | 0.001         | Yes          | 80.4%         |

## Key Findings
- Data augmentation (random crops and horizontal flips) consistently improved accuracy by ~5% across all optimizers.
- SGD with momentum (0.9) and a learning rate of 0.01 generalised better than Adam for this task, possibly due to its regularising effect.
- Lower learning rates (0.0001) slowed convergence, while higher rates (0.1) caused instability.
- Transfer learning with ResNet18 (pretrained on ImageNet) achieved the highest accuracy of **88.3%** after fine‑tuning for 20 epochs.

## Model Checkpoints
During training, model checkpoints are saved every 5 epochs in the `models/` directory. The final model is saved as `models/final_model.pth`. You can load a checkpoint for inference or to resume training:

```python
import torch
from src.model import SimpleCNN

model = SimpleCNN()
checkpoint = torch.load('models/checkpoint_epoch20.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

```

