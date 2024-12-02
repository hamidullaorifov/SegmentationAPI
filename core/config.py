from pathlib import Path
import os
# Root project directory
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_FILES = os.path.join(BASE_DIR, 'static')
RTSTRUCT_DIR = os.path.join(STATIC_FILES, 'rtstruct')
# Define temporary directories
TEMP_FILES = BASE_DIR / 'temp'
TEMP_ZIP_INPUT_DIR = TEMP_FILES / 'zip' / 'input'
TEMP_EXTRACTED_DICOM = TEMP_FILES / 'files' / 'dicom'
TEMP_INPUT_NIFTI = TEMP_FILES / 'files' / 'nifti'



# Model folder for prediction
# TRAINING_RESULTS_FOLDER = BASE_DIR / 'results' / 'nnUNet' / '3d_fullres' / 'Task01_BraTS_onlyT1ce' / 'nnUNetTrainer__nnUNetPlans' 
TRAINING_RESULTS_FOLDER = os.path.join(BASE_DIR, 'results') 

MODEL_FOLDER = TRAINING_RESULTS_FOLDER

PREDICTIONS_FOLDER = os.path.join(TEMP_FILES,'predictions')

