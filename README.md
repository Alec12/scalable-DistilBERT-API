# Full End-to-End Machine Learning API

<!-- markdownlint-disable MD028 -->

<p align="center">
    <!--Hugging Face-->
        <img src="https://user-images.githubusercontent.com/1393562/197941700-78283534-4e68-4429-bf94-dce7ab43a941.svg" width=7% alt="Hugging Face">
    <!--PLUS SIGN-->
        <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--FASTAPI-->
        <img src="https://user-images.githubusercontent.com/1393562/190876570-16dff98d-ccea-4a57-86ef-a161539074d6.svg" width=7% alt="FastAPI">
    <!--PLUS SIGN-->
        <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--REDIS LOGO-->
        <img src="https://user-images.githubusercontent.com/1393562/190876644-501591b7-809b-469f-b039-bb1a287ed36f.svg" width=7% alt="Redis">
    <!--PLUS SIGN-->
        <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--KUBERNETES-->
        <img src="https://user-images.githubusercontent.com/1393562/190876683-9c9d4f44-b9b2-46f0-a631-308e5a079847.svg" width=7% alt="Kubernetes">
    <!--PLUS SIGN-->
        <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--Azure-->
        <img src="https://user-images.githubusercontent.com/1393562/192114198-ac03d0ef-7fb7-4c12-aba6-2ee37fc2dcc8.svg" width=7% alt="Azure">
    <!--PLUS SIGN-->
        <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--k6-->
        <img src="https://user-images.githubusercontent.com/1393562/197683208-7a531396-6cf2-4703-8037-26e29935fc1a.svg" width=7% alt="K6">
    <!--PLUS SIGN-->
        <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width=7% alt="Plus">
    <!--GRAFANA-->
        <img src="https://user-images.githubusercontent.com/1393562/197682977-ff2ffb72-cd96-4f92-94d9-2624e29098ee.svg" width=7% alt="Grafana">
</p>


# **Sentiment Analysis API**

## **Overview**
This project demonstrates the deployment of a fully functional machine learning API for sentiment analysis using the **DistilBERT** model. The API accepts text inputs and provides predictions on whether the sentiment is **positive** or **negative** with confidence scores for each label. Built using **FastAPI**, the application is containerized with **Docker** and deployed on **Azure Kubernetes Service (AKS)** for scalability and performance.

---

## **Features**
- Accepts batched text input and returns sentiment predictions with confidence scores.
- Leverages the **HuggingFace Transformers** library for simplified model inference.
- Designed for efficient CPU-based inference with pre-trained **DistilBERT** hosted on HuggingFace.
- Includes robust input/output validation with **Pydantic models**.
- Supports horizontal scaling with Kubernetes and caching with **Redis** to minimize latency.
- Tested with **k6** for load testing and monitored using **Grafana** for performance insights.

---

## **API Specifications**

### **Input Model**
The API accepts input in the following format:

```json
{
    "text": ["example 1", "example 2"]
}
```

### **Output Model**
The API returns predictions in the following format:

```json
{
    "predictions": [
        [
            {
                "label": "POSITIVE",
                "score": 0.7127904295921326
            },
            {
                "label": "NEGATIVE",
                "score": 0.2872096002101898
            }
        ],
        [
            {
                "label": "POSITIVE",
                "score": 0.7186233401298523
            },
            {
                "label": "NEGATIVE",
                "score": 0.2813767194747925
            }
        ]
    ]
}
```

---

## **Setup and Deployment**

### **1. Prerequisites**
- Install dependencies with **Poetry**:
  ```bash
  poetry install
  ```
- Pull the pre-trained DistilBERT model locally:
  ```bash
  git lfs install
  git clone https://huggingface.co/winegarj/distilbert-base-uncased-finetuned-sst2
  ```
  Add the model files to `.gitignore` to avoid unnecessary commits.

### **2. Running Locally**
- Build and deploy the application locally using **kustomize**:
  ```bash
  kustomize build overlays/dev | kubectl apply -f -
  ```

### **3. Deployment to AKS**
- Push the Docker image to **Azure Container Registry (ACR)**:
  ```bash
  docker build -t <acr_namespace>/project:latest .
  docker push <acr_namespace>/project:latest
  ```
- Deploy the application to **Azure Kubernetes Service**:
  - Adjust the `kustomize` virtual service to route paths for `/project` and `/lab`.
  - Apply the updated configuration:
    ```bash
    kubectl apply -k overlays/prod
    ```

---

## **Testing and Monitoring**

### **1. Unit Testing**
- Ensure the application works as expected with **pytest**:
  ```bash
  poetry run pytest
  ```

### **2. Load Testing**
- Test API performance using **k6** with the provided `load.js` script:
  ```bash
  k6 run load.js
  ```

### **3. Monitoring**
- Use **Grafana** to monitor system performance during load testing.
- Capture key metrics such as latency, request rates, and resource utilization.

---

## **Model Background**
The model is based on **DistilBERT**, fine-tuned for sentiment analysis. It was trained on a GPU-enabled system using two A4000 GPUs with the following configuration:
- **Batch size**: 256
- **Sequence length**: Up to 512 tokens
- **Training time**: 5 minutes

Training on CPUs is not recommended due to the significant computational requirements. The HuggingFace Transformers library provides a pre-configured prediction pipeline for efficient inference.

### See `mlapi` for API development