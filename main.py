import os
from random import randint
from pyngrok import ngrok
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles




from api.endpoints import segmentation
from core.config import TEMP_FILES, TRAINING_RESULTS_FOLDER, STATIC_FILES


os.environ['nnUNet_preprocessed'] = os.path.join(TEMP_FILES, 'preprocessed')
os.environ['RESULTS_FOLDER'] = TRAINING_RESULTS_FOLDER
load_dotenv()

ngrok.set_auth_token(token='2cWwv5uMeHXGNtquH0vNa0REn2K_7BeDTmcs2BFXG1UW8Fsdk')

public_url = ngrok.connect(8000)
print("Public URL:", public_url)

app = FastAPI()

# Serve files from the "UmbrellaAPI/temp" directory under the "/files" URL path

os.makedirs(STATIC_FILES, exist_ok=True)
app.mount(STATIC_FILES, StaticFiles(directory=STATIC_FILES), name="files")


@app.get("/")
async def hello_world():
    return {"message": f"Hello, World! - {randint(0, 100)}"}



app.include_router(segmentation.router)
