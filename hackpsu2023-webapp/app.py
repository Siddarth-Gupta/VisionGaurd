from flask import Flask, render_template, request, redirect, url_for, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="retina_scanner.tflite")
interpreter.allocate_tensors()

# Get input and output tensors information
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def preprocess_image(image_path):
    # Open image and preprocess here based on your model's requirements
    # This is a generic example; adjust accordingly.
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img).astype('float32') / 255.0
    return img_array


# Dictionary to map category names to image paths
image_paths = {
    'Normal': "static/2332_left.jpg",
    'Cataract': "static/_0_4015166.jpg",
    'Glaucoma': "static/1213_left.jpg",
    'Diabetes': "static/1000_right.jpeg",
}

#0 = cataract, 1 = diabetic_retinopathy, 2 = glaucoma, 3 = normal, 
idx_to_class = {
    0: 'Cataract',
    1: 'Diabetic Retinopathy',
    2: 'Glaucoma',
    3: 'Normal'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    selected_image = None
    
    if request.method == 'POST':
        disease_type = request.form.get('disease_type')
        selected_image = image_paths.get(disease_type)

        image = preprocess_image(selected_image)
        input_data = image.astype(np.float32)  # Ensure it has the correct shape (224, 224, 3)

        # Set input tensor data
        interpreter.set_tensor(input_details[0]['index'], [input_data])

        # Run inference
        interpreter.invoke()

        # Get the output tensor
        output_details = interpreter.get_output_details()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Use the output data (e.g., post-process and analyze results)
        prediction = idx_to_class[np.argmax(output_data, 1)[0]]
        print(prediction)


    return render_template('index.html', image_paths=image_paths, selected_image=selected_image, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
