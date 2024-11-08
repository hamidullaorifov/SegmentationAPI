import os
from celery_app import celery
import zipfile
import shutil
from fastapi import HTTPException, UploadFile



@celery.task
def process_file(file_path, patient_id):
    extracted_path = f"temp/extracted/{patient_id}"
    nifti_output_path = f"temp/nifti/{patient_id}"

    # Extract and convert steps here
    os.makedirs(extracted_path, exist_ok=True)
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_path)
    convert_dicom_to_nifti(extracted_path, nifti_output_path)

    # Cleanup
    os.remove(file_path)
    shutil.rmtree(extracted_path)
    return {"message": f"File successfully processed and saved to {nifti_output_path}"}



def validate_zipfile_type(file: UploadFile):
    """Validate that the uploaded file is a ZIP file."""
    if file.content_type != "application/zip":
        raise HTTPException(status_code=400, detail="File must be a ZIP file")

async def save_upload(file: UploadFile, save_path: str):
    """Save the uploaded file to the specified path."""
    with open(save_path, "wb") as buffer:
        buffer.write(await file.read())

def extract_zip(zip_path: str, extract_to: str):
    """Extract a ZIP file to a specified directory."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file")

def cleanup(paths: list):
    """Remove files or directories from the specified paths."""
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


# Find the first compressed nifti file and rename that filename ends with _0000
def get_first_nifti_filename(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.nii.gz'):
            base_name = filename[:-7]  # Remove '.nii.gz' from the end
            new_filename = f"{base_name}_0000.nii.gz"
            
            # Create full paths for renaming
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            return new_filename 
    return None