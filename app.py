from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from dotenv import load_dotenv

from groq import Groq

import os

import joblib

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

model = joblib.load("model.pkl")

app = FastAPI(title="Student Performance Predictor")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class Student(BaseModel):
    studytime: int
    failures: int
    absences: int
    G1: int
    G2: int


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/generate")
async def generate(student: Student):

    data = [[
        student.studytime,
        student.failures,
        student.absences,
        student.G1,
        student.G2
    ]]

    prediction = model.predict(data)[0]

    if prediction == 1:
        result = "PASS"
    else:
        result = "FAIL"

    prompt = f"""
A student's prediction result is {result}.

Study Time:
{student.studytime}

Failures:
{student.failures}

Absences:
{student.absences}

Previous Marks:
{student.G1}
{student.G2}

Give motivation and study advice in 100 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    advice = response.choices[0].message.content

    return {
        "prediction": result,
        "advice": advice
    }