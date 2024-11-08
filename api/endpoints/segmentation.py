import os
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.exceptions import HTTPException


from core.config import TEMP_ZIP_INPUT_DIR, TEMP_EXTRACTED_DICOM, TEMP_INPUT_NIFTI
from utils.image_utils import convert_dicom_to_nifti
from utils.file_utils import validate_zipfile_type, save_upload, extract_zip, cleanup, get_first_nifti_filename
from utils.prediction import predict
router = APIRouter(tags=['Segmentation'])





@router.post("/segmentation/", status_code=200)
async def upload_file(file: UploadFile = File(...)):
    
    # Check if uploaded file is a ZIP file
    validate_zipfile_type(file)

    
    patient_id = os.path.splitext(file.filename)[0]
    zip_path = os.path.join(TEMP_ZIP_INPUT_DIR, file.filename)
    extracted_path = os.path.join(TEMP_EXTRACTED_DICOM, patient_id)
    nifti_output_path = os.path.join(TEMP_INPUT_NIFTI, patient_id)

    # Create necessary directories
    os.makedirs(TEMP_ZIP_INPUT_DIR, exist_ok=True)
    os.makedirs(extracted_path, exist_ok=True)
    os.makedirs(nifti_output_path, exist_ok=True)

    # Process the upload: save, extract, convert, and clean up
    await save_upload(file, zip_path)
    extract_zip(zip_path, extracted_path)
    convert_dicom_to_nifti(extracted_path, nifti_output_path)
    cleanup([zip_path, extracted_path])  # Cleanup ZIP and extracted DICOM directory
    
    nifti_filename = get_first_nifti_filename(nifti_output_path)
    if nifti_filename is None:
        raise HTTPException(status_code=500, detail="Couldn't find nifti file")


    predict(nifti_output_path, 'predictions')

    return {"message": f"File successfully processed and saved to {nifti_output_path}"}
   
