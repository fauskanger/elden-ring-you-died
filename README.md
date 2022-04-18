This is the root folder for the project. 
We wanted to make a motivational death counter for the video game Elden Ring (2022). 

## How to use the `YouDied`-package

You probably want to look at the [README for the youdied package][ydrm] in the `youdied`-folder 
if you're here to learn how to use it. 
 

[ydrm]: https://github.com/fauskanger/elden-ring-you-died/tree/main/youdied

## Are you a nerd with a desire to know how it works?

If you're looking for more than just info on how to use the package,
e.g. if you want to learn how to make something similar yourself, 
then continue reading. 

The three Jupyter Notebooks are:

 - `createImages.ipynb` - used to create images (.png) from many hours of screen recordings (.mkv) 
 - `createModel.ipynb`  - used to train a Tensorflow model from a tiny subset of those images
 - `createScreenCaptures.ipynb` - used to verify screen capture and running inference

The folder `elden_ring_death_dataset` is the manually (aka "sloppily curated") dataset 
with 100 images of death frames and 900 images of non-death frames, 
all cropped to a region around the "YOU DIED" message shown by the game when the player dies. (Duh)

Those 1000 images are used to train, validate and test a very simple convolutional neural network 
so that it may serve as our "death" or "not death" image recognition model.

The full dataset we have (as of writing) is nearly 300 000 images (from aproxx. 75 hours of video), 
but this computer vision problem is very simple so that is a lot more than we need.
Most of the frames in the full dataset are "not death" frames, and we need more examples to 
cover the higher variance, but the positive "death" frames have a clear and consistent 
structure. 

Further, the "non death" frames before and after "death" frames are included in the training set 
to assist the model to differentiate between them based on the overlay. 
Other than that, we want to include as much variety as we find without spending too much 
time on it, so we have frames from menus, maps, varius biomes, times of day etc.

The `youdied` folder is the pypi package used to easily distribute and install it on other machines, 
and provide a CLI to start and configure the death message detector. 