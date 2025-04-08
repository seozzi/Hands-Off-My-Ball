import json
import os
from pyglet.math import Vec3, Quaternion, Mat4
from scripts.primitives import Cube

class Hand:
    def __init__(self, hand_name: str):
        json_path = os.path.join("scripts/pose_data", "body_objects.json")
        colors_path = os.path.join("scripts/pose_data", "colors.json")

        with open(json_path) as f:
            data = json.load(f)
        with open(colors_path) as f:
            color_map = json.load(f)

        self.name = hand_name
        self.rotation = Quaternion()
        self.transform_mat = Mat4()

        self.vertices = []
        self.indices = []
        self.colors = []

        vertex_offset = 0

        if hand_name == "Right_Hand_P":
            units = data["Hip"]["Belly"]["Chest"]["Right_Arm"]["Right_Forearm"]["Right_Hand"]["unit_boxes"]
        else:
            units = data["Hip"]["Belly"]["Chest"]["Left_Arm"]["Left_Forearm"]["Left_Hand"]["unit_boxes"]

        for unit in units:
            pos = unit["position"]
            color_name = unit["color"]
            color = tuple(color_map[color_name])

            cube = Cube(scale=Vec3(1.0, 1.0, 1.0), color=color)
            transformed_vertices = []

            for i in range(0, len(cube.vertices), 3):
                v = Vec3(cube.vertices[i], cube.vertices[i+1], cube.vertices[i+2])
                translated = v + Vec3(*pos)
                transformed_vertices.extend([translated.x, translated.y, translated.z])

            self.vertices.extend(transformed_vertices)
            self.colors.extend(cube.colors)
            self.indices.extend([i + vertex_offset for i in cube.indices])
            vertex_offset += len(cube.vertices) // 3

        self.set_origin_to_center()
        self.scale_hand(scale= 3)

    def scale_hand(self, scale):
        for i in range(0, len(self.vertices), 3):
            self.vertices[i] *= scale
            self.vertices[i+1] *= scale
            self.vertices[i+2] *= scale

    def set_origin_to_center(self):
        center = Vec3(2.5, 1.5, 2.5)

        for i in range(0, len(self.vertices), 3):
            self.vertices[i] -= center.x
            self.vertices[i + 1] -= center.y
            self.vertices[i + 2] -= center.z

    def get_transform(self):
        return self.transform_mat

    def update_transform(self, new_mat: Mat4):
        self.transform_mat = new_mat

    def add_part(self, renderer):
        renderer.add_custom_shape(self, self.get_transform(), self.vertices, self.indices, self.colors)
