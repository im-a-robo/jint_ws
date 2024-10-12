import os
import librosa
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib  # For saving and loading the model

# Function to extract features from audio files
def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

# # Path to your dataset
# dataset_path = 'Emotions/'  # Replace with your dataset path
# labels = []
# features = []

# # Iterate over all folders and files in the dataset
# for root, dirs, files in os.walk(dataset_path):
#     for filename in files:
#         if filename.endswith('.wav'):
#             label = filename.split('_')[0]  # Assuming labels are part of the filename
#             labels.append(label)
#             feature = extract_features(os.path.join(root, filename))
#             features.append(feature)

# # Create a DataFrame for features and labels
# X = np.array(features)
# y = np.array(labels)

# # Encode labels to integers
# label_encoder = LabelEncoder()
# y_encoded = label_encoder.fit_transform(y)

# # Split the dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# # Train the model
# model = SVC(kernel='linear')
# model.fit(X_train, y_train)

# # Save the trained model and label encoder
# joblib.dump(model, 'emotion_model.pkl')
# joblib.dump(label_encoder, 'label_encoder.pkl')

# # Predict on test set and print classification report
# y_pred = model.predict(X_test)
# print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))


# Function to detect emotion from an input WAV file
def detect_emotion(input_audio_path):
    # Load the saved model and label encoder
    model = joblib.load('emotion_model.pkl')
    label_encoder = joblib.load('label_encoder.pkl')

    # Extract features from the input audio
    input_feature = extract_features(input_audio_path)

    # Reshape the feature to match the model input
    input_feature = input_feature.reshape(1, -1)

    # Make a prediction
    prediction = model.predict(input_feature)

    # Decode the prediction
    predicted_label = label_encoder.inverse_transform(prediction)

    return predicted_label[0]

# Example usage of the emotion detection function
input_file = 'file.wav'  # Replace with your input file path
detected_emotion = detect_emotion(input_file)
print(f'Detected Emotion: {detected_emotion}')
