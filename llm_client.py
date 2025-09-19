from openai import OpenAI
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.openai_client = None
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialize OpenAI client if API key is available"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            self.openai_client = OpenAI(api_key=api_key)
    
    async def generate_chat_completion(
        self,
        message: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 150,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Generate a chat completion using OpenAI's API"""
        
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        # Prepare messages
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": model,
                "tokens_used": response.usage.total_tokens if response.usage else None,
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            raise ValueError(f"Error generating completion: {str(e)}")
    
    async def generate_text_completion(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo-instruct",
        temperature: float = 0.7,
        max_tokens: int = 150
    ) -> Dict[str, Any]:
        """Generate a text completion (legacy completions endpoint)"""
        
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            response = self.openai_client.completions.create(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "response": response.choices[0].text.strip(),
                "model": model,
                "tokens_used": response.usage.total_tokens if response.usage else None,
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            raise ValueError(f"Error generating completion: {str(e)}")

# Global LLM client instance
llm_client = LLMClient()