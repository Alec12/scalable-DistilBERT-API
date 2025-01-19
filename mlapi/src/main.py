from contextlib import AsyncExitStack

from fastapi import FastAPI

from src.sentiment_predict import lifespan, sub_application_sentiment_predict


async def main_lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        # Manage the lifecycle of sub_app
        await stack.enter_async_context(lifespan(sub_application_sentiment_predict))
        yield


app = FastAPI(lifespan=main_lifespan)


app.mount("/project", sub_application_sentiment_predict)
