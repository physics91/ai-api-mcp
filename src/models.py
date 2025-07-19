from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum


class AIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROK = "grok"


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str
    provider: Optional[AIProvider] = None
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    stream: Optional[bool] = False
    
    
class ChatResponse(BaseModel):
    content: str
    model: str
    provider: AIProvider
    usage: Optional[Dict[str, int]] = None
    

class ModelInfo(BaseModel):
    id: str
    name: str
    provider: AIProvider
    description: Optional[str] = None
    context_window: Optional[int] = None
    max_output_tokens: Optional[int] = None
    supported_features: List[str] = Field(default_factory=list)


class CompareRequest(BaseModel):
    prompt: str
    models: List[str]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, gt=0)


class CompareResponse(BaseModel):
    responses: List[ChatResponse]
    prompt: str
    

class AnalyzeRequest(BaseModel):
    content: str
    analysis_type: Literal["code", "text", "security", "performance", "general"]
    model: str
    provider: Optional[AIProvider] = None
    

class GenerateRequest(BaseModel):
    prompt: str
    generation_type: Literal["code", "text", "documentation", "test"]
    model: str
    provider: Optional[AIProvider] = None
    language: Optional[str] = None
    framework: Optional[str] = None