from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

app = FastAPI()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-001')

AGENT_CARD = {
    "name": "TradingAgent",
    "description": "Agent for analyzing trade viability and market fit",
    "url": "http://localhost:8001/a2a",
    "version": "1.0",
    "skills": ["trade_analysis", "market_trends"],
    "authentication": {"schemes": ["API-Key"]}
}

API_KEY = "trade-key"

@app.get("/.well-known/agent.json")
async def get_agent_card():
    return AGENT_CARD

class JsonRpcRequest(BaseModel):
    jsonrpc: str
    method: str
    params: dict
    id: int

@app.post("/a2a")
async def a2a_endpoint(request: Request, json_rpc: JsonRpcRequest):
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if json_rpc.method == "tasks/send":
        task = json_rpc.params["task"]
        trade_details = task["messages"][0]["parts"][0]["content"]
        
        prompt = f"""
        You are a financial trading expert. Analyze the following trade details: {trade_details}.
        Focus on market fit, potential profitability, and alignment with current market trends.
        Provide a concise analysis (100-150 words) including:
        - Whether the trade seems viable based on market conditions.
        - Potential upside or challenges.
        - A brief recommendation (e.g., proceed, adjust, avoid).
        If specific market data is unavailable, make reasonable assumptions based on general trading principles.
        """
        
        try:
            response = model.generate_content(prompt)
            if response.candidates:
                response_text = response.candidates[0].content.parts[0].text
            else:
                response_text = "Content generation failed or was blocked."
        except Exception as e:
            response_text = f"Error generating content: {str(e)}"
        
        response_task = {
            "id": task["id"],
            "status": "completed",
            "messages": task["messages"] + [
                {"role": "agent", "parts": [{"type": "text", "content": response_text}]}
            ],
            "artifacts": [{"parts": [{"type": "text", "content": response_text}]}]
        }
        return {"jsonrpc": "2.0", "result": {"task": response_task}, "id": json_rpc.id}
    else:
        raise HTTPException(status_code=400, detail="Method not supported")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)