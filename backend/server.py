from fastapi import FastAPI, File, UploadFile
from fastmcp import FastMCP
import zipfile, os, shutil, uuid

app = FastAPI()
mcp = FastMCP("FileOrganizer")

# Tool stub for classification—fill in AI logic later
@mcp.tool
def classify_file(file_path: str) -> str:
    # TODO: call LLM to determine category
    name = os.path.splitext(os.path.basename(file_path))[0].lower()
    if 'essay' in name: return "English"
    if 'calc' in name or 'diff' in name: return "Math"
    return "Misc"

app.mount("/mcp", mcp.app)

@app.post("/upload")
async def upload_zip(file: UploadFile = File(...)):
    temp_dir = f"tmp/{uuid.uuid4()}"
    out_dir = f"{temp_dir}/organized"
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    zip_path = f"{temp_dir}/upload.zip"
    with open(zip_path, "wb") as buffer:
        buffer.write(await file.read())

    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)

    # Classify & sort
    for fname in os.listdir(temp_dir):
        full = os.path.join(temp_dir, fname)
        if os.path.isfile(full):
            category = classify_file(full)
            dest = os.path.join(out_dir, category)
            os.makedirs(dest, exist_ok=True)
            shutil.move(full, os.path.join(dest, fname))

    # Re-zip organized directory
    out_zip = f"{temp_dir}/organized.zip"
    shutil.make_archive(out_zip.replace('.zip',''), 'zip', out_dir)

    return FastAPI().send_file(out_zip, media_type='application/zip')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)