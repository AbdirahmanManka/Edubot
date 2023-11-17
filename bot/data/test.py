import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the saved model
loaded_model = joblib.load('chatbot_model.joblib')

# Load the TF-IDF vectorizer used during training
vectorizer = joblib.load('tfidf_vectorizer.joblib')  # Assuming you saved the vectorizer during training

# Define stop words
stop_words = ['exit', 'stop', 'thank you']

while True:
    # User input
    user_input = input("User: ")

    # Check if user wants to exit
    if any(stop_word in user_input.lower() for stop_word in stop_words):
        print("Chatbot: Goodbye!")
        break

    # Preprocess the user input
    user_input_tfidf = vectorizer.transform([user_input])

    # Make a prediction using the loaded model
    predicted_answer = loaded_model.predict(user_input_tfidf)

    # Print the predicted answer
    print("Chatbot:", predicted_answer[0])
