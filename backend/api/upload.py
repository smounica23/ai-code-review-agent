from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter()

EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".ts": "typescript",
    ".cpp": "cpp",
    ".c": "c",
    ".html": "html",
    ".css": "css",
    ".sql": "sql",
}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    filename = file.filename
    if not filename:
        raise HTTPException(
            status_code = 400,
            detail = "File name not found"
        )
    
    extension = Path(filename).suffix.lower()
    language = EXTENSION_LANGUAGE_MAP.get(extension)

    file_bytes = await file.read()

    try:
        code = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to decode file. Please upload a valid text/code file."
        )

    return {
        "filename": filename,
        "extension": extension,
        "language": language,
        "code": code
    }


