from nnunet.inference.predict import predict_from_folder
from core.config import MODEL_FOLDER




def predict(input_folder, output_folder):
    predict_from_folder(
        model=str(MODEL_FOLDER),            # Path to the model folder
        input_folder=input_folder,            # Input folder with NIfTI files
        output_folder=output_folder,          # Where the predictions will be saved
        folds=[0],                            # Fold(s) to be used for prediction
        num_threads_preprocessing=1,          # Number of preprocessing threads
        num_threads_nifti_save=1,             # Number of threads for saving NIfTI files
        lowres_segmentations=None,            # If applicable, for low-resolution predictions
        part_id=0,                            # Which part of the dataset (for distributed prediction)
        num_parts=1,                          # Number of parts in case of distributed prediction
        tta=True,
        save_npz=False
        # Test Time Augmentation (set to True for better accuracy)
    )