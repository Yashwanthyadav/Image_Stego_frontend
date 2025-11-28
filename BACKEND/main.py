from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import uuid
import os
from stego import encode_image, decode_image

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/encode")
async def encode_api(message: str = Form(...), image: UploadFile = File(...)):
    image_id = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{image_id}.png"
    output_path = f"{OUTPUT_DIR}/{image_id}_encoded.png"

    with open(input_path, "wb") as f:
        f.write(await image.read())

    encode_image(input_path, message, output_path)
    return FileResponse(output_path, media_type="image/png", filename="encoded.png")

@app.post("/decode")
async def decode_api(image: UploadFile = File(...)):
    image_id = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{image_id}.png"

    with open(input_path, "wb") as f:
        f.write(await image.read())

    decoded = decode_image(input_path)
    return {"message": decoded}
