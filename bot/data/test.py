import joblib

# Load the trained model
classifier = joblib.load('chatbot_model.joblib')

# Load the TF-IDF vectorizer
vectorizer = joblib.load('tfidf_vectorizer.joblib')

# Test the model
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break

    # Transform the user input using the loaded TF-IDF vectorizer
    user_input_vectorized = vectorizer.transform([user_input])

    # Predict the response using the loaded model
    response = classifier.predict(user_input_vectorized)

    print(f"Bot: {response[0]}")
