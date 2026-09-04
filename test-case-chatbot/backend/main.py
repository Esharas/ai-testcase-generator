from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.ai_service import generate_test_cases
from backend.excel_exporter import export_test_cases_to_excel
from backend.ai_service import analyze_requirement

import os
import uuid


app = FastAPI()


class Requirement(BaseModel):
    requirement: str


class ExcelRequest(BaseModel):
    test_cases: list


@app.get("/")
def home():

    return {
        "message": "Test Case Generator API is running"
    }
# ---------------------------------------
# Analys the requirment
# ---------------------------------------

@app.post("/analyze-requirement")
def analyze(requirement: Requirement):

    try:

        analysis = analyze_requirement(
            requirement.requirement
        )

        return {
            "analysis": analysis
        }

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ---------------------------------------
# Generate test cases using Gemini
# ---------------------------------------

@app.post("/generate-testcases")
def generate(requirement: Requirement):

    try:

        test_cases = generate_test_cases(
            requirement.requirement
        )

        return {
            "test_cases": test_cases
        }

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------
# Create Excel from EXISTING test cases
# ---------------------------------------

@app.post("/generate-excel")
def generate_excel(request: ExcelRequest):

    try:

        # Create generated folder
        os.makedirs(
            "generated",
            exist_ok=True
        )

        # Unique temporary filename
        filename = (
            f"test_cases_{uuid.uuid4().hex}.xlsx"
        )

        output_path = os.path.join(
            "generated",
            filename
        )

        # Create Excel using the SAME test cases
        export_test_cases_to_excel(
            request.test_cases,
            output_path
        )

        return FileResponse(
            path=output_path,
            filename="Generated_Test_Cases.xlsx",
            media_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )

    except Exception as e:

        print("EXCEL ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )