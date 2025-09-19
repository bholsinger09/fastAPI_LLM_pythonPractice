from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, AsyncGenerator
import json
import asyncio
from llm_client import llm_client

router = APIRouter(prefix="/advanced", tags=["Advanced Endpoints"])

class StreamRequest(BaseModel):
    message: str
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 200

class SummarizeRequest(BaseModel):
    text: str
    model: Optional[str] = "gpt-3.5-turbo"
    max_tokens: Optional[int] = 150

class TranslateRequest(BaseModel):
    text: str
    source_language: Optional[str] = "auto"
    target_language: str = "English"
    model: Optional[str] = "gpt-3.5-turbo"

async def simulate_streaming_response(text: str) -> AsyncGenerator[str, None]:
    """Simulate streaming response by yielding words with delay"""
    words = text.split()
    for i, word in enumerate(words):
        chunk = {
            "delta": {"content": word + " "},
            "index": i,
            "finish_reason": None if i < len(words) - 1 else "stop"
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.1)  # Simulate streaming delay
    
    # Send final chunk
    final_chunk = {"delta": {"content": ""}, "index": len(words), "finish_reason": "stop"}
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"

@router.post("/stream")
async def stream_chat(request: StreamRequest):
    """Stream a chat response word by word"""
    try:
        # Generate full response first (in a real implementation, you'd use OpenAI's streaming)
        result = await llm_client.generate_chat_completion(
            message=request.message,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return StreamingResponse(
            simulate_streaming_response(result["response"]),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        error_chunk = {"error": str(e)}
        async def error_stream():
            yield f"data: {json.dumps(error_chunk)}\n\n"
        
        return StreamingResponse(error_stream(), media_type="text/plain")

@router.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    """Summarize the provided text"""
    try:
        prompt = f"Please provide a concise summary of the following text:\n\n{request.text}\n\nSummary:"
        
        result = await llm_client.generate_chat_completion(
            message=prompt,
            model=request.model,
            max_tokens=request.max_tokens
        )
        
        return {
            "summary": result["response"],
            "original_length": len(request.text.split()),
            "summary_length": len(result["response"].split()),
            "model": result["model"],
            "tokens_used": result["tokens_used"]
        }
    
    except Exception as e:
        return {"error": str(e)}

@router.post("/translate")
async def translate_text(request: TranslateRequest):
    """Translate text between languages"""
    try:
        if request.source_language == "auto":
            prompt = f"Translate the following text to {request.target_language}:\n\n{request.text}"
        else:
            prompt = f"Translate the following text from {request.source_language} to {request.target_language}:\n\n{request.text}"
        
        result = await llm_client.generate_chat_completion(
            message=prompt,
            model=request.model,
            max_tokens=len(request.text.split()) * 2 + 50  # Rough estimation
        )
        
        return {
            "translated_text": result["response"],
            "source_language": request.source_language,
            "target_language": request.target_language,
            "model": result["model"],
            "tokens_used": result["tokens_used"]
        }
    
    except Exception as e:
        return {"error": str(e)}

@router.get("/models")
async def list_available_models():
    """List available LLM models"""
    return {
        "chat_models": [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-4",
            "gpt-4-1106-preview"
        ],
        "text_models": [
            "gpt-3.5-turbo-instruct"
        ],
        "note": "Availability depends on your OpenAI API access level"
    }