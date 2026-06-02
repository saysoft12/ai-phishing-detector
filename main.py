from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Request model
class EmailRequest(BaseModel):
    email_text: str

# API endpoint
@app.get("/")
def home():
    return FileResponse("static/index.html")
@app.post("/analyze")
def analyze_email(request: EmailRequest):

    prompt = f"""
    Analyze this email for phishing risk.

    Email:
    {request.email_text}

    Return the result in this JSON format:

    {{
      "risk_level": "",
      "explanation": "",
      "recommended_action": ""
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    # Remove markdown formatting
    cleaned_result = result.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to dictionary
    parsed_result = json.loads(cleaned_result)

    return {"analysis": parsed_result}