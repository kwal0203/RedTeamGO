from fastapi import FastAPI
from utils.models import *
from utils.utils import *
from services.toxicity_detection.service import (
    toxicity_detection_service,
)
from services.bias_detection_dbias.service import dbias_service

app = FastAPI()


@app.post("/toxicity-detection-batch", response_model=ResultBatch)
def toxicity_detection_batch(args: DetectionBatchToxicity):
    print("----- toxicity_detection_batch")
    # TODO: Check the structure of the model dump
    model_dump = args.model_dump()
    print(model_dump)
    toxicity_result = toxicity_detection_service(**args.model_dump())
    # toxicity_result = {"response": "NOT IMPLEMENTED"}
    # TODO: How do I want to process the raw toxicity evaluations?
    return ResultBatch(result=toxicity_result)


@app.post("/bias-detection-batch", response_model=ResultBatch)
def bias_detection_batch(args: DetectionBatchBias):
    print("----- bias_detection_batch")
    dbias_result = dbias_service(**args.model_dump())
    return ResultBatch(result={"result": "NOT_IMPLEMENTED"})


@app.post("/toxicity-detection-realtime", response_model=ResultRealtime)
def toxicity_detection_realtime(args: UserPrompt):
    print("toxicity_detection_realtime not implemented")
    return ResultRealtime(result="NOT_IMPLEMENTED")


@app.post("/bias-detection-realtime", response_model=ResultRealtime)
def bias_detection_realtime(args: UserPrompt):
    print("bias_detection_realtime not implemented")
    return ResultRealtime(result="NOT_IMPLEMENTED")


@app.get("/")
def read_root():
    return {"service": "online"}
