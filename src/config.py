from src.utils import pick_color, RGB, Terrain


# display settings
resolution, upscale = "1920x1080", 0.05
fps = 18

screen_width, screen_height = int(int(resolution.split("x")[0]) * upscale), int(int(resolution.split("x")[-1]) * upscale)
print(f"{screen_width}x{screen_height} {fps}fps")

display_caption = "Planets"
background_color = pick_color("black")

# planet settings
lighting_speed = 0.01
rotation_speed = 0.01
rotation_direction = "left"
starting_angle = 0  # dark
level_of_detail = 1
color_mode = "change"  # "solid", "change"
terrains = {
    "earth": [
        Terrain(name="deep_water", color=RGB(50, 112, 211), threshold=0.55),
        Terrain(name="shallow_water", color=RGB(100, 152, 234), threshold=0.6),
        Terrain(name="coast", color=RGB(238, 232, 169), threshold=0.62),
        Terrain(name="land", color=RGB(140, 185, 122), threshold=0.7),
        Terrain(name="forest", color=RGB(84, 161, 109), threshold=float("inf")),
    ],
    "moon": [
        Terrain(name="dust", color=RGB(65, 70, 73), threshold=0.6),
        Terrain(name="rim", color=RGB(45, 48, 51), threshold=0.65),
        Terrain(name="crater", color=RGB(32, 34, 35), threshold=float("inf")),
    ],
}
