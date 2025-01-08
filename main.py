from fastapi import FastAPI
from models import *
from utils import *
from services.toxicity_detection_automated.service import (
    automated_toxicity_detection_service,
)
from services.bias_detection_dbias.service import dbias_service

# Replace with LiteLLM
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()


@app.post("/toxicity-detection-batch", response_model=ResultBatch)
def toxicity_detection_batch(args: DetectionBatchToxicity):
    print("----- toxicity_detection_batch")

    prompts = args.prompts
    model = args.model

    print(f"  Model:   {model}")
    print(f"  Prompts: {prompts[0]}")

    automated_result = automated_toxicity_detection_service(args=args)
    result_batch = {**automated_result}

    return ResultBatch(result=result_batch)


@app.post("/bias-detection-batch", response_model=ResultBatch)
def bias_detection_batch(args: DetectionBatchBias):
    print("----- bias_detection_batch")

    prompts = args.prompts
    model = args.model

    print(f"  Model:   {model}")
    print(f"  Prompts: {prompts[0]}")

    dbias_result = dbias_service(args=args)
    result_batch = {**dbias_result}

    return ResultBatch(result=result_batch)


@app.post("/toxicity-detection-realtime", response_model=ResultRealtime)
def toxicity_detection_realtime(args: UserPrompt):
    print("toxicity_detection_realtime not implemented")


@app.post("/bias-detection-realtime", response_model=ResultRealtime)
def bias_detection_realtime(args: UserPrompt):
    print("bias_detection_realtime not implemented")


@app.get("/")
def read_root():
    return {"service": "online"}
