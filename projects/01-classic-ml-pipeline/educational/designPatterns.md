Here’s a complete guide to **Factory**, **Strategy**, and **Template** design patterns — three of the most useful patterns in object‑oriented design.  
You’ll learn what they are, when to use them, see memorable code snippets, and understand how to choose between them.

---

## 1. Factory Pattern (Creational)

### Introduction
The **Factory** pattern provides an interface for creating objects without specifying their concrete classes. It shifts the responsibility of instantiation from the client to a dedicated factory class or method.  
There are two common variations:

- **Factory Method** – defines an abstract method in a base class that subclasses override to create specific objects.
- **Abstract Factory** – provides an interface for creating families of related objects.

### When to Use
- You don’t know the exact type of object you need until runtime.
- You want to centralise and decouple object creation logic.
- You need to enforce that objects follow a common interface.

### Memorable Code Snippet (Factory Method)
```python
from abc import ABC, abstractmethod

# Product
class Transport(ABC):
    @abstractmethod
    def deliver(self): pass

class Truck(Transport):
    def deliver(self): return "Deliver by land"

class Ship(Transport):
    def deliver(self): return "Deliver by sea"

# Creator with factory method
class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:   # factory method
        pass

    def plan_delivery(self):
        transport = self.create_transport()
        return transport.deliver()

class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()

class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()

# Client
logistics = RoadLogistics()
print(logistics.plan_delivery())   # "Deliver by land"
```
**Key takeaway:** The factory method (`create_transport`) lets subclasses decide which concrete product to instantiate.

---

## 2. Strategy Pattern (Behavioral)

### Introduction
The **Strategy** pattern defines a family of interchangeable algorithms, encapsulates each one, and makes them swappable at runtime. It separates the algorithm from the context that uses it.

### When to Use
- You have multiple ways to perform an operation and want to switch between them dynamically.
- You want to avoid conditional statements (if/else, switch) for selecting behaviour.
- The algorithm’s code should be isolated from the context to make it easier to maintain and extend.

### Memorable Code Snippet
```python
from abc import ABC, abstractmethod

# Strategy interface
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): pass

# Concrete strategies
class BubbleSort(SortStrategy):
    def sort(self, data):
        return sorted(data)   # pretend bubble sort

class QuickSort(SortStrategy):
    def sort(self, data):
        return sorted(data)   # pretend quick sort

# Context
class DataProcessor:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def process(self, data):
        return self._strategy.sort(data)

# Client
processor = DataProcessor(BubbleSort())
print(processor.process([3, 1, 2]))   # uses bubble sort

processor.set_strategy(QuickSort())
print(processor.process([3, 1, 2]))   # now uses quick sort
```
**Key takeaway:** The context holds a reference to a strategy object and delegates work to it. Strategies are interchangeable.

---

## 3. Template Method Pattern (Behavioral)

### Introduction
The **Template Method** pattern defines the skeleton of an algorithm in a base class method, deferring some steps to subclasses. Subclasses can redefine certain steps without changing the algorithm’s structure.

### When to Use
- You have an algorithm with invariant parts and variant parts.
- You want to avoid code duplication by pulling common behaviour into a base class.
- You need to control which steps subclasses are allowed to override (often using hooks).

### Memorable Code Snippet
```python
from abc import ABC, abstractmethod

class DataMiner(ABC):
    # Template method
    def mine(self, path):
        file = self.open_file(path)
        data = self.extract_data(file)
        parsed = self.parse_data(data)
        self.analyze(parsed)
        self.send_report()
        self.close_file(file)

    # Steps that may vary
    def open_file(self, path):    # concrete step
        return open(path, 'r')

    @abstractmethod
    def extract_data(self, file): pass

    @abstractmethod
    def parse_data(self, raw): pass

    # Hook (optional override)
    def analyze(self, parsed):
        pass

    # Hook
    def send_report(self):
        print("Report sent")

    def close_file(self, file):   # concrete step
        file.close()

class PDFMiner(DataMiner):
    def extract_data(self, file):
        return "raw pdf content"

    def parse_data(self, raw):
        return "parsed pdf data"

class CSVMiner(DataMiner):
    def extract_data(self, file):
        return "raw csv content"

    def parse_data(self, raw):
        return "parsed csv data"

# Client
miner = PDFMiner()
miner.mine("file.pdf")
```
**Key takeaway:** The template method (`mine`) defines the algorithm structure; subclasses implement the abstract steps, but cannot change the overall flow.

---

## Comparative Analysis: How to Choose

| Aspect                | Factory (Method)                          | Strategy                                 | Template Method                          |
|-----------------------|-------------------------------------------|------------------------------------------|------------------------------------------|
| **Purpose**           | Object creation                           | Algorithm selection and swapping         | Algorithm skeleton with customisable steps |
| **Scope**             | Creational                                | Behavioral                               | Behavioral                               |
| **Main mechanism**    | Inheritance (subclass overrides factory method) | Composition (context holds strategy)    | Inheritance (subclass implements abstract steps) |
| **When to use**       | You need to instantiate different subclasses based on context | You have multiple interchangeable behaviours that change at runtime | You have a fixed algorithm but want to let subclasses override specific parts |
| **Change point**      | The type of object created                 | The algorithm used by the context        | The implementation of certain steps      |
| **Example scenario**  | A logistics app that creates trucks or ships depending on the region | A payment system that can use credit card, PayPal, or crypto | A data mining framework where file formats differ but the overall process is the same |

### Decision Guide
- **Use Factory** when your primary challenge is **how objects are created**. It hides the instantiation logic and lets the client work with an interface rather than concrete classes.
- **Use Strategy** when you need to **vary an entire algorithm** and possibly switch it at runtime. It’s perfect for eliminating conditional logic and making algorithms reusable.
- **Use Template Method** when you have an **invariant algorithm structure** but want to give subclasses the ability to **customise certain steps**. It’s a way to reuse code while controlling the degree of customisation.

### Can they be combined?
Yes, often! For example:
- A **Factory** can create **Strategy** objects.
- A **Template Method** can call a factory method to obtain objects needed for the algorithm.

Understanding these three patterns gives you a powerful toolbox for writing flexible, maintainable code.