import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib  # Import joblib to save the vectorizer

# Load data from knowledge_base.json
with open('knowledge_base.json', 'r') as file:
    knowledge_base = json.load(file)

questions = [entry['question'] for entry in knowledge_base['questions']]
answers = [entry['answer'] for entry in knowledge_base['questions']]

# Use TF-IDF for text representation
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)  # Fit the vectorizer on the entire set of questions
y = answers

# Save the fitted vectorizer
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose a classifier (Support Vector Machine in this example)
classifier = SVC()

# Train the model
classifier.fit(X_train, y_train)

# Save the trained model
joblib.dump(classifier, 'chatbot_model.joblib')



