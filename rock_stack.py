import os
import random
from PIL import Image, ImageDraw, ImageFont


rock_components_path = "img/rocks/base"
canvas_width = 110
canvas_height = 110
rocks_file_list = []
for filename in os.listdir(rock_components_path):
    if os.path.isfile(os.path.join(rock_components_path, filename)):
        rocks_file_list.append(f"{rock_components_path}/{filename}")
pass

def stack_number_on_image(image, number):
    image = image.convert('RGBA')
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("arial.ttf", 20)
    text_width, text_height = draw.textsize(str(number), font)
    text_position = ((canvas_width - text_width) // 2, (canvas_height - text_height) // 2)
    text_color = (255, 255, 255, 255)  # White
    draw.text(text_position, str(number), font=font, fill=text_color)
    return image


def scale_image(image, scale_factor):
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    return image.resize((new_width, new_height))


def create_string(string_input: str, player: str):
    string_image = Image.new('RGBA', (canvas_height, canvas_width), (0, 0, 0, 0))
    draw = ImageDraw.Draw(string_image)

    font = ImageFont.truetype("arial.ttf", 20)
    text_width, text_height = draw.textsize(string_input, font)
    text_position = ((canvas_width - text_width) // 2, (canvas_height - text_height) // 2)
    text_color = (255, 255, 255, 255)  # White
    draw.text(text_position, str(string_input), font=font, fill=text_color)
    string_image.save(f'img/names/{player}.png')
    return f'names/{player}.png'


def stack_images(amount: int, row: int, col: int, round_counter: int, board: object = None) -> str:

    final_image = Image.new('RGBA', (canvas_height, canvas_width), (0, 0, 0, 0))

    for _ in range(amount):
        selected_image_filename = random.choice(rocks_file_list)
        selected_image = Image.open(selected_image_filename).convert('RGBA')

        rotation_angle = random.randint(0, 360)
        selected_image = selected_image.rotate(rotation_angle)
        scale_factor = float("{0:.2f}".format(random.uniform(0.80, 1.10)))
        selected_image = scale_image(selected_image, scale_factor)

        final_image.paste(selected_image, (0, 0), selected_image)

    final_image = stack_number_on_image(final_image, amount)
    final_image.save(f'img/rocks/stacked_rocks_{row}_{col}_rnd{round_counter}.png')
    if board: board[row][col] = None
    return f'rocks/stacked_rocks_{row}_{col}_rnd{round_counter}'


# Example usage
if __name__ == '__main__':
    stack_images(random.randint(1, 5), 9, 9, None)
