# Image Resizer

This script resizes an image according to user wishes.
Script gets an image and required image size and returns
a new image having required features.

# How To Install

Python v3.5 should be already installed. 
Afterwards use pip (or pip3 if there is a conflict with old Python 2 setup)
to install dependecies:

```bash
pip install -r requirements.txt # alternatively try pip3
```
Remember that it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) 
for better isolation.

# Quick Start

An image file path is the positional argument of the script.
An output image path is the optional argument. 
By default the output image is saved in the directory of input image.

Moreover, user should set at least one of these arguments: 
1. new image height (pixels number), 
2. new image width (pixels number), 
3. scale rate to resize an image.

To run script on Linux:
```bash
$ python image_resize.py /home/image.jpg --output_path /home/img width_height --width 500 --height 400
The path of edited image: /home/img/image__500x400.jpg
```
 Windows usage is the same.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
