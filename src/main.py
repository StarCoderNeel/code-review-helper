"""Main application module for code-review-helper."""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Code Review Helper",
    description="An AI-powered code review tool that provides real-time feedback on code quality, security, and best practices. The tool integrates with version control systems to analyze code changes.",
    version="0.1.0"
)

class HealthResponse(BaseModel):
    status: str
    version: str

class RequestData(BaseModel):
    input_text: str

class ResponseData(BaseModel):
    output: str
    status: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")

@app.post("/process", response_model=ResponseData)
async def process_data(request: RequestData):
    """Process input data."""
    try:
        if not request.input_text or not request.input_text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty")
        
        result = f"Processed: {request.input_text}"
        return ResponseData(output=result, status="success")
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Update 1: Development iteration 1
