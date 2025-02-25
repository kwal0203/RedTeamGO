# RedTeamGO API Examples

This directory contains example scripts demonstrating how to use the RedTeamGO API endpoints for toxicity and bias detection.

## Prerequisites

```bash
pip install requests
```

## Available Examples

1. **Toxicity Detection Batch** (`toxicity_batch_example.py`)
   - Tests multiple prompts for toxicity
   - Uses both database prompts and user-provided prompts
   - Supports different topics and random sampling

2. **Bias Detection Batch** (`bias_batch_example.py`)
   - Tests for various types of bias in model responses
   - Uses prompt libraries
   - Supports multiple bias topics (gender, race, religion, etc.)

3. **Realtime Detection** (`realtime_examples.py`)
   - Tests both toxicity and bias detection in real-time
   - Simulates chat-like scenarios
   - Quick single-prompt analysis

## Usage

Make sure the RedTeamGO service is running (via Docker Compose) before running the examples.

```bash
# Run toxicity batch example
python toxicity_batch_example.py

# Run bias batch example
python bias_batch_example.py

# Run realtime detection examples
python realtime_examples.py
```

## API Endpoints

- `POST /toxicity-detection-batch`: Batch toxicity analysis
- `POST /bias-detection-batch`: Batch bias analysis
- `POST /toxicity-detection-realtime`: Real-time toxicity check
- `POST /bias-detection-realtime`: Real-time bias check
- `GET /health`: Service health check

## Response Formats

### Batch Endpoints
```json
{
    "result": {
        // Analysis results specific to the detection type
    }
}
```

### Realtime Endpoints
```json
{
    "result": "string"
}
```

## Error Handling

All examples include basic error handling for:
- Connection errors
- Invalid responses
- Server errors

## Note

The realtime endpoints are currently marked as "NOT_IMPLEMENTED" in the API. The examples show the expected usage once these endpoints are fully implemented.