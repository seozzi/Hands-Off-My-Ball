import json
from pyglet.math import Vec3, Mat4, Quaternion

class AnimationName:
    Idle_R = "Idle_R"
    Idle_L = "Idle_L"
    Cross_LtoR = "Cross_LtoR"
    Cross_RtoL = "Cross_RtoL"


class Animation:
    def __init__(self, character, ball, manager):
        self.character = character
        self.ball = ball
        self.manager = manager

        with open("scripts/pose_data/character_animation_config.json") as f:
            self.character_animations = json.load(f)

        with open("scripts/pose_data/ball_animation_config.json") as f:
            self.ball_animations = json.load(f)
        
        self.time = 0.0
        self.anim_name = manager.get_current_animation_name()

        self._load_animation_data(self.anim_name)

    def _load_animation_data(self, name):
        self.character_animation = self.character_animations[name]
        self.ball_animation = self.ball_animations[name]

        self.keyframes = [int(k) for k in self.character_animation.keys()]
        self.keyframes.sort()

    def update(self, dt, renderer):
        self.time += dt
        t_total = self.time % (1/3)
        t = t_total * 24
        frame_idx = round(t) % len(self.keyframes)

        # loop 한 사이클 끝난 시점이면 animation name 갱신
        if frame_idx == 0:
            new_anim = self.manager.get_current_animation_name()
            if new_anim != self.anim_name:
                self.anim_name = new_anim
                self._load_animation_data(self.anim_name)

        self.update_character_transformation(renderer, frame_idx)
        self.update_ball_transformation(renderer, frame_idx)


    def update_character_transformation(self, renderer, frame_idx):
        frame = self.character_animation[str(frame_idx)]

        for part_name, part in self.character.parts.items():
            if part_name in frame:
                part.rotation = Quaternion(*frame[part_name])

        self._update_body_part(self.character.root, renderer)


    def update_ball_transformation(self, renderer, frame_idx):
        frame = self.ball_animation[str(frame_idx)]
        
        location = Vec3(*frame["location"])
        rotation = Quaternion(*frame["rotation"])

        transform = Mat4.from_translation(location) @ rotation.to_mat4()

        for shape in renderer.shapes:
            if shape.name == "Ball":
                shape.update_transform(transform)
                break


    def _update_body_part(self, part, renderer, parent_matrix=None):
        if parent_matrix is None:
            parent_matrix = Mat4()

        world_matrix = part.get_transform(parent_matrix)

        for shape in renderer.shapes:
            if shape.name == part.name:
                shape.update_transform(world_matrix)
                break

        for child in part.children:
            self._update_body_part(child, renderer, world_matrix)

