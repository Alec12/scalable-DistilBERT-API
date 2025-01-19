# **End-to-End ML Sentiment Analysis API**

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

## **Overview**
This repository hosts an end-to-end machine learning API for sentiment analysis using **HuggingFace’s DistilBERT** model. The API predicts whether input text has a **positive** or **negative** sentiment and provides confidence scores. Deployed on **Azure Kubernetes Service (AKS)**, the application is built with **FastAPI**, containerized with **Docker**, and optimized for performance with **Redis** caching and **k6** load testing.

---

## **Core Features**
- Efficient **DistilBERT**-based sentiment analysis using HuggingFace Transformers.
- **FastAPI** application serving batched predictions via a user-friendly REST API.
- Scalable deployments with **Kubernetes** for development (Minikube) and production (AKS).
- Optimized latency with **Redis** caching and robust load testing using **k6**.
- Real-time monitoring and resource utilization insights via **Grafana** dashboards.

---

## **How It Works**
1. **Text Input**: Submit a batch of text inputs (e.g., `["I love you", "I hate you"]`).
2. **Sentiment Prediction**: Receive a confidence score for **POSITIVE** and **NEGATIVE** sentiments for each text.
3. **High Scalability**: Supports increased traffic through Kubernetes horizontal scaling and baked-in model optimizations.

---

## **For Setup and Deployment**
Detailed setup instructions, deployment steps for **Minikube** and **AKS**, and API testing guidelines are provided in the [detailed README](mlapi/README.md).

---

## **Key Performance Metrics**
- Achieves ~40 requests per second with 99th-percentile latency below 2 seconds during load testing.
- Minimal resource usage spikes observed, even with a finetuned **DistilBERT** model.

![K6 Summary Statistics](mlapi/k6_performance_summary.png "K6 Performance Metrics")

---

## **Technologies Used**
- **HuggingFace Transformers** for pre-trained model inference.
- **FastAPI** for lightweight, high-performance RESTful API development.
- **Pydantic** for robust input/output data validation and serialization.
- **Docker** for containerization and portability.
- **Kubernetes** (Minikube for development, AKS for production) for orchestration.
- **Redis** for caching frequently accessed data.
- **k6** for stress testing and performance optimization.
- **Grafana** for system monitoring and resource utilization insights.

---

## **Get Started**
To get started, clone the repository and follow the setup steps provided in the detailed guide: [Full End-to-End ML API Setup Guide](mlapi/README.md).