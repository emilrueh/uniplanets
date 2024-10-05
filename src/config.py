from src.utils import pick_color


# display settings
resolution, upscale = "1920x1080", 0.1
fps = 10

screen_width, screen_height = int(int(resolution.split("x")[0]) * upscale), int(int(resolution.split("x")[-1]) * upscale)
print(f"{screen_width}x{screen_height} {fps}fps")

display_caption = "Planets"
background_color = pick_color("black")

# planet settings
lighting_speed = 0.1
rotation_speed = 0.1
starting_angle = 1.5  # dark
level_of_detail = 2
color_mode = "change"  # "solid", "change"
