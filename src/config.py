from src.utils import pick_color


# display settings
resolution, upscale = "1920x1080", 0.2
fps = 18

screen_width, screen_height = int(int(resolution.split("x")[0]) * upscale), int(int(resolution.split("x")[-1]) * upscale)
print(f"{screen_width}x{screen_height} {fps}fps")

display_caption = "Planets"
background_color = pick_color("black")

# planet settings
rotation_speed = 0.1
starting_angle = 1.5  # dark
color_mode = "solid"  # "solid", "change"
