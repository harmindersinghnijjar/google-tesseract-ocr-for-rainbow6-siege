import os

folders = [
    "Misc_02",
    "Research_01",
    "00_Prototype",
    "01_Select_YOLOv8_Architecture",
    "02_Gather_Training_Data",
    "03_Preprocess_Data",
    "04_Train_YOLOv8_Model",
    "05_Create_Feedback_Loop",
    "06_Retrain_Periodically",
    "07_Evaluate_Monitor_Performance",
    "08_Fine_Tune_Model",
]

for folder in folders:
    os.makedirs(folder)
    with open(os.path.join(folder, '.gitkeep'), 'w'):
        pass
    print(f"Created folder: {folder}")

print("All folders have been created successfully, including .gitkeep files!")
