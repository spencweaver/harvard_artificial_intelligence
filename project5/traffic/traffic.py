import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # create a list for the labels and images
    labels = []
    images = []
    for category in range(NUM_CATEGORIES):
        # cast the category as a string and use in index the path
        category = str(category)
        path = f"{data_dir}{os.sep}{category}"

        # process each image file in the folder
        # by reading in the img and resizing it
        # then append the category and image to their respective lists
        for data in os.listdir(path):
            img = cv2.imread(os.path.join(data_dir, category, data))
            resized = cv2.resize(
                img, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA
                )
            images.append(resized)
            labels.append(category)

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Initialize a model for a seqential neural network
    model = keras.models.Sequential([
        # Define the input layer to support the image size
        layers.Reshape(
            (IMG_WIDTH, IMG_HEIGHT, 3),
            input_shape=[IMG_WIDTH, IMG_HEIGHT, 3, ]
            ),

        # Do three rounds of convolution and pooling
        layers.Conv2D(
            50, activation='relu', kernel_size=3, padding="same"
            ),
        layers.MaxPool2D(pool_size=2),


        layers.Conv2D(
            40, activation='relu', kernel_size=3, padding="same"
            ),
        layers.MaxPool2D(pool_size=2),

        layers.Conv2D(
            30, activation='relu', kernel_size=3, padding="same"
            ),
        layers.MaxPool2D(pool_size=2),

        # # create a final layer before flattening
        layers.Conv2D(
            30, activation='relu', kernel_size=3, padding="same"
            ),

        # flatten the image to make a set of vectors
        layers.Flatten(),

        # Create one more dense layer
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),

        # Output to 43 neurons because
        # that is the NUM_CATEGORIES we are looking for
        layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    # compile the model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    main()
