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
        '--output_directory',
        help='Enter a directory path to save the resized file.'
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


def get_all_script_arguments(arguments):
    file_path = arguments.file_path
    output_directory_path = arguments.output_directory
    try:
        width_arg = arguments.width
        height_arg = arguments.height
    except AttributeError:
        width_arg = None
        height_arg = None
    try:
        scale_arg = arguments.scale_ratio
    except AttributeError:
        scale_arg = None
    return file_path, output_directory_path, width_arg, height_arg, scale_arg


def get_image(path):
    try:
        input_image = Image.open(path)
        return input_image
    except IOError:
        return None


def get_new_image_size(img, required_width, required_height, scale_ratio):
    image_width = img.width
    image_height = img.height
    if required_width and not required_height:
        scale_rate = required_width / image_width
        required_height = int(image_height * scale_rate)
    if not required_width and required_height:
        scale_rate = required_height / image_height
        required_width = int(image_width * scale_rate)
    if scale_ratio:
        required_width = int(image_width * scale_ratio)
        required_height = int(image_height * scale_ratio)
    return required_width, required_height


def get_new_image_path(input_img_path, new_directory, img_width, img_height):
    if new_directory:
        directory_path = os.path.dirname(new_directory)
    if not new_directory:
        directory_path = os.path.dirname(input_img_path)
    if not directory_path:
        directory_path = os.getcwd()
    input_image_full_name = os.path.basename(input_img_path)
    image_name, image_extension = os.path.splitext(input_image_full_name)
    new_image_name = '{}__{}x{}{}'.format(
        image_name,
        img_width,
        img_height,
        image_extension
    )
    new_image_path = os.path.join(directory_path, new_image_name)
    return new_image_path


def check_proportion_conservation(old_img, new_img):
    old_image_proportion = old_img.width / old_img.height
    new_image_proportion = new_img.width / new_img.height
    proportion_difference = old_image_proportion - new_image_proportion
    small_proportion_difference = 0.01
    return abs(proportion_difference) < small_proportion_difference


def print_script_result(image_path, preserve_proportions):
    if not preserve_proportions:
        print('The ratio between image width and height has been changed.')
    print('The path of edited image: {}'.format(image_path))


if __name__ == '__main__':
    console_arguments, argument_parser = get_console_arguments_and_parser()
    input_path, output_dir, width, height, scale = get_all_script_arguments(
        console_arguments
    )
    if not width and not height and not scale:
        argument_parser.error(
            'At least one argument is required: width, height or scale.'
        )
    image = get_image(input_path)
    if not image:
        exit('Can not open the given file.')
    new_width, new_height = get_new_image_size(image, width, height, scale)
    new_image = image.resize((new_width, new_height))
    proportion_conservation = check_proportion_conservation(image, new_image)
    output_file_path = get_new_image_path(
        input_path,
        output_dir,
        new_width,
        new_height
    )
    new_image.save(output_file_path)
    print_script_result(output_file_path, proportion_conservation)
