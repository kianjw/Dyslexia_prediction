Dyslexia Prediction
Overview
This project predicts dyslexia risk levels (High, Moderate, Low) using a machine learning model with an interactive interface built in Streamlit.

Source of Data
Data sourced from Kaggle: Dyslexia Dataset
File Structure
Main Files
Details_dyslexia.ipynb: Final version containing all preprocessing, training, and prediction logic.
data_preprocessing_model_training.ipynb: Focuses on data preprocessing and model training using Random Forest with GridSearchCV.
inputtest.ipynb: Demonstrates input handling for generating predictions.
Dyslexia_test_questions_set.docx: Contains a custom test with questions compiled from well-known sources.
Instructions to Run the App
File Preparation:

Ensure the following files are in the same directory as the application scripts:
model.pkl
scaler.pkl
questions_vocab.json
(Optional) Audios_memory for audio-based questions.
Execution:

For macOS users:
Run the app using app_mac_ver.py.
For Windows users:
Run the app using app.py.
Notes
The Streamlit app does not show the detailed prediction input process (handled separately in inputtest.ipynb).
Audio-based questions require downloading the Audios_memory file.


<img width="925" alt="image" src="https://github.com/user-attachments/assets/57ccdb22-03e7-4d41-9645-b6565a023b7d">
<img width="925" alt="image" src="https://github.com/user-attachments/assets/72b56aaf-d738-4fef-9024-989dabf4c929">
<img width="925" alt="image" src="https://github.com/user-attachments/assets/1d403aa4-1df2-4a3d-856f-1df5be8f6820">
<img width="925" alt="image" src="https://github.com/user-attachments/assets/b4401048-44e7-4161-8893-2796b799d7fe">
<img width="925" alt="image" src="https://github.com/user-attachments/assets/8ad0e0aa-40eb-403a-ac51-2df4f2a6ae17">
<img width="925" alt="image" src="https://github.com/user-attachments/assets/2c6bcd70-a389-4e11-a06f-6e12f707cd59">

