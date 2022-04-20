import sys
import time
from pathlib import Path

import numpy as np
import tensorflow as tf
import d3dshot
from PIL import Image

from src.storage import process_death, add_session


def capture_anything():
    print('capture something')


# need to specify class labels, copied from training phase
class_names = ['death', 'non-death']

# Load trained model
models_file_path = Path().resolve().parent / 'models'
model_file = models_file_path / 'theModel'

model = tf.keras.models.load_model(model_file)
print('Model loaded. Ready to start screen capture\n')

# Need to preprocess images the same way as we did during training
# resizing them first
frame_size_ratio = 1 / 4
frame_size = tuple((frame_size_ratio * np.array([1920, 1080])).astype(int))

# define cropped region shape (same as training input size)
# NOTE numpy format: y, x, n_channels  -- i.e. height, width, 3 (from rgb)
cropped_shape = 54, 125, 3
# print(f'cropped images should have shape {cropped_shape}')


def resize_frame(frame):
    return np.array(Image.fromarray(frame).resize(frame_size))


def get_cropped_bounds():
    x, y = frame_size

    x_margin = 0.37
    y_margin = 0.40
    x_offset = 0
    y_offset = 0.01

    x_min = int(x * (x_margin + x_offset))
    x_max = int(x * ((1 - x_margin) + x_offset))
    y_min = int(y * (y_margin + y_offset))
    y_max = int(y * ((1 - y_margin) + y_offset))

    return y_min, y_max, x_min, x_max


cy_min, cy_max, cx_min, cx_max = get_cropped_bounds()


# after screenshot is resized, we extract cropped region
def get_death_text_crop(im, debug=False):
    cropped = im[cy_min: cy_max, cx_min:cx_max, :]

    if debug:
        print(
            f'Image shape {im.shape} cropped to region x:{cx_min, cx_max} y:{cy_min, cy_max} with shape {cropped.shape}'
        )

    return cropped


def preprocess_captured_frame(img_array):
    img_array = resize_frame(img_array)
    img_array = get_death_text_crop(img_array)
    return img_array


def classify_image_array(img_array, print_image=False):
    img_array_batch = tf.expand_dims(img_array, 0)  # Create a batch
    # print(f'img array expanded shape {img_array_batch.shape}')
    predictions = model.predict(img_array_batch)
    score = tf.nn.softmax(predictions[0])

    if print_image:
        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[np.argmax(score)], 100 * np.max(score))
        )
    return class_names[np.argmax(score)], np.max(score)


def classify_capture(img_array, *args, **kwargs):
    # preprocess and then run inference
    img_array = preprocess_captured_frame(img_array)
    return classify_image_array(img_array, *args, **kwargs)


# Need to capture frames from screen to run inference on model so we can motivate player on death
#
# To install d3dshot, use fork in this way:
#   fork: https://github.com/fauskanger/D3DShot
#   pip install git+https://github.com/<user>/D3DShot.git#egg=D3DShot
#     ref.: https://github.com/SerpentAI/D3DShot/issues/44
#
#   Quirk on laptops
#      TL;DR: run Python script on integrated gpu and not dedicated gpu on laptops#
#      https://github.com/SerpentAI/D3DShot/wiki/Installation-Note:-Laptops
#      https://docs.microsoft.com/en-US/troubleshoot/windows-client/shell-experience/error-when-dda-capable-app-is-against-gpu


def run_a_test():
    # Test by tabbing into fullscreen video with death: https://youtu.be/-n93tXWPggc
    # Will capture a screenshot, preprocess and run inference every second 15 times
    d = d3dshot.create(capture_output="numpy")
    for i in range(15):
        time.sleep(1)
        img_array = d.screenshot()
        class_name, score = classify_capture(img_array, print_image=False)
        if class_name == 'death':
            print(f'You died (confidence: {(score*100):>3.2f}) but you can do better!')


def run_forever(character):
    # Will capture a screenshot, preprocess and run inference every second until stopped.
    # After death, a five seconds cool-down is used to prevent counting same death more than once.
    add_session(character)
    d = d3dshot.create(capture_output="numpy")
    cooldown_seconds = 0
    try:
        while "program is running":
            time.sleep(1)
            cooldown_seconds = max(0, cooldown_seconds-1)
            if cooldown_seconds > 0:
                continue
            img_array = d.screenshot()
            class_name, score = classify_capture(img_array)
            if class_name == 'death':
                cooldown_seconds = 5
                process_death(character, score)
    except KeyboardInterrupt:
        print('\nExiting script...')
        sys.exit()

