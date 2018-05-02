import argparse
from PIL import Image
import os


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


def get_console_arguments(arguments):
    input_path = arguments.file_path
    output_path = arguments.output_path
    try:
        width = arguments.width
    except AttributeError:
        width = None
    try:
        height = arguments.height
    except AttributeError:
        height = None
    try:
        scale_ratio = arguments.scale_ratio
    except AttributeError:
        scale_ratio = None
    return input_path, output_path, width, height, scale_ratio


def check_console_arguments(width_input, height_input):
    correct_arguments = True
    if any([width_input, height_input]):
        if not height_input and not width_input:
            correct_arguments = False
    return correct_arguments


def get_console_arguments_and_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Enter a path of image file.')
    parser.add_argument(
        '-o',
        '--output_path',
        help='Enter a path to save the resized file.'
    )
    subparsers = parser.add_subparsers()

    width_height_parser = subparsers.add_parser(
        'width_height',
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

    scale_parser = subparsers.add_parser(
        'scale',
        help='Enter scale ratio to resize an image.'
    )
    scale_parser.add_argument(
        'scale_ratio',
        type=positive_arguments,
        help='Enter a scale ratio of image resizing.'
    )

    args = parser.parse_args()
    return args, parser


def get_image(path):
    try:
        image = Image.open(path)
    except IOError:
        return None
    return image


def get_resized_image(image, width, height, scale_ratio):
    image_width = image.size[0]
    image_height = image.size[1]
    keep_proportions = True
    if width and height:
        required_width = int(width)
        required_height = int(height)
        keep_proportions = False
    if width and not height:
        required_width = int(width)
        scale_ratio = required_width/image_width
        required_height = int(image_height * scale_ratio)
    if not width and height:
        required_height = int(height)
        scale_ratio = required_height/image_height
        required_width = int(image_width * scale_ratio)
    if scale_ratio:
        required_width = int(image_width * scale_ratio)
        required_height = int(image_height * scale_ratio)
    resized_image = image.resize((required_width, required_height))
    return resized_image, required_width, required_height, keep_proportions


def get_new_image_path(input_path, new_path, width, height):
    if new_path:
        directory_path = os.path.dirname(new_path)
    if not new_path:
        directory_path = os.path.dirname(input_path)
    if directory_path == '':
        directory_path = os.getcwd()
    input_image_full_name = os.path.basename(input_path)
    input_image_name = os.path.splitext(input_image_full_name)[0]
    input_image_extension = os.path.splitext(input_image_full_name)[1]
    new_image_name = '{}__{}x{}{}'.format(
        input_image_name,
        width,
        height,
        input_image_extension
    )
    new_image_path = os.path.join(directory_path, new_image_name)
    return new_image_path


def print_script_result(image_path, preserve_proportions):
    if not preserve_proportions:
        print('The ratio between image width and height has been changed.')
    print('The path of edited image: {}'.format(image_path))


if __name__ == '__main__':
    console_arguments, argument_parser = get_console_arguments_and_parser()
    source_picture_path, new_picture_path, width_arg, height_arg, scale_arg =\
        get_console_arguments(console_arguments)
    proper_arguments = check_console_arguments(width_arg, height_arg)
    if proper_arguments is False:
        argument_parser.error(
            'At least one argument is required: width, height or scale.'
        )
    picture = get_image(source_picture_path)
    if not picture:
        exit('Can not open the given file.')
    new_picture, new_width, new_height, the_same_proportions = \
        get_resized_image(picture, width_arg, height_arg, scale_arg)
    new_picture_path = get_new_image_path(
        source_picture_path,
        new_picture_path,
        new_width,
        new_height
    )
    new_picture.save(new_picture_path)
    print_script_result(new_picture_path, the_same_proportions)
