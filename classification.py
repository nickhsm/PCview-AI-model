import tensorflow as tf
import json

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import pathlib

# Finding image on disk
data_dir = pathlib.Path("data/")

image_count = len(list(data_dir.glob('*/*.jpg')))

print("\n\nNumber of images I could find:")
print(image_count)
print("\n")

# Loading image to memory
batch_size = 32
img_height = 180
img_width = 180

train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
        )

val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
        )

class_names = train_ds.class_names
print("\n")
print("These are the classes that I made:")
print(class_names)
print("\n")

# Optimize for performance
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Augment data
data_augmentation = keras.Sequential(
        [
            layers.RandomFlip(mode="horizontal_and_vertical",
                              # The input_shape must be the first one
                              input_shape=(img_height, img_width, 3)
                              ),
            layers.RandomRotation(0.5),
            layers.RandomZoom(0.2),
            layers.RandomTranslation(height_factor=0.2,
                                     width_factor=0.2),
        ]
    )

# Creating the model
# It's essentialy a blueprint of how to train later
num_classes = len(class_names)

model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(128, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(256, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(512, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dense(num_classes, name="outputs")
    ])


# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# View summery of the model
print("\n\nHere is a summery of the model:\n")
model.summary()

# Earlystopping
early_stop = keras.callbacks.EarlyStopping(
        monitor="val_loss",
        verbose=1,
        patience=3,
        min_delta=0.001
        )

# Train the model
epochs=100
history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[early_stop]
        )

model.save("model/trained_model.keras")

with open("model/class_names.json", "w", encoding="UTF-8") as file:
    dictionary = {}
    dictionary["classes"] = class_names
    file.writelines(json.dumps(dictionary))
