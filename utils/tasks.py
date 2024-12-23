import os
import zipfile
import shutil

from fastapi.exceptions import HTTPException
from celery_app import celery
from utils.image_utils import convert_dicom_to_nifti, convert_nifti_to_rtStruct
from utils.file_utils import extract_zip, cleanup, get_nifti_filename
from core.config import TEMP_EXTRACTED_DICOM, TEMP_INPUT_NIFTI, PREDICTIONS_FOLDER, RTSTRUCT_DIR
from utils.prediction import predict


@celery.task
def process_file(zipfile_path, patient_id):
    print("Task started...")

    extracted_path = os.path.join(TEMP_EXTRACTED_DICOM, patient_id)
    nifti_output_path = os.path.join(TEMP_INPUT_NIFTI, patient_id)

    # Extract and convert steps here
    os.makedirs(extracted_path, exist_ok=True)
    
    extract_zip(zipfile_path, extracted_path)

    # Convert dicom files to nifti
    convert_dicom_to_nifti(extracted_path, nifti_output_path)

    nifti_file_name = get_nifti_filename(nifti_output_path)

    # nifti file is not found
    if nifti_file_name is None:
        raise HTTPException(status_code=500, detail="Error occured converting nifti! Nifti file is not found")

    # nnunet requires input nifti filename in "*_0000.nii.gz" format"
    # Rename nifti file
    base_name = nifti_file_name[:-7]  # Remove '.nii.gz' from the end
    new_file_name = f"{base_name}_0000.nii.gz"

    # Create full paths for renaming
    old_file_path = os.path.join(nifti_output_path, nifti_file_name)
    new_file_path = os.path.join(nifti_output_path, new_file_name)
    
    # Rename the file
    os.rename(old_file_path, new_file_path)

    prediction_result_folder = os.path.join(PREDICTIONS_FOLDER, patient_id)
    # Execute prdeiction
    predict(nifti_output_path, prediction_result_folder)

    # Get predicted image filename
    predicted_filename =  get_nifti_filename(prediction_result_folder)

    # Convert to RTStruct
    output_dicom_folder = os.path.join(RTSTRUCT_DIR, patient_id)
    os.makedirs(output_dicom_folder, exist_ok=True)

    input_nifti_path = os.path.join(prediction_result_folder, predicted_filename)
    rtstruct_file_path = convert_nifti_to_rtStruct(input_nifti_path, extracted_path, output_dicom_folder)
    # rtstruct_file_path = convert_nifti_to_rtStruct_rtutils(input_nifti_path, extracted_path, output_dicom_folder)
    
    # Cleanup
    cleanup([extracted_path, prediction_result_folder])
    # shutil.rmtree(extracted_path)
    
    return {"file_path": rtstruct_file_path}