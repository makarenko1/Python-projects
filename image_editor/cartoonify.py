from ex6_helper import *
from typing import Optional
import math
from sys import argv
import ex6_helper

# CLA PARAMETERS:
NUM_ARGUMENTS = 8
IMAGE_SOURCE_INDEX = 1
CARTOON_DEST_INDEX = 2
MAX_IM_SIZE_INDEX = 3
BLUR_SIZE_INDEX = 4
TH_BLOCK_SIZE_INDEX = 5
TH_C_INDEX = 6
QUANT_NUM_SHADES_INDEX = 7

# ERROR MESSAGE:
ERROR_NUM_ARGUMENTS = "Usage: python3 cartoonify.py <image_src> <cartoon_dest>"\
                      "<max_im_size> <blur_size> <th_block_size> <th_c> "\
                      "<quant_num_shades>"

# LEGAL PIXEL VALUES:
MAX_PIXEL = 255
MIN_PIXEL = 0

# PARAMETERS FOR CONVERTING FROM RGB TO GRAYSCALE:
RED_COEFFICIENT = 0.299
GREEN_COEFFICIENT = 0.587
BLUE_COEFFICIENT = 0.114
RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2



def separate_channels(image: ColoredImage) -> List[List[List[int]]]:
    new_image = []
    for channel in range(len(image[0][0])):
        new_channel = []
        for row in range(len(image)):
            new_row = []
            for column in range(len(image[row])):
                new_row.append(image[row][column][channel])
            new_channel.append(new_row)
        new_image.append(new_channel)
    return new_image


def combine_channels(channels: List[List[List[int]]]) -> ColoredImage:
    if len(channels) == 0:
        return []
    matrix = []
    for row in range(len(channels[0])):
        new_row = []
        for column in range(len(channels[0][row])):
            new_channel = []
            for channel in range(len(channels)):
                new_channel.append(channels[channel][row][column])
            new_row.append(new_channel)
        matrix.append(new_row)
    return matrix


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    new_image = []
    for row in range(len(colored_image)):
        new_row = []
        for column in range(len(colored_image[row])):
            red = colored_image[row][column][RED_INDEX] * RED_COEFFICIENT
            green = colored_image[row][column][GREEN_INDEX] * GREEN_COEFFICIENT
            blue = colored_image[row][column][BLUE_INDEX] * BLUE_COEFFICIENT
            temp = round(red + green + blue)
            temp = min(temp, MAX_PIXEL)
            temp = max(temp, MIN_PIXEL)
            new_row.append(temp)
        new_image.append(new_row)
    return new_image


def blur_kernel(size: int) -> Kernel:
    matrix = []
    for row in range(size):
        new_row = []
        for column in range(size):
            new_row.append(float(1) / float(size**2))
        matrix.append(new_row)
    return matrix


def apply_kernel_helper(image: SingleChannelImage, pixel_row: int,
                        pixel_col: int, radius: int) -> SingleChannelImage:
    projection_matrix = []
    for i in range(pixel_row - radius, pixel_row + radius + 1):
        new_row = []
        for j in range(pixel_col - radius, pixel_col + radius + 1):
            if i < 0 or i >= len(image) or j < 0 or j >= len(image[i]):
                new_row.append(image[pixel_row][pixel_col])
            else:
                new_row.append(image[i][j])
        projection_matrix.append(new_row)
    return projection_matrix


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    radius = int(len(kernel) / float(2))
    new_image = []
    for i in range(len(image)):
        new_row = []
        for j in range(len(image[i])):
            sum_matrix = 0
            projection_matrix = apply_kernel_helper(image, i, j, radius)
            for i_proj in range(len(kernel)):
                for j_proj in range(len(kernel)):
                    sum_matrix += (projection_matrix[i_proj][j_proj] *
                                   kernel[i_proj][j_proj])
            sum_matrix = round(sum_matrix)
            sum_matrix = min(sum_matrix, MAX_PIXEL)
            sum_matrix = max(sum_matrix, MIN_PIXEL)
            new_row.append(sum_matrix)
        new_image.append(new_row)
    return new_image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    y_floor = math.floor(y)
    y_ceil = math.ceil(y)
    x_floor = math.floor(x)
    x_ceil = math.ceil(x)
    a = image[y_floor][x_floor]
    b = image[y_ceil][x_floor]
    c = image[y_floor][x_ceil]
    d = image[y_ceil][x_ceil]
    delta_x = x - x_floor
    delta_y = y - y_floor
    temp = round(a * (1 - delta_x) * (1 - delta_y) +
                 b * delta_y * (1 - delta_x) + c * delta_x * (1 - delta_y) +
                 d * delta_x * delta_y)
    temp = max(temp, MIN_PIXEL)
    temp = min(temp, MAX_PIXEL)
    return temp


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    matrix = []
    for row in range(new_height):
        new_row = []
        for column in range(new_width):
            if row == 0 and column == 0:
                new_row.append(image[0][0])
            elif row == new_height - 1 and column == 0:
                new_row.append(image[len(image) - 1][0])
            elif row == 0 and column == new_width - 1:
                new_row.append(image[0][len(image[0]) - 1])
            elif row == new_height - 1 and column == new_width - 1:
                new_row.append(image[len(image) - 1][len(image[0]) - 1])
            else:
                row_index = ((row + 1) * len(image) / new_height) - 1
                column_index = ((column + 1) * len(image[0]) / new_width) - 1
                new_row.append(bilinear_interpolation(image, row_index,
                                                      column_index))
        matrix.append(new_row)
    return matrix


def scale_down_colored_image(image: ColoredImage, max_size: int) -> Optional[ColoredImage]:
    if len(image) <= max_size and len(image[0]) <= max_size:
        return
    else:
        if len(image[0]) >= len(image):  # width >= height
            # new_height -> current_height
            # new_width -> current_width
            new_width = max_size
            new_height = math.floor(new_width * len(image) / len(image[0]))
        else:
            new_height = max_size
            new_width = math.floor(new_height * len(image[0]) / len(image))
        channels = separate_channels(image)
        new_channels = []
        for channel in channels:
            new_channels.append(resize(channel, new_height, new_width))
        return combine_channels(new_channels)


def invert_rows(matrix: SingleChannelImage) -> SingleChannelImage:
    new_matrix = []
    for row in matrix:
        new_matrix.append(row[::-1])
    return new_matrix


def transpose(matrix: SingleChannelImage) -> SingleChannelImage:
    if not matrix:
        return matrix
    new_matrix = [[] for i in range(len(matrix[0]))]
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            new_matrix[col].append(matrix[row][col])
    return new_matrix


def rotate_90_helper(image: SingleChannelImage,
                     direction: str) -> SingleChannelImage:
    if direction == 'L':
        return transpose(invert_rows(image))
    return invert_rows(transpose(image))


def rotate_90(image: Image, direction: str) -> Image:
    if isinstance(image[0][0], List):  # if the image is 3-dimensional.
        new_channels = []
        for channel in separate_channels(image):
            new_channels.append(rotate_90_helper(channel, direction))
        return combine_channels(new_channels)
    return rotate_90_helper(image, direction)


def calculate_threshold(blurred_image: SingleChannelImage, start_row: int,
                        end_row: int, start_col: int, end_col: int, c: int) -> float:
    sum_pixels = 0
    num_pixels = 0
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            sum_pixels += blurred_image[row][col]
            num_pixels += 1
    return float(sum_pixels) / float(num_pixels) - c


def get_edges(image: SingleChannelImage, blur_size: int,
              block_size: int, c: int) -> SingleChannelImage:
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    new_image = []
    r = block_size // 2
    for row in range(len(blurred_image)):
        new_row = []
        for col in range(len(blurred_image[row])):
            start_row = max(row - r, 0)
            end_row = min(row + r + 1, len(blurred_image))
            start_col = max(col - r, 0)
            end_col = min(col + r + 1, len(blurred_image[0]))
            threshold = calculate_threshold(blurred_image, start_row, end_row,
                                            start_col, end_col, c)
            if blurred_image[row][col] < threshold:
                new_row.append(MIN_PIXEL)
            else:
                new_row.append(MAX_PIXEL)
        new_image.append(new_row)
    return new_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    qimg = []
    for row in range(len(image)):
        new_row = []
        for col in range(len(image[row])):
            new_value = round(math.floor(image[row][col] * (
                    float(N) / float(MAX_PIXEL + 1))) * (float(MAX_PIXEL) /
                                                         float(N - 1)))
            new_row.append(new_value)
        qimg.append(new_row)
    return qimg


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    channels = separate_channels(image)
    quantized_channels = []
    for channel in channels:
        quantized_channels.append(quantize(channel, N))
    return combine_channels(quantized_channels)


def add_mask_helper(image1: SingleChannelImage, image2: SingleChannelImage,
                    mask: List[List[float]]) -> SingleChannelImage:
    new_image = []
    for row in range(len(mask)):
        new_row = []
        for col in range(len(mask[row])):
            new_value = round(image1[row][col] * mask[row][col] +
                              image2[row][col] * (1 - mask[row][col]))
            new_row.append(new_value)
        new_image.append(new_row)
    return new_image


def add_mask_3d(image1: ColoredImage, image2: ColoredImage,
                mask: List[List[float]]) -> ColoredImage:
    channels1 = separate_channels(image1)
    channels2 = separate_channels(image2)
    masked_channels = []
    for i in range(len(channels1)):
        masked_channels.append(add_mask_helper(channels1[i], channels2[i],
                                               mask))
    return combine_channels(masked_channels)


def add_mask(image1: Image, image2: Image, mask: List[List[float]]) -> Image:
    if isinstance(image1[0][0], List):
        return add_mask_3d(image1, image2, mask)
    return add_mask_helper(image1, image2, mask)


def get_mask_from_edges(edges: SingleChannelImage) -> List[List[float]]:
    mask = []
    for row in range(len(edges)):
        new_row = []
        for col in range(len(edges[row])):
            new_row.append(round(float(edges[row][col]) / float(MAX_PIXEL)))
        mask.append(new_row)
    return mask


def cartoonify(image: ColoredImage, blur_size: int, th_block_size: int,
               th_c: int, quant_num_shades: int) -> ColoredImage:
    edges = get_edges(RGB2grayscale(image), blur_size, th_block_size, th_c)
    quantized_image = quantize_colored_image(image, quant_num_shades)
    mask_from_edges = get_mask_from_edges(edges)
    new_channels = []
    for channel in separate_channels(quantized_image):
        new_channels.append(add_mask(channel, edges, mask_from_edges))
    return combine_channels(new_channels)


def check_cla():
    if len(argv) != NUM_ARGUMENTS:
        print(ERROR_NUM_ARGUMENTS)
        return False
    return True


def run():
    if not check_cla():
        return
    loaded_image = ex6_helper.load_image(argv[IMAGE_SOURCE_INDEX])
    max_sized_image = scale_down_colored_image(loaded_image, int(
        argv[MAX_IM_SIZE_INDEX]))
    if max_sized_image is None:
        max_sized_image = loaded_image
    result_image = cartoonify(max_sized_image, int(argv[BLUR_SIZE_INDEX]),
                              int(argv[TH_BLOCK_SIZE_INDEX]),
                              int(argv[TH_C_INDEX]),
                              int(argv[QUANT_NUM_SHADES_INDEX]))
    ex6_helper.save_image(result_image, argv[CARTOON_DEST_INDEX])


if __name__ == "__main__":
    run()
