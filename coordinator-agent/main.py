import httpx
import uuid
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-001')

agent_urls = ["http://localhost:8001", "http://localhost:8002"]
agent_cards = {}
api_keys = {
    "http://localhost:8001": "trade-key",
    "http://localhost:8002": "risk-key"
}

class TradeRequest(BaseModel):
    trade_details: str

for url in agent_urls:
    try:
        response = httpx.get(f"{url}/.well-known/agent.json")
        if response.status_code == 200:
            agent_cards[url] = response.json()
        else:
            print(f"Failed to discover agent at {url}")
    except Exception as e:
        print(f"Error discovering agent at {url}: {e}")

@app.post("/analyze-trade")
async def analyze_trade(trade_request: TradeRequest):
    user_input = trade_request.trade_details
    
    # Prepare tasks for both agents
    trade_task_id = f"task-{uuid.uuid4()}"
    risk_task_id = f"task-{uuid.uuid4()}"
    request_body = {
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "params": {
            "task": {
                "id": trade_task_id,
                "messages": [
                    {"role": "user", "parts": [{"type": "text", "content": user_input}]}
                ]
            }
        },
        "id": 1
    }
    trade_response = None
    risk_response = None
    
    try:
        trade_url = agent_cards["http://localhost:8001"]["url"]
        response = httpx.post(trade_url, json=request_body, headers={"X-API-Key": api_keys["http://localhost:8001"]})
        if response.status_code == 200:
            result = response.json()
            trade_response = result["result"]["task"]["artifacts"][0]["parts"][0]["content"]
        else:
            trade_response = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        trade_response = f"Error communicating with Trading Agent: {e}"
    
    request_body["params"]["task"]["id"] = risk_task_id
    try:
        risk_url = agent_cards["http://localhost:8002"]["url"]
        response = httpx.post(risk_url, json=request_body, headers={"X-API-Key": api_keys["http://localhost:8002"]})
        if response.status_code == 200:
            result = response.json()
            risk_response = result["result"]["task"]["artifacts"][0]["parts"][0]["content"]
        else:
            risk_response = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        risk_response = f"Error communicating with Risk Agent: {e}"
    
    prompt = f"""
    You are a financial advisor. Based on the following analyses, determine if the trade '{user_input}' is good or not.
    - Trading Agent Analysis: {trade_response}
    - Risk Agent Analysis: {risk_response}
    Provide a concise decision (100-150 words) including:
    - Whether the trade is recommended (good, cautious, or not recommended).
    - Key factors influencing the decision.
    - Any suggested adjustments (if applicable).
    """
    
    try:
        response = model.generate_content(prompt)
        if response.candidates:
            final_decision = response.candidates[0].content.parts[0].text
        else:
            final_decision = "Failed to generate final decision."
    except Exception as e:
        final_decision = f"Error generating final decision: {str(e)}"
    
    return {
        "trade_analysis": trade_response,
        "risk_analysis": risk_response,
        "final_decision": final_decision
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)