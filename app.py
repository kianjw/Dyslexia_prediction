import streamlit as st
import pickle
import pandas as pd
import random
import json
import time
import os

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




# Check if the page variable exists in session state
if 'page' not in st.session_state:
    st.session_state.page = 1  # Initialize the page variable

# Streamlit UI
st.title("Dyslexia Detection Tool")
'''
Vocab Part

'''
# Vocabulary Test
st.header("Vocabulary Test")
st.write("Choose the correct word for each sentence:")

# Check if the questions have already been selected in the session state
if 'selected_questions' not in st.session_state:
    # Randomly choose 5 sentence completion questions
    sentence_completion_questions = [q for q in vocab_data['questions'] if q['type'] == 'sentence_completion']
    st.session_state.selected_questions = random.sample(sentence_completion_questions, 10)

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


# Memory Part



# Function to evaluate the memory test for each sequence
def evaluate_memory(user_answer, correct_answer):
    # Compare the entire string (the sequence of digits) without spaces
    return user_answer.strip() == correct_answer.strip()

# Memory Test
st.header("Memory Test")
st.write("Observe the sequence of numbers. After the sequence disappears, type them in the correct order and press submit to check your answer.")

# Check if the sequences have already been selected in the session state
if 'sequences' not in st.session_state:
    # Generate 5 random sequences of 6 digits
    st.session_state.sequences = [random.sample(range(10), 6) for _ in range(5)]

# Store user answers in session state
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = ['' for _ in range(5)]  # Initialize empty answers for each sequence

# Store scores for each sequence
if 'scores' not in st.session_state:
    st.session_state.scores = [None for _ in range(5)]  # Initialize None for scores to evaluate later

# Store whether each sequence has been displayed or not
if 'displayed' not in st.session_state:
    st.session_state.displayed = [False for _ in range(5)]  # Track if each sequence is displayed

# Store whether each sequence has been submitted or not
if 'submitted' not in st.session_state:
    st.session_state.submitted = [False for _ in range(5)]  # Track if each sequence is submitted

# Display buttons for each sequence
for i in range(5):
    sequence_label = f"Sequence {i + 1}"

    # Display the sequence only if it's not displayed yet and not submitted
    if not st.session_state.displayed[i] and not st.session_state.submitted[i]:
        # Button to display the sequence
        if st.button(f"Display Sequence {i + 1}", key=f"display_{i}"):
            # Show the sequence to the user
            sequence = st.session_state.sequences[i]
            sequence_str = " ".join(map(str, sequence))

            # Display the sequence for 1.5 seconds
            st.write(f"**{sequence_label}:** {sequence_str}")
            time.sleep(1.5)  # Wait for 1.5 seconds

            # Hide the sequence after time has passed
            st.empty()

            # Mark this sequence as displayed
            st.session_state.displayed[i] = True

    # Input box for the user to enter their answer for this sequence
    if st.session_state.displayed[i] and not st.session_state.submitted[i]:
        user_answer = st.text_input(f"Enter the sequence for {sequence_label}", max_chars=6, key=f"sequence_{i}_input", 
                                     value=st.session_state.user_answers[i])  # Preserve previous input

        # Store the user answer in session state for this sequence
        if user_answer:
            st.session_state.user_answers[i] = user_answer.strip()  # Store the entire input as a string

        # Button to submit the answer for this sequence
        if st.button(f"Submit {sequence_label}", key=f"submit_{i}") and not st.session_state.submitted[i]:
            # Evaluate the sequence answer
            if evaluate_memory(user_answer, ''.join(map(str, st.session_state.sequences[i]))):
                st.session_state.scores[i] = 1  # Correct
                st.write(f"**{sequence_label}: Correct!**")
            else:
                st.session_state.scores[i] = 0  # Incorrect
                st.write(f"**{sequence_label}: Incorrect!**")

            # Mark the sequence as submitted
            st.session_state.submitted[i] = True
# Audio-Based Memory Test Section
st.header("Memory Test Part 2: Immediate Recall")
st.write("Listen carefully to the audio. After the audio finishes, type in the words in the correct order and press submit to check your answer.")

# Audio path for the WAV files
audio_path = r"C:\Users\Acer\Desktop\Machine Leaning\Final Project\Audios_memory"

# List of audio files based on the path you provided
st.session_state.audio_files = [
    f"{audio_path}\\audio_1.wav",  # Apple, Lettuce, House, River, Dog, Book, Cooking.
    f"{audio_path}\\audio_2.wav",  # Dog, Cat, Rabbit, Horse, Sheep, Cow, Goat. (Farm animals)
    f"{audio_path}\\audio_3.wav",  # Table, Chair, Sofa, Bed, Desk, Lamp, Shelf. (Furniture)
    f"{audio_path}\\audio_4.wav",  # River, Lake, Ocean, Pond, Stream, Beach, Waterfall. (Bodies of water)
    f"{audio_path}\\audio_5.wav",  # Red, Blue, Green, Yellow, Pink, Black, White. (Colors)
    f"{audio_path}\\audio_6.wav",  # Car, Bus, Train, Plane, Boat, Bike, Truck. (Modes of transport)
    f"{audio_path}\\audio_7.wav",  # Rain, Snow, Sun, Cloud, Wind, Storm, Thunder. (Weather)
    f"{audio_path}\\audio_8.wav",  # Pen, Pencil, Eraser, Paper, Book, Notebook, Ruler. (Stationery)
    f"{audio_path}\\audio_9.wav",  # Tree, Flower, Grass, Leaf, Seed, Branch, Bush. (Nature)
    f"{audio_path}\\audio_10.wav"  # Shirt, Pants, Socks, Jacket, Hat, Gloves, Scarf.
]

# Correct answers for each audio file
st.session_state.correct_answers = [
    ["Apple", "Lettuce", "House", "River", "Dog", "Book", "Cooking"],
    ["Dog", "Cat", "Rabbit", "Horse", "Sheep", "Cow", "Goat"],
    ["Table", "Chair", "Sofa", "Bed", "Desk", "Lamp", "Shelf"],
    ["River", "Lake", "Ocean", "Pond", "Stream", "Beach", "Waterfall"],
    ["Red", "Blue", "Green", "Yellow", "Pink", "Black", "White"],
    ["Car", "Bus", "Train", "Plane", "Boat", "Bike", "Truck"],
    ["Rain", "Snow", "Sun", "Cloud", "Wind", "Storm", "Thunder"],
    ["Pen", "Pencil", "Eraser", "Paper", "Book", "Notebook", "Ruler"],
    ["Tree", "Flower", "Grass", "Leaf", "Seed", "Branch", "Bush"],
    ["Shirt", "Pants", "Socks", "Jacket", "Hat", "Gloves", "Scarf"]
]

# Check if the audio selection is already in the session state
if 'selected_audios' not in st.session_state:
    # Randomly select 5 audios from the list of 10
    st.session_state.selected_audios = random.sample(list(enumerate(st.session_state.audio_files)), 5)

# Initialize playback counters for each audio
if 'audio_play_counts' not in st.session_state:
    st.session_state.audio_play_counts = [0 for _ in range(len(st.session_state.selected_audios))]

# Store user answers for audio-based test
if 'audio_user_answers' not in st.session_state:
    st.session_state.audio_user_answers = ['' for _ in range(5)]  # Initialize empty answers

# Store scores for audio test
if 'audio_scores' not in st.session_state:
    st.session_state.audio_scores = [None for _ in range(5)]  # Initialize None for scores

# Function to play audio via Streamlit's native audio function
def play_audio(audio_file):
    st.audio(audio_file, format="audio/wav")

# Display each audio and input field
for idx, (audio_idx, audio_path) in enumerate(st.session_state.selected_audios):
    audio_label = f"Audio {idx + 1}"
    play_count = st.session_state.audio_play_counts[idx]  # Get the current play count

    # Button to play the audio
    if play_count < 2:
        if st.button(f"Play {audio_label} ({2 - play_count} plays left)", key=f"play_{idx}"):
            # Increment the play count
            st.session_state.audio_play_counts[idx] += 1
            play_audio(audio_path)  # Play the audio using Streamlit's audio function

    else:
        st.write(f"**{audio_label}: Audio can no longer be played.**")

    # Input box for the user to enter their answer
    user_answer_audio = st.text_input(f"Enter your answer for {audio_label}", key=f"audio_input_{idx}", 
                                      value=st.session_state.audio_user_answers[idx])

    # Store user answer in session state
    if user_answer_audio:
        st.session_state.audio_user_answers[idx] = user_answer_audio.strip()

    # Button to submit the answer for this audio
    if st.button(f"Submit {audio_label}", key=f"audio_submit_{idx}") and st.session_state.audio_scores[idx] is None:
        # Evaluate the answer
        correct_answer = " ".join(st.session_state.correct_answers[audio_idx])
        if user_answer_audio.lower() == correct_answer.lower():
            st.session_state.audio_scores[idx] = 1  # Correct
            st.write(f"**{audio_label}: Correct!**")
        else:
            st.session_state.audio_scores[idx] = 0  # Incorrect
            st.write(f"**{audio_label}: Incorrect! The correct answer was '{correct_answer}'**")

# Button to calculate final score for audio test
if st.button("Submit Final Audio Test Score"):
    audio_total_score = sum(filter(None, st.session_state.audio_scores))  # Filter out None values
    audio_total_percentage = audio_total_score / len(st.session_state.audio_scores)
    st.write(f"Final Audio Test Score: {audio_total_percentage:.2f} (0 = no correct answers, 1 = all correct answers)")

    # Optionally, display results for each audio
    for idx, (audio_idx, _) in enumerate(st.session_state.selected_audios):
        correct_answer = " ".join(st.session_state.correct_answers[audio_idx])
        st.write(f"Audio {idx + 1}:")
        st.write(f"User Answer: '{st.session_state.audio_user_answers[idx]}'")
        st.write(f"Correct Answer: '{correct_answer}'")
        st.write(f"Score: {st.session_state.audio_scores[idx]}")

# Button to calculate and show final memory score
if st.button("Submit Final Memory Test Score"):
    total_score = sum(st.session_state.scores)  # Add up the scores for all sequences
    total_score_percentage = total_score / 5  # Calculate the percentage (total score / number of sequences)

    st.write(f"Final Memory Test Score: {total_score_percentage:.2f} (0 = no correct answers, 1 = all correct answers)")

# Visual Discrimination Test Section
st.header("Visual Discrimination Test")
st.write("Complete the tasks below to assess visual discrimination ability.")

# Letter Identification
st.subheader("Letter Identification")
st.write("On the following line of letters, count the number of 'd' letters:")
st.write("`b p q d b d p q b d p q`")

# Input for Letter Identification
user_count_d = st.number_input("Enter the number of 'd' letters you found:", min_value=0, max_value=12, step=1, key="letter_count")

# Button to submit Letter Identification task
if st.button("Submit Letter Identification"):
    correct_count_d = 3  # Correct answer for the number of 'd'
    score_letter_identification = min(user_count_d, correct_count_d) * 0.1  # Each correct 'd' is worth 0.1, max is 0.3
    st.write(f"**Score for Letter Identification:** {score_letter_identification:.2f} / 0.3")

# Spot the Differences
st.subheader("Spot the Differences")
st.write("Identify the differences in the following sequence:")
st.write("`b p q d d p`")

# Pre-defined correct differences
correct_differences = ["b", "p", "q", "d"]  # Define the correct differences here

# Input for Spot the Differences
user_spot_diff = st.text_input("List the differences you spotted (separate each with a comma):", key="spot_diff")

# Button to submit Spot the Differences task
if st.button("Submit Spot the Differences"):
    # Process user input: split by commas, clean whitespace, and ensure lowercase
    user_differences = [item.strip().lower() for item in user_spot_diff.split(",")]

    # Deduplicate the input and maintain the order of first appearance
    unique_user_differences = []
    for item in user_differences:
        if item not in unique_user_differences:
            unique_user_differences.append(item)

    # Identify invalid inputs (not in the correct differences)
    invalid_differences = [diff for diff in unique_user_differences if diff not in correct_differences]

    # Count correct differences, ignoring duplicates
    correct_count = sum(1 for diff in unique_user_differences if diff in correct_differences)

    # Calculate the score: 0.1 points for each correct difference, max 0.4
    score_spot_differences = min(correct_count * 0.1, 0.4)  # Cap the score at 0.4

    # Display the result
    st.write(f"**Your Input:** {user_spot_diff}")
    st.write(f"**Correct Differences:** {', '.join(correct_differences)}")
    st.write(f"**Unique Differences Considered:** {', '.join(unique_user_differences)}")
    if invalid_differences:
        st.write(f"**Invalid Differences:** {', '.join(invalid_differences)} (not part of the correct differences)")
    st.write(f"**Number of Correct Differences Identified:** {correct_count}")
    st.write(f"**Score for Spot the Differences:** {score_spot_differences:.2f} / 0.4")

# Odd One Out
st.subheader("Odd One Out")
st.write("Choose the option that doesn't belong:")

# Odd One Out Options
odd_one_out = st.radio(
    "Which is the odd one out?",
    options=["a) ○", "b) ○", "c) ○", "d) ■"],
    key="odd_one_out"
)

# Button to submit Odd One Out task
if st.button("Submit Odd One Out"):
    correct_answer = "d) ■"  # Correct answer for the odd one out
    if odd_one_out == correct_answer:
        st.write("**Correct! The odd one out is 'd) ■'.**")
        score_odd_one_out = 0.3
    else:
        st.write(f"**Incorrect. The correct answer is 'd) ■'. You selected {odd_one_out}.**")
        score_odd_one_out = 0
    st.write(f"**Score for Odd One Out:** {score_odd_one_out:.2f} / 0.3")


# Survey Test Section
st.header("Survey Test")
st.write("Answer the following questions by selecting the most appropriate option:")

# Define the survey questions
survey_questions = [
    "Do you often find it difficult to read words or letters in the correct order?",
    "Do you have trouble spelling common words correctly?",
    "Do you frequently mix up similar-looking letters like 'b' and 'd'?",
    "Do you find it hard to concentrate when reading or writing?",
    "Do you have difficulty remembering sequences such as phone numbers?"
]

# Define the options and corresponding scores
survey_options = {"Yes": 4, "Often": 3, "Sometimes": 2, "Not Often": 1, "No": 0}

# Initialize user responses
user_responses = []

# Loop through the questions and collect responses
for i, question in enumerate(survey_questions):
    st.write(f"**Question {i + 1}:** {question}")
    response = st.radio(f"Select your answer for Question {i + 1}", list(survey_options.keys()), key=f"survey_q{i+1}")
    user_responses.append(survey_options[response])

# Submit button for survey test
if st.button("Submit Survey Test"):
    # Calculate the raw score and scaled score
    raw_score = sum(user_responses)
    scaled_score = raw_score / 20  # Total possible points = 20 (5 questions * 4 points max per question)

    # Display the results
    st.write(f"**Survey Test Raw Score:** {raw_score} / 20")
    st.write(f"**Survey Test Scaled Score:** {scaled_score:.2f} (0 = lowest, 1 = highest)")




'''
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
'''