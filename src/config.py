from src.utils import pick_color, RGB, Terrain, PlanetConfig, Lighting, Rotation, Vector


# display settings
resolution, upscale = "1920x1080", 0.05
fps = 30

screen_width, screen_height = int(int(resolution.split("x")[0]) * upscale), int(int(resolution.split("x")[-1]) * upscale)
print(f"{screen_width}x{screen_height} {fps}fps")

display_caption = "UniPlanets"
background_color = pick_color("black")

# planet settings
base_lighting = Lighting(angle=-1.5, speed=0.01, intensity=1.0)
base_rotation = Rotation(direction="left", speed=0.01, axis="y", angle=0.0)
base_lod = 1
base_radius = int(((screen_width + screen_height) // 4) * 0.6)
base_position = Vector(x=screen_width // 2, y=screen_height // 2)

terrains = {
    "earth": [
        Terrain(name="deep_water", color=RGB(50, 112, 211), threshold=0.55),
        Terrain(name="shallow_water", color=RGB(100, 152, 234), threshold=0.6),
        Terrain(name="coast", color=RGB(238, 232, 169), threshold=0.62),
        Terrain(name="land", color=RGB(140, 185, 122), threshold=0.7),
        Terrain(name="forest", color=RGB(84, 161, 109), threshold=float("inf")),
    ],
    "moon": [
        Terrain(name="dust", color=RGB(65, 70, 73), threshold=0.4),
        Terrain(name="rim", color=RGB(45, 48, 51), threshold=0.7),
        Terrain(name="crater", color=RGB(32, 34, 35), threshold=float("inf")),
    ],
    "mars": [
        Terrain(name="desert", color=RGB(160, 80, 43), threshold=0.6),
        Terrain(name="mountain", color=RGB(214, 133, 83), threshold=float("inf")),
    ],
}
