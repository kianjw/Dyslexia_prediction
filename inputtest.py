# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, f1_score
import pickle

# Step 1: Load and preprocess the data
data = pd.read_csv(r"labelled_dysx.csv")
y = data['Label']
X = data.drop(['Label'], axis=1)
columns = X.columns  # Store the feature names

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=10)

# Initialize and fit the scaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Step 2: Train the model using GridSearchCV
n_est = {'n_estimators': [10, 100, 500, 1000]}
model = GridSearchCV(RandomForestClassifier(random_state=0), n_est, scoring='accuracy')
model.fit(X_train, y_train)

# Make predictions on the test set and print the evaluation report
predictions = model.predict(X_test)

# Save the trained model and scaler
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)
with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(sc, scaler_file)

# Step 3: Interactive section for new inputs
name = input("Enter name of applicant: ")
print("\nThe scores of all the tests in quiz as well as survey need to be entered.")
print("All the values lie in the range 0 to 1.\n")

# Function to validate input scores
def get_score(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0.0 <= value <= 1.0:
                return value
            else:
                print("Please enter a value between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a numerical value between 0 and 1.")

lang_vocab = get_score("Enter the score of Language Vocab test: ")
memory = get_score("Enter the score of Memory test: ")
speed = get_score("Enter the score of Speed test: ")
visual = get_score("Enter the score of Visual Discrimination test: ")
audio = get_score("Enter the score of Audio Discrimination test: ")
survey = get_score("Enter the score obtained from Survey: ")

# Step 4: Define the function to make predictions based on new input
def get_result(lang_vocab, memory, speed, visual, audio, survey):
    # Load the model and scaler
    with open("model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("scaler.pkl", "rb") as scaler_file:
        sc = pickle.load(scaler_file)

    # Create a DataFrame for the new input data
    data = pd.DataFrame([[lang_vocab, memory, speed, visual, audio, survey]], columns=columns)
    
    # Scale the new data
    data_scaled = sc.transform(data)

    # Predict using the loaded model
    prediction = model.predict(data_scaled)

    # Interpret the prediction result
    label = int(prediction[0])
    if label == 0:
        output = "There is a high chance of the applicant having dyslexia."
    elif label == 1:
        output = "There is a moderate chance of the applicant having dyslexia."
    else:
        output = "There is a low chance of the applicant having dyslexia."
    return output

# Get and print the prediction result for the new input
result = get_result(lang_vocab, memory, speed, visual, audio, survey)
print(result)
