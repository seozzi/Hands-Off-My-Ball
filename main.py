from scripts.render import RenderWindow
from scripts.animation import Animation
from scripts.character import Character
from scripts.ball import Ball
from scripts.hand import Hand
from scripts.animation_manager import AnimationManager

if __name__ == '__main__':
    width = 1920
    height = 1080

    manager = AnimationManager()

    character = Character()
    ball = Ball()
    right_hand = Hand("Right_Hand_P", manager)
    left_hand = Hand("Left_Hand_P", manager)
    
    animation = Animation(character, ball, manager)

    # Render window.
    renderer = RenderWindow(animation, width, height, "Hands Off My Ball", resizable = True)   
    renderer.set_location(100, 100)

    character.add_parts(renderer)
    ball.add_part(renderer)
    right_hand.add_part(renderer)
    left_hand.add_part(renderer)

    right_hand.bind_window(renderer)
    left_hand.bind_window(renderer)

    renderer.run()
