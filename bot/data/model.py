from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import json

# Load data from JSON file
with open("knowledge_base.json", "r") as json_file:
    data = json.load(json_file)

# Extract questions and answers
questions = [q["question"] for q in data["questions"]]
answers = [q["answer"] for q in data["questions"]]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(questions, answers, test_size=0.2, random_state=42)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Save the TF-IDF vectorizer to a file
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

# Train a Support Vector Machine (SVM) classifier
clf = SVC(kernel='linear')
clf.fit(X_train_tfidf, y_train)

# Make predictions
predictions = clf.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print("Model Accuracy:", accuracy)

# Save the model to a file
joblib.dump(clf, 'chatbot_model.joblib')