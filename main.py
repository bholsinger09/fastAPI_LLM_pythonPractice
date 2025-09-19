from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
from llm_client import llm_client
from advanced_endpoints import router as advanced_router
from middleware import rate_limit_middleware, error_handler_middleware, validate_temperature, validate_max_tokens, validate_model

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="FastAPI LLM API",
    description="A FastAPI application integrated with Large Language Models for learning purposes",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include advanced endpoints
app.include_router(advanced_router)

# Add middleware (order matters - later middleware wraps earlier ones)
app.middleware("http")(error_handler_middleware)
app.middleware("http")(rate_limit_middleware)

# Pydantic models for request/response
class HealthResponse(BaseModel):
    status: str
    message: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="The message to send to the LLM")
    model: Optional[str] = Field(default="gpt-3.5-turbo", description="The model to use for completion")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=150, ge=1, le=4000, description="Maximum tokens to generate")
    
    @validator('model')
    def validate_model_field(cls, v):
        return validate_model(v)

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: Optional[int] = None

class TextRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000, description="The prompt for text completion")
    model: Optional[str] = Field(default="gpt-3.5-turbo-instruct", description="The model to use for completion")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=150, ge=1, le=4000, description="Maximum tokens to generate")
    
    @validator('model')
    def validate_model_field(cls, v):
        return validate_model(v)

class ConversationRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="The message to send")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default=None, description="Previous conversation history")
    model: Optional[str] = Field(default="gpt-3.5-turbo", description="The model to use for completion")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=150, ge=1, le=4000, description="Maximum tokens to generate")
    
    @validator('model')
    def validate_model_field(cls, v):
        return validate_model(v)
    
    @validator('conversation_history')
    def validate_history(cls, v):
        if v is not None:
            if len(v) > 20:  # Limit conversation history
                raise ValueError('conversation_history cannot exceed 20 messages')
            for msg in v:
                if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                    raise ValueError('Each message must have "role" and "content" fields')
                if msg['role'] not in ['user', 'assistant', 'system']:
                    raise ValueError('Role must be "user", "assistant", or "system"')
        return v

# Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="success",
        message="FastAPI LLM API is running!"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is operational"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """Generate a simple chat completion"""
    try:
        result = await llm_client.generate_chat_completion(
            message=request.message,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            response=result["response"],
            model=result["model"],
            tokens_used=result["tokens_used"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/text", response_model=ChatResponse)
async def text_completion(request: TextRequest):
    """Generate a text completion"""
    try:
        result = await llm_client.generate_text_completion(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            response=result["response"],
            model=result["model"],
            tokens_used=result["tokens_used"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/conversation", response_model=ChatResponse)
async def conversation_completion(request: ConversationRequest):
    """Generate a chat completion with conversation history"""
    try:
        result = await llm_client.generate_chat_completion(
            message=request.message,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            response=result["response"],
            model=result["model"],
            tokens_used=result["tokens_used"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)