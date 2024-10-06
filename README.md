# uniplanets
Basic Pygame planet customizer inspired by Gpopcorn and DaFluffyPotato on YoutTube

![image](https://github.com/user-attachments/assets/a8673fa6-7ad9-4398-a37e-2296864c64be)

Simply add a `Planet` with a `PlanetConfig` to the list of assets in `src/assets.py`:

```python
planet_assets = [
    Planet(
        config=PlanetConfig(
            name="Eve",
            radius=int(((screen_width + screen_height) // 4) * 0.6),  # 60% of the resolution
            position=Vector(x=screen_width // 2, y=screen_height // 2),  # centered relative to the resolution
            level_of_detail=3,
            terrains=[
                Terrain(name="sea", color=RGB(132, 80, 183), threshold=0.6),
                Terrain(name="land", color=RGB(212, 80, 165), threshold=float("inf")),  # last terrain (highest) needs rest of the scale
            ],
            color_mode="solid",
            lighting=base_lighting,  # keep centralized so all planets share the same sun
            rotation=Rotation(direction="left", speed=0.01),
        ),
    ),
]
```