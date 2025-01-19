import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel, field_validator, ConfigDict
from redis import asyncio
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from datetime import datetime
from typing import List
import numpy as np

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    top_k=None,
)

logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://localhost:6379"


@asynccontextmanager
async def lifespan(app: FastAPI):
    HOST_URL = os.environ.get("REDIS_URL", LOCAL_REDIS_URL)
    logger.debug(HOST_URL)
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache-project")

    yield


sub_application_sentiment_predict = FastAPI(lifespan=lifespan)

# Define the /health endpoint as a GET request
# My original health endpoint
# @sub_application_sentiment_predict.get("/health")
# async def health():
#     current_time = datetime.now().isoformat()  # Get current time in ISO8601 format
#     return {"time": current_time}

# Provided health endpoint
@sub_application_sentiment_predict.get("/health")
async def health():
    return {"status": "healthy"}

@sub_application_sentiment_predict.get("/hello")
async def hello(name: str=Query(..., description="The name to greet")):
        return {"message": f"Hello {name}"}


class SentimentRequest(BaseModel):
    text: List[str]

    @field_validator('text')
    def check_non_empty(cls, v):
        if not v:
            raise ValueError('The list of sentiment text cannot be empty')
        return v

    def cust_to_numpy(self) -> np.ndarray:
        # Transform the houses into a numpy array
        array = np.array(self.text)
        # Log the array for debugging purposes
        print("Transformed input array for prediction:", array)
        return array

class Sentiment(BaseModel):
    label: str # ("POSITIVE", "NEGATIVE")
    score: float # Confidence Score for Label

class SentimentResponse(BaseModel):
    predictions: List[List[Sentiment]]


@sub_application_sentiment_predict.post(
    "/bulk-predict", response_model=SentimentResponse
)
@cache(expire=60)
async def predict(sentiments: SentimentRequest):
    # Make prediction
    if model is None:
        raise ValueError("Model not loaded. Please check the loading process.")
    
    # Transform raw predictions into the required format
    predictions = [
        [{"label": p["label"], "score": p["score"]} for p in raw_predictions]
        for raw_predictions in classifier(sentiments.text)
    ]
    
    return {"predictions": predictions}

