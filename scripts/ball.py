import json
import os
from pyglet.math import Vec3, Quaternion, Mat4
from scripts.primitives import Cube

class Ball:
    def __init__(self):
        json_path = os.path.join("scripts/pose_data", "ball_object.json")
        colors_path = os.path.join("scripts/pose_data", "colors.json")

        with open(json_path) as f:
            data = json.load(f)
        with open(colors_path) as f:
            color_map = json.load(f)

        self.name = "Ball"
        self.rotation = Quaternion()
        self.transform_mat = Mat4()

        self.vertices = []
        self.indices = []
        self.colors = []

        vertex_offset = 0

        for unit in data["Ball"]["unit_boxes"]:
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
        self.scale_ball(scale= 0.7)

    def scale_ball(self, scale):
        # Ball 전체 크기 scale(0.7)배로 줄이기
        for i in range(0, len(self.vertices), 3):
            self.vertices[i] *= scale
            self.vertices[i+1] *= scale
            self.vertices[i+2] *= scale

    def set_origin_to_center(self):
        center = Vec3(4.5, 4.5, 4.5)

        for i in range(0, len(self.vertices), 3):
            self.vertices[i] -= center.x
            self.vertices[i + 1] -= center.y
            self.vertices[i + 2] -= center.z

    def add_part(self, renderer):
        renderer.add_custom_shape(self, Mat4(), self.vertices, self.indices, self.colors)
