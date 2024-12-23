from typing import Annotated
from constants import homepage
from fastapi.responses import HTMLResponse
from lib import detect_thermal_anomalies
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

@app.post("/detect_thermal_anomalies/")
async def detect_thermal_anomalies_controller(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    results = await detect_thermal_anomalies(files)
    return results

@app.get("/")
async def main():
    return HTMLResponse(content=homepage)