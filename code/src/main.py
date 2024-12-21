from typing import Annotated
from constants import homepage
from fastapi.responses import HTMLResponse
from lib import debug_import_data
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

@app.post("/detect_thermal_anomalies/")
async def debug_input_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    results = await debug_import_data(files)
    return results

@app.get("/")
async def main():
    return HTMLResponse(content=homepage)