from joblib import dump
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Load a sample dataset
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Train a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X, y)

# Save the model to a file
dump(clf, 'model.joblib')
print('done')

