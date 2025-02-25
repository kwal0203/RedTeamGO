from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from utils.models import *
from utils.utils import *
from services.toxicity_detection.service import (
    toxicity_detection_service,
)
from services.bias_detection_dbias.service import dbias_service

# Create FastAPI app
app = FastAPI()

# Set up Prometheus instrumentation
Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/toxicity-detection-batch", response_model=ResultBatch)
def toxicity_detection_batch(args: DetectionBatchToxicity):
    print("----- toxicity_detection_batch")
    toxicity_result = toxicity_detection_service(**args.model_dump())
    return ResultBatch(result=toxicity_result)


@app.post("/bias-detection-batch", response_model=ResultBatch)
def bias_detection_batch(args: DetectionBatchBias):
    print("----- bias_detection_batch")
    dbias_result = dbias_service(**args.model_dump())
    return ResultBatch(result={"result": "NOT_IMPLEMENTED_BIAS"})


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
