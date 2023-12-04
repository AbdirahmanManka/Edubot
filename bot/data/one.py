from joblib import load

# Load the model from the file
model = load('chatbot_model.joblib')

# Display the model
print(model)