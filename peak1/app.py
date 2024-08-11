from flask import Flask, render_template, request, redirect, url_for, jsonify
import cv2
import face_recognition
import face_recognition_models
import numpy as np
import os

app = Flask(__name__)

# Load the known images and create encodings
known_face_encodings = []
known_face_names = []

for label in os.listdir('peak1/labeled_images'):
    for filename in os.listdir(f'peak1/labeled_images/{label}'):
        image_path = f'peak1/labeled_images/{label}/{filename}'
        image = face_recognition.load_image_file(image_path)
        image_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(image_encoding)
        known_face_names.append(label)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read the uploaded image
    image = face_recognition.load_image_file(file)
    unknown_face_encodings = face_recognition.face_encodings(image)

    if len(unknown_face_encodings) == 0:
        return jsonify({'message': 'No face detected'}), 200

    # Compare the face with the known faces
    results = face_recognition.compare_faces(known_face_encodings, unknown_face_encodings[0])
    face_distances = face_recognition.face_distance(known_face_encodings, unknown_face_encodings[0])

    best_match_index = np.argmin(face_distances)
    if results[best_match_index]:
        return jsonify({'message': f'Recognized: {known_face_names[best_match_index]}'}), 200
    else:
        return jsonify({'message': 'Unknown face'}), 200

if __name__ == '__main__':
    app.run(debug=True)
