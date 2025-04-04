from scripts.render import RenderWindow
from scripts.control import Control
from scripts.animation import Animation
from scripts.character import Character
from scripts.ball import Ball
from scripts.primitives import Cube


if __name__ == '__main__':
    width = 1920
    height = 1080

    character = Character()
    ball = Ball()
    animation = Animation(character, ball)

    # Render window.
    renderer = RenderWindow(animation, width, height, "Hands Off My Ball", resizable = True)   
    renderer.set_location(100, 100)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)

    character.add_parts(renderer)
    # ball.add_part(renderer)

    renderer.run()
