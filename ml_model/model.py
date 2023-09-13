#script to train and save model

# Example code to train and save a model
from sklearn.ensemble import RandomForestClassifier
import joblib

# Train the model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Save the model
joblib.dump(clf, 'model.pkl')