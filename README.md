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

## Instructions to Run the App
### File Preparation
Ensure the following files are in the same directory as the application script:
- `model.pkl`
- `scaler.pkl`
- `questions_vocab.json`
- (Optional) `Audios_memory` directory for handling audio-based questions.

### Running the App
- **For macOS users**:  
  Run the app using the script `app_mac_ver.py`.
  
- **For Windows users**:  
  Run the app using the script `app.py`.

---

## Notes
- The Streamlit app does not include detailed input workflows, which are instead demonstrated in `inputtest.ipynb`.
- Audio-based questions rely on the `Audios_memory` directory for execution.

---

## Contact
If you have any questions or encounter issues, feel free to open an issue or contact through kian.ttvi@gmail.com

---

### Example Markdown Features Used
- Headings for a clear hierarchy (`#`, `##`, `###`)
- Bullet points for lists
- Inline links for external resources
- Code blocks (```markdown``` for GitHub format demonstration)

This structure is clean, visually appealing, and follows GitHub README best practices.
