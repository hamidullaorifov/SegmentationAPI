import os
from pyngrok import ngrok
from fastapi import APIRouter, FastAPI
from dotenv import load_dotenv
from api.endpoints import segmentation
from core.config import TEMP_FILES, TRAINING_RESULTS_FOLDER
os.environ['nnUNet_preprocessed'] = os.path.join(TEMP_FILES, 'preprocessed')
os.environ['RESULTS_FOLDER'] = TRAINING_RESULTS_FOLDER
load_dotenv()



ngrok.set_auth_token(token='2cWwv5uMeHXGNtquH0vNa0REn2K_7BeDTmcs2BFXG1UW8Fsdk')

public_url = ngrok.connect(8000)
print("Public URL:", public_url)

# nest_asyncio.apply()
app = FastAPI()
@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}



app.include_router(segmentation.router)

# public_url = ngrok.connect(8000)
# print("Public URL:", public_url)
