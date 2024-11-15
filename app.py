import streamlit as st
import pickle
import pandas as pd
import random
import json

# Load the trained model and scaler
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open('questions_vocab.json', 'r') as file:
    vocab_data = json.load(file)

# Function to evaluate the user's score
def evaluate_vocab(user_answers, correct_answers):
    correct_count = sum([1 for user_answer, correct in zip(user_answers, correct_answers) if user_answer.lower() == correct.lower()])
    return correct_count / len(correct_answers)

# Streamlit UI
st.title("Dyslexia Detection Tool")

# Vocabulary Test
st.header("Vocabulary Test")
st.write("Choose the correct word for each sentence:")

# Check if the questions have already been selected in the session state
if 'selected_questions' not in st.session_state:
    # Randomly choose 5 sentence completion questions
    sentence_completion_questions = [q for q in vocab_data['questions'] if q['type'] == 'sentence_completion']
    st.session_state.selected_questions = random.sample(sentence_completion_questions, 5)

# Get the selected questions from session state
selected_questions = st.session_state.selected_questions

user_answers = []
for i, question in enumerate(selected_questions):
    # Display each question with options
    st.write(f"**Question {i+1}:** {question['question']}")
    options = question['options']
    user_answer = st.radio(f"Choose the correct answer for Question {i+1}", options, key=f"q{i+1}")
    user_answers.append(user_answer)

# Submit button to evaluate the answers
if st.button("Submit Vocabulary Test"):
    # Collect the correct answers for the selected questions
    correct_answers = [q['correct_answer'] for q in selected_questions]
    vocab_score = evaluate_vocab(user_answers, correct_answers)
    st.write(f"Vocabulary Test Score: {vocab_score:.2f} (0 = no correct answers, 1 = all correct answers)")


# Function to evaluate memory test
def evaluate_memory(user_order, correct_order):
    correct_count = sum([1 for user_word, correct_word in zip(user_order, correct_order) if user_word.lower() == correct_word.lower()])
    return correct_count / len(correct_order)

# Function to make predictions
def predict_dyslexia(input_data):
    # Scale the input data
    scaled_data = scaler.transform(input_data)
    # Predict using the model
    prediction = model.predict(scaled_data)
    # Interpret the result
    label = int(prediction[0])
    if label == 0:
        return "High chance of dyslexia"
    elif label == 1:
        return "Moderate chance of dyslexia"
    else:
        return "Low chance of dyslexia"


# Memory Test Part 2 (Numbers)
st.header("Memory Test: Part 2 (Numbers)")
st.write("Type in the correct order of the numbers shown:")

memory_numbers = random.sample(range(1, 101), 8)  # Generating 8 random numbers between 1 and 100
user_memory_numbers = [st.text_input(f"Number {i+1}: ", key=f"memory_num_{i}") for i in range(8)]

# Prediction Section
st.header("Dyslexia Prediction")
st.write("Enter test scores to determine the likelihood of dyslexia.")

# Function to safely convert input to float, return None if empty or invalid
def safe_float_conversion(input_value):
    if input_value == '':
        return None  # Return None if empty
    try:
        return float(input_value)
    except ValueError:
        return None  # Return None if conversion fails

# User inputs for prediction
lang_vocab = safe_float_conversion(st.text_input("Language Vocabulary Score (0 to 1):"))
memory = safe_float_conversion(st.text_input("Memory Score (0 to 1):"))
speed = safe_float_conversion(st.text_input("Speed Score (0 to 1):"))
visual = safe_float_conversion(st.text_input("Visual Discrimination Score (0 to 1):"))
audio = safe_float_conversion(st.text_input("Audio Discrimination Score (0 to 1):"))
survey = safe_float_conversion(st.text_input("Survey Score (0 to 1):"))

# Check if any input is empty and display a warning
if None in [lang_vocab, memory, speed, visual, audio, survey]:
    st.warning("Please fill in all the fields before proceeding.")
else:
    # Create a DataFrame for the inputs if all fields are filled
    features = ['Language Vocabulary', 'Memory', 'Speed', 'Visual Discrimination', 'Audio Discrimination', 'Survey']
    input_data = pd.DataFrame([[lang_vocab, memory, speed, visual, audio, survey]], columns=features)

    # Handle the button and make prediction
    if st.button("Predict"):
        result = predict_dyslexia(input_data)
        st.success(result)

# Check and display scores for vocabulary and memory tests
if st.button("Submit Vocabulary Test"):
    vocab_score = evaluate_vocab(user_vocab_answers, correct_vocab_answers)
    st.write(f"Vocabulary Test Score: {vocab_score:.2f}")

if st.button("Submit Memory Test Part 1"):
    memory_score = evaluate_memory(user_memory_order, memory_word_list)
    st.write(f"Memory Test Part 1 Score: {memory_score:.2f}")

if st.button("Submit Memory Test Part 2"):
    memory_num_score = evaluate_memory(user_memory_numbers, memory_numbers)
    st.write(f"Memory Test Part 2 Score: {memory_num_score:.2f}")
