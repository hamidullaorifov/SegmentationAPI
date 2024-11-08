from pathlib import Path

# Root project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define temporary directories
TEMP_FILES = BASE_DIR / 'temp'
TEMP_ZIP_INPUT_DIR = TEMP_FILES / 'zip' / 'input'
TEMP_EXTRACTED_DICOM = TEMP_FILES / 'files' / 'dicom'
TEMP_INPUT_NIFTI = TEMP_FILES / 'files' / 'nifti'

# Model folder for prediction
TRAINING_RESULTS_FOLDER = BASE_DIR / 'results' / 'nnUNet' / '3d_fullres' / 'Task01_BraTS_onlyT1ce' / 'nnUNetTrainer__nnUNetPlans' 

MODEL_FOLDER = TRAINING_RESULTS_FOLDER


