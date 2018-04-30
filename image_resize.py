import argparse
from PIL import Image


def positive_arguments(console_string):
    try:
        argument = float(console_string)
    except ValueError:
        raise argparse.ArgumentTypeError(
            'The argument should be a real number.'
        )
    if argument <= 0:
        error_message = 'This argument should be bigger than 0.'
        raise argparse.ArgumentTypeError(error_message)
    return argument


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Enter a path of image file.')
    parser.add_argument(
        '-o',
        '--output_path',
        help='Enter a path to save the resized file.'
    )

    subparsers = parser.add_subparsers()

    width_height_parser = subparsers.add_parser(
        'width_and_height',
        help='Enter required width and (or) height of image.')
    width_height_parser.add_argument(
        '--height',
        type=positive_arguments,
        help='Enter an image height.'
    )
    width_height_parser.add_argument(
        '-w',
        '--width',
        type=positive_arguments,
        help='Enter an image width.'
    )

    scale_parser = subparsers.add_parser('scale', help='Enter scale ratio to resize an image.')
    scale_parser.add_argument(
        'scale',
        type=positive_arguments,
        help='Enter a scale ratio of image resizing.'
    )
    args = parser.parse_args()
    return args


def get_image(image_path):
    try:
        image = Image.open(image_path)
    except IOError:
        return None
    return image


def save_image(image, path_to_save):
    image.save(path_to_save)


def resize_image(path_to_original, path_to_result):
    pass


if __name__ == '__main__':
    console_arguments = get_console_arguments()
    file_path = console_arguments.file_path
    picture_width = console_arguments.width
    picture_height = console_arguments.height
    scale_ratio = console_arguments.scale
    output_path = console_arguments.output_path
    picture = get_image(file_path)
    if not picture:
        exit('Can not open the given file.')
    save_image(picture, output_path)

