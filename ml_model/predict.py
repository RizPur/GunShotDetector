#script to make prediction if audio is a gunshot

# Example code to load a model and make predictions
import joblib

# Load the model
clf = joblib.load('model.pkl')

# Make predictions
predictions = clf.predict(X_new)