import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import numpy as np
import json

model = keras.models.load_model("model/trained_model.keras")

with open("model/class_names.txt", "r", encoding="UTF-8") as file:
    dictionary = json.load(file)

class_names = dictionary["classes"]

img_height = 180
img_width = 180

image_to_test = "cpu.jpg"

img = tf.keras.utils.load_img(
        image_to_test, target_size=(img_height, img_width)
        )

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))
