import os

from nnunet.inference.predict import predict_from_folder
from core.config import TRAINING_RESULTS_FOLDER
from dotenv import load_dotenv
import subprocess


os.environ['RESULTS_FOLDER'] = TRAINING_RESULTS_FOLDER


def predict(nifti_output_path, prediction_result_folder):
    print("Prediction started...")
    model_path = "results/nnUNet/3d_fullres/Task01_BraTS_onlyT1ce/nnUNetTrainer__nnUNetPlans/fold_0/model_best.model"
    
    subprocess.run([
        'nnUNet_predict',
        '-i', nifti_output_path,               
        '-o', prediction_result_folder,        
        '-m', '3d_fullres',
        '-t', 'Task01_BraTS_onlyT1ce',                   
        '-f', '0',                             
        '--num_threads_preprocessing', '1',
        '--num_threads_nifti_save', '1',
    ])


# def predict(input_folder, output_folder):
#     print("Prediction started...")
#     predict_from_folder(
#         model=str(MODEL_FOLDER),            # Path to the model folder
#         input_folder=input_folder,            # Input folder with NIfTI files
#         output_folder=output_folder,          # Where the predictions will be saved
#         folds=[0],                            # Fold(s) to be used for prediction
#         num_threads_preprocessing=1,          # Number of preprocessing threads
#         num_threads_nifti_save=1,             # Number of threads for saving NIfTI files
#         lowres_segmentations=None,            # If applicable, for low-resolution predictions
#         part_id=0,                            # Which part of the dataset (for distributed prediction)
#         num_parts=1,                          # Number of parts in case of distributed prediction
#         tta=True,
#         save_npz=False
#         # Test Time Augmentation (set to True for better accuracy)
#     )