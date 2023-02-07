# from joblib import load
import joblib
from sklearn import datasets

# Load the model from a file
clf = joblib.load('./model.joblib')
print(clf)

# Load new data
iris = datasets.load_iris()
X_new, y_new = iris.data, iris.target

# Use the model to make predictions on new data
predictions = clf.predict_proba(X_new)
print(predictions)

# Each data
predictions = clf.predict(X_new)
print(predictions)

print('done')