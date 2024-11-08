import dicom2nifti
from core.config import TEMP_EXTRACTED_DICOM
import os

def convert_dicom_to_nifti(dicom_directory, output_folder):
    
    dicom2nifti.convert_directory(dicom_directory, output_folder, compression=True, reorient=True)

    






