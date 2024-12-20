from typing import Annotated
from constants import homepage
from fastapi.responses import HTMLResponse
from lib import validate_netcdf_files, debug_import_data
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return debug_import_data(files)

@app.get("/")
async def main():
    return HTMLResponse(content=homepage)