import joblib
from sklearn.linear_model import LinearRegression

# # Train a model
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load the iris dataset
import numpy as np
from sklearn import svm

# Generate dummy data with three classes and one feature
np.random.seed(0)
X = np.random.randn(30, 1)
y = np.concatenate([np.ones(10), np.zeros(10), 2 * np.ones(10)])

# Train a 3-class SVM classifier
clf = svm.SVC(kernel='linear', C=1, decision_function_shape='ovr')
clf.fit(X, y)

# Predict on new data
predictions = clf.predict([[0.5]])


# Save the model as a joblib file
joblib.dump(clf, "model.joblib")

# # Load the saved model
# loaded_model = joblib.load("model_1.joblib")

# # Use the loaded model to make predictions
# predictions = loaded_model.predict([[4, 4]])
# print(predictions)