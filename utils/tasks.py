import os
import zipfile
import shutil

from celery_app import celery
from utils.image_utils import convert_dicom_to_nifti
from utils.file_utils import validate_zipfile_type, save_upload, extract_zip, cleanup, get_first_nifti_filename
from core.config import TEMP_ZIP_INPUT_DIR, TEMP_EXTRACTED_DICOM, TEMP_INPUT_NIFTI



@celery.task
def process_file(zipfile_path, patient_id):
    print("Task started...")
    extracted_path = os.path.join(TEMP_EXTRACTED_DICOM, patient_id)
    nifti_output_path = os.path.join(TEMP_INPUT_NIFTI, patient_id)

    # Extract and convert steps here
    os.makedirs(extracted_path, exist_ok=True)
    print("Extracting file...")
    extract_zip(zipfile_path, extracted_path)
    print("Converting to dicom...")
    convert_dicom_to_nifti(extracted_path, nifti_output_path)
    print("Converting finished!")
    # Cleanup
    
    # shutil.rmtree(extracted_path)
    return {"message": "File successfully processed and saved"}