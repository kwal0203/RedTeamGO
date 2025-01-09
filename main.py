from fastapi import FastAPI
from utils.models import *
from utils.utils import *
from services.toxicity_detection_automated.service import (
    toxicity_detection_service,
)
from services.bias_detection_dbias.service import dbias_service

# # Replace with LiteLLM
# from dotenv import load_dotenv
# import os

# load_dotenv()

# API_KEY = os.getenv("OPENAI_API_KEY")
# DEVICE = os.getenv("DEVICE")

app = FastAPI()


@app.post("/toxicity-detection-batch", response_model=ResultBatch)
def toxicity_detection_batch(args: DetectionBatchToxicity):
    print("----- toxicity_detection_batch")
    toxicity_result = toxicity_detection_service(**args.model_dump())
    return ResultBatch(result=toxicity_result)


@app.post("/bias-detection-batch", response_model=ResultBatch)
def bias_detection_batch(args: DetectionBatchBias):
    print("----- bias_detection_batch")
    dbias_result = dbias_service(**args.model_dump())
    return ResultBatch(result=dbias_result)


@app.post("/toxicity-detection-realtime", response_model=ResultRealtime)
def toxicity_detection_realtime(args: UserPrompt):
    print("toxicity_detection_realtime not implemented")


@app.post("/bias-detection-realtime", response_model=ResultRealtime)
def bias_detection_realtime(args: UserPrompt):
    print("bias_detection_realtime not implemented")


@app.get("/")
def read_root():
    return {"service": "online"}
