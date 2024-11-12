import dicom2nifti

def convert_dicom_to_nifti(dicom_directory, output_folder):
    print("Converting dicom files to nifti...")

    dicom2nifti.convert_directory(dicom_directory, output_folder, compression=True, reorient=True)

    print("Successfully converted dicom files to nifti!")
    






