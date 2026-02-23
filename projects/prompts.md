
---

### Task 1: Classic ML Pipeline

```markdown
I'm working on my ML engineering job preparation portfolio. I have a monorepo structure with a folder `projects/01-classic-ml-pipeline`. My goal is to build an end-to-end ML pipeline on a benchmark dataset (like House Prices or Titanic). I need step-by-step guidance to:

- Perform exploratory data analysis (EDA) with visualizations.
- Handle missing values, encode categorical features, and scale numeric features.
- Train multiple models (linear regression, random forest, XGBoost) with cross-validation.
- Evaluate and select the best model using appropriate metrics.
- Save the model and document results in a clear README.

Please guide me through each step, including code snippets and best practices. I'm using a virtual environment with pandas, numpy, matplotlib, seaborn, scikit-learn, and Jupyter. I want to produce clean, well-documented code that I can commit to my repo.
```

---

### Task 2: Deep Learning with PyTorch

```markdown
I'm continuing my ML engineering portfolio. Next, I need to complete Task 2: Deep Learning with PyTorch on CIFAR-10. The project folder is `projects/02-deep-learning-cifar`. I want step-by-step guidance to:

- Implement a custom Dataset class and DataLoader.
- Define a CNN architecture (or use transfer learning with a pretrained model like ResNet).
- Write training and validation loops with loss and accuracy tracking.
- Experiment with different optimizers, learning rates, and data augmentation.
- Log results (manually or with TensorBoard) and save model weights.
- Document everything in a README.

I have PyTorch installed. Please help me structure the code and explain key concepts along the way.
```

---

### Task 3: Model Serving with FastAPI & Docker

```markdown
For Task 3 of my ML engineering portfolio, I need to serve a trained model via a REST API using FastAPI and containerize it with Docker. The project folder is `projects/03-model-serving-fastapi`. I have a model saved from a previous task (e.g., the House Prices model). I want step-by-step guidance to:

- Write a FastAPI app with a `/predict` endpoint that accepts JSON input and returns predictions.
- Create a `Dockerfile` that installs dependencies and runs the app.
- Test the API locally with `curl` or Postman.
- Document the API and Docker usage in a README.

I have FastAPI, uvicorn, and Docker installed. Please guide me through the process, including error handling and best practices for production-ready APIs.
```

---

### Task 4: Cloud Deployment

```markdown
I'm ready for Task 4: deploying my containerized model to a cloud platform. The project folder is `projects/04-cloud-deployment`. I have a Docker image from Task 3. I need step-by-step guidance to:

- Push the Docker image to a registry (e.g., Docker Hub).
- Deploy to a cloud platform (I'd like to try AWS, but I'm open to GCP or Azure if easier).
- Test the public endpoint.
- Document the deployment steps, costs, and any challenges.

Please walk me through the deployment process, including setting up cloud CLI tools, creating resources, and making the service accessible.
```

---

### Task 5: CI/CD for ML with GitHub Actions

```markdown
Task 5 is about setting up CI/CD for an ML project using GitHub Actions. The project folder is `projects/05-ci-cd-github-actions`. I want to add automated testing and validation to one of my existing projects (e.g., the classic ML pipeline). I need step-by-step guidance to:

- Write unit tests with pytest for data processing and model prediction.
- Create a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs tests on every push.
- Optionally, add a step to validate model performance against a baseline.
- Add a status badge to the README.

I have pytest installed. Please help me design meaningful tests and set up the workflow correctly.
```

---

### Task 6: RAG with LangChain & Ollama

```markdown
For Task 6, I want to build a Retrieval-Augmented Generation (RAG) system using LangChain and a local LLM via Ollama. The project folder is `projects/06-rag-langchain`. I need step-by-step guidance to:

- Install and set up Ollama with a small model (e.g., Llama 3 8B).
- Use LangChain to load documents (e.g., PDFs), split them, and create embeddings.
- Store embeddings in a vector database (Chroma or FAISS).
- Build a query interface that retrieves relevant chunks and generates answers.
- Document the system with a README and possibly a demo video.

I have langchain, chromadb, and other dependencies installed. Please guide me through the implementation, explaining the concepts along the way.
```

---

### Task 7: Experiment Tracking with MLflow

```markdown
Task 7 is about implementing experiment tracking with MLflow. The project folder is `projects/07-mlflow-tracking`. I want to instrument one of my training scripts (e.g., the deep learning task) to log parameters, metrics, and artifacts. I need step-by-step guidance to:

- Add MLflow logging to the training script (log hyperparameters, loss/accuracy curves, and model artifacts).
- Start the MLflow UI and compare runs.
- Register the best model in the model registry.
- Load the registered model for inference.
- Document the setup and results.

I have MLflow installed. Please show me how to structure the code and use MLflow effectively.
```

---

### Task 8: Data Pipeline with Airflow

```markdown
For Task 8, I need to build an automated data pipeline using Apache Airflow (or a simpler alternative if Airflow is overkill). The project folder is `projects/08-data-pipeline`. I want to simulate a real-world scenario: periodically fetch data from an API (e.g., weather or stock prices), clean it, and store it in a database or CSV. I need step-by-step guidance to:

- Set up Airflow locally (or use a lightweight scheduler like `schedule` if Airflow is too heavy).
- Write a DAG (or script) that fetches, processes, and stores data.
- Handle incremental updates and error handling.
- Document the pipeline architecture and how to run it.

I have Apache Airflow installed in a separate virtual environment. Please guide me through the process, keeping it practical for a portfolio.
```

---

### Task 9: Testing for ML

```markdown
Task 9 focuses on writing comprehensive tests for ML code. The project folder is `projects/09-testing`. I want to take a module from one of my projects (e.g., data preprocessing or model inference) and write thorough tests. I need step-by-step guidance to:

- Write unit tests for data validation (e.g., expected columns, data types).
- Test model prediction shape and range.
- Test edge cases (empty input, missing values).
- Mock external dependencies (e.g., API calls, database connections).
- Achieve good code coverage and document the testing strategy.

I have pytest and pytest-mock installed. Please help me design and implement these tests.
```

---

### Task 10: Open Source Contribution

```markdown
For the final task, Task 10, I want to make my first open source contribution to an ML-related project. The project folder is `projects/10-open-source-contribution`. I need step-by-step guidance to:

- Find a beginner-friendly issue in a project (e.g., scikit-learn, PyTorch, Hugging Face, or a smaller library).
- Understand the codebase and set up the development environment.
- Implement a fix or improvement.
- Submit a pull request and engage with maintainers.
- Document the experience and lessons learned.

Please advise me on how to choose a suitable project, navigate the contribution process, and make a meaningful contribution.
```