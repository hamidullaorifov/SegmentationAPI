from celery import Celery
import os
import zipfile
import shutil


from utils.image_utils import convert_dicom_to_nifti
from utils.file_utils import validate_zipfile_type, save_upload, extract_zip, cleanup, get_nifti_filename
from core.config import TEMP_ZIP_INPUT_DIR, TEMP_EXTRACTED_DICOM, TEMP_INPUT_NIFTI

celery = Celery(
    __name__,
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True
)

# @celery.task
# def preprocess_file(zipfile_path, patient_id):
#     print("Task started...")
#     extracted_path = os.path.join(TEMP_EXTRACTED_DICOM, patient_id)
#     nifti_output_path = os.path.join(TEMP_INPUT_NIFTI, patient_id)

#     # Extract and convert steps here
#     os.makedirs(extracted_path, exist_ok=True)
#     print("Extracting file...")
#     extract_zip(zipfile_path, extracted_path)
#     print("Converting to dicom...")
#     convert_dicom_to_nifti(extracted_path, nifti_output_path)
#     print("Converting finished!")
#     # Cleanup
    
#     # shutil.rmtree(extracted_path)
#     return {"message": "File successfully processed and saved"}


celery.autodiscover_tasks(['utils'])


celery.conf.update(
    task_track_started=True,  # Track task start
    worker_concurrency=1,  # Single worker concurrency (adjust as needed)
)
