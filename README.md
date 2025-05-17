# A2A Project

## Overview

This repo intends to implement the Google A2A Protocol at a basic level by implementing a trading analysis platform.
We will be using A2A to let our 3 agents communicate with each other, the agents are : 
The platform consists of:
1. Coordinator Agent: Central controller that receives trade requests, distributes them to specialized agents, and synthesizes a final recommendation
2. Trading Agent: Analyzes trade details for market opportunity and technical factors
3. Risk Agent: Evaluates potential risks associated with the proposed trade

## Installation & Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/sayantann7/A2A.git
    ```
2. Install dependencies:
    ```bash
    pip install fastapi uvicorn google-generativeai python-dotenv
    ```
3. Visit https://aistudio.google.com/ and Create your Gemini API Key and store it inside 3 .env files inside user-agent, info-agent, creative-agent directories

4. Start the Trading Agent:
    ```bash
    cd trading-agent
    python main.py
    ```
5. Start the Risk Agent:
    ```bash
    cd risk-agent
    python main.py
    ```
6. Start the Coordinator Agent:
    ```bash
    cd coordinator-agent
    python main.py
    ```
7. Open a new terminal and start the Frontend:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
8. Open another Terminal and Navigate to the Frontend directory and start the client:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
9. Now open your browser and navigate to http://localhost:3000 to start analyzing trades

## How It Works
1. Users enter trade details in the frontend interface (e.g., "Buy 100 shares of AAPL at $200, stop-loss $190, target $220")
2. The coordinator agent receives this request and forwards it to both specialized agents
3. The trading agent analyzes market opportunity, technical factors, and potential upside
4. The risk agent evaluates potential downside, volatility concerns, and risk factors
5. The coordinator collects both analyses and uses Gemini AI to synthesize a final recommendation
6. All three analyses (trading, risk, and final decision) are displayed to the user in a modern, responsive interface