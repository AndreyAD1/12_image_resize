import argparse
from PIL import Image
import os


def positive_integer_arguments(console_string):
    try:
        argument = int(console_string)
    except ValueError:
        error_message = 'The argument should be an integer.'
        raise argparse.ArgumentTypeError(error_message)
    if argument <= 0:
        error_message = 'This argument should be bigger than 0.'
        raise argparse.ArgumentTypeError(error_message)
    return argument


def positive_real_arguments(console_string):
    try:
        argument = float(console_string)
    except ValueError:
        error_message = 'The argument should be a real number.'
        raise argparse.ArgumentTypeError(error_message)
    if argument <= 0:
        error_message = 'This argument should be bigger than 0.'
        raise argparse.ArgumentTypeError(error_message)
    return argument


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
        type=positive_integer_arguments,
        help='Enter an image height.'
    )
    width_height_parser.add_argument(
        '-w',
        '--width',
        type=positive_integer_arguments,
        help='Enter an image width.'
    )

    scale_parser = subparsers.add_parser(
        'scale',
        help='Enter scale ratio to resize an image.'
    )
    scale_parser.add_argument(
        'scale_ratio',
        type=positive_real_arguments,
        help='Enter a scale ratio of image resizing.'
    )
    args = parser.parse_args()
    return args, parser


def get_all_script_arguments(arguments_from_console):
    arguments = ['file_path', 'output_path', 'width', 'height', 'scale_ratio']
    input_arguments_dict = arguments_from_console.__dict__
    all_arguments_dict = {}
    for argument in arguments:
        try:
            input_argument_value = input_arguments_dict[argument]
        except KeyError:
            input_argument_value = None
        all_arguments_dict[argument] = input_argument_value
    file_path = all_arguments_dict['file_path']
    output_file_path = all_arguments_dict['output_path']
    width = all_arguments_dict['width']
    height = all_arguments_dict['height']
    scale = all_arguments_dict['scale_ratio']
    return file_path, output_file_path, width, height, scale


def get_image(path):
    try:
        image = Image.open(path)
    except IOError:
        return None
    return image


def get_new_image_features(image, required_width, required_height, scale_rate):
    width_index = 0
    height_index = 1
    image_width = image.size[width_index]
    image_height = image.size[height_index]
    saving_image_proportions = True
    if required_width and required_height:
        saving_image_proportions = False
    if required_width and not required_height:
        scale_rate = required_width / image_width
        required_height = int(image_height * scale_rate)
    if not required_width and required_height:
        scale_rate = required_height / image_height
        required_width = int(image_width * scale_rate)
    if scale_rate:
        required_width = int(image_width * scale_rate)
        required_height = int(image_height * scale_rate)
    return required_width, required_height, saving_image_proportions


def get_new_image_path(input_image_path, new_path, width, height):
    if new_path:
        directory_path = os.path.dirname(new_path)
    if not new_path:
        directory_path = os.path.dirname(input_image_path)
    if directory_path == '':
        directory_path = os.getcwd()
    input_image_full_name = os.path.basename(input_image_path)
    input_image_name_and_extension = os.path.splitext(input_image_full_name)
    name_index = 0
    extension_index = 1
    input_image_name = input_image_name_and_extension[name_index]
    input_image_extension = input_image_name_and_extension[extension_index]
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
    input_path, output_path, width_arg, height_arg, scale_arg =\
        get_all_script_arguments(console_arguments)
    if not width_arg and not height_arg and not scale_arg:
        argument_parser.error(
            'At least one argument is required: width, height or scale.'
        )
    picture = get_image(input_path)
    if not picture:
        exit('Can not open the given file.')
    new_width, new_height, proportion_conservation = \
        get_new_image_features(picture, width_arg, height_arg, scale_arg)
    new_picture = picture.resize((new_width, new_height))
    output_path = get_new_image_path(
        input_path,
        output_path,
        new_width,
        new_height
    )
    new_picture.save(output_path)
    print_script_result(output_path, proportion_conservation)
