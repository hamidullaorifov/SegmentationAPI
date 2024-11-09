import os
from pyngrok import ngrok
from fastapi import APIRouter, FastAPI
from dotenv import load_dotenv
from api.endpoints import segmentation
from core.config import TEMP_FILES
os.environ['nnUNet_preprocessed'] = os.path.join(TEMP_FILES, 'preprocessed')
os.environ['RESULTS_FOLDER'] = os.path.join(TEMP_FILES,'predictions')

load_dotenv()


# nest_asyncio.apply()
app = FastAPI()
@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}

print("ENVVVVV:", os.environ.get("RESULTS_FOLDER"))

app.include_router(segmentation.router)

# public_url = ngrok.connect(8000)
# print("Public URL:", public_url)
