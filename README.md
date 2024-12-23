# Dyslexia Prediction

## Overview
This project predicts dyslexia risk levels (High, Moderate, Low) using a machine learning model with an interactive interface built in Streamlit.

## Source of Data
The dataset used in this project is sourced from Kaggle: [Dyslexia Dataset](https://www.kaggle.com/datasets/thenikhilnj45/dyslexiaproject).

---

## File Structure
### Main Files
- **Details_dyslexia.ipynb**:  
  The final notebook version that includes all preprocessing, model training, and prediction logic.
- **data_preprocessing_model_training.ipynb**:  
  A separate notebook for data preprocessing and model training using Random Forest with GridSearchCV.
- **inputtest.ipynb**:  
  A notebook demonstrating how the inputs work to generate predictions (High, Moderate, Low). This functionality is not exposed in the Streamlit app.
- **Dyslexia_test_questions_set.docx**:  
  A document containing a custom test created using data and formulas from several well-known sources.

---

## Dyslexia Detection Tool: Instructions

This tool uses a machine learning model to detect dyslexia through vocabulary and memory tests. Below are the steps to set up, run, and interact with the project.

### Prerequisites

### Install Required Software
1. **Python**: Install Python 3.8 or later. You can download it from [python.org](https://www.python.org/downloads/).
2. **pip**: Ensure you have `pip` installed to manage Python packages.

### Clone the Repository
1. Open a terminal (or command prompt) and run:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

### Install Dependencies
2. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Streamlit**: Ensure Streamlit is installed. You can install it using:
   ```bash
   pip install streamlit
   ```

### Additional Setup
4. **Dataset**: Place your training and testing data (e.g., vocabulary and memory test quizzes) in the `data/` directory. Make sure the folder structure matches what the scripts expect.

5. **Model File**: Ensure the pre-trained model file is in the `models/` directory. The model file name should match the one referenced in the code.

---

## Running the Application

### Step 1: Launch the Interface
1. Run the application using the following command:
   ```
   streamlit run app.py
   ```

2. This will start a local web server. You should see output similar to:
   ```
   Local URL: http://localhost:8501
   Network URL: http://<your_network_ip>:8501
   ```

### Step 2: Open the Web Interface
1. Open your browser and navigate to the provided URL (e.g., `http://localhost:8501`).
2. You will see the Dyslexia Detection Tool interface.

---

## Using the Tool

### Vocabulary Test
1. Start the vocabulary quiz by clicking the **Start Vocabulary Test** button.
2. Random words will appear. Enter your responses into the input fields.
3. Submit your answers to evaluate the test.

### Memory Test
1. Initiate the memory test by clicking the **Start Memory Test** button.
2. The system will play audio with a list of words.
3. After playback, input the words you recall.
4. Submit your responses to see the evaluation.

---

## Results and Feedback
1. After completing the quizzes, the tool will provide feedback on your performance.
2. The results will also include a prediction about potential dyslexia indicators based on the machine learning model.

---

## Optional: Model Training
If you want to train the model with new data:

### Step 1: Prepare the Dataset
1. Place the dataset in the `data/` directory.
2. Ensure the data is labeled and preprocessed correctly.

### Step 2: Run the Training Script
1. Execute the following command:
   ```bash
   python train_model.py
   ```
2. Once training is complete, the updated model file will be saved in the `models/` directory.

---

## Troubleshooting

1. **Dependencies Issues**: Ensure all required Python packages are installed. If an error occurs, try:
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Issues**: If the port is already in use, specify a different port:
   ```bash
   streamlit run app.py --server.port 8080
   ```

3. **Browser Issues**: Clear your browser cache or try a different browser if the interface does not load.

---
---
### Interface view
https://github.com/user-attachments/assets/479e1f63-2a31-4930-aa8c-9d328cc19ab4



## Notes
- The Streamlit app does not include detailed input workflows, which are instead demonstrated in `inputtest.ipynb`.
- Audio-based questions rely on the `Audios_memory` directory for execution.

---

## Contact
If you have any questions or encounter issues, feel free to open an issue or contact through kian.ttvi@gmail.com or karandahal@gmail.com


This structure is clean, visually appealing, and follows GitHub README best practices.




