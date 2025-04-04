import json
import os
from pyglet.math import Vec3, Quaternion, Mat4
from scripts.primitives import Cube
import math

class BodyPart:
    '''
    Reads the unit cube data from Character's json parser,
    combines the unit cubes,
    gets vertices, indices, colors for the body piece,
    and handles local transformation.
    '''
    def __init__(self, name, unit_boxes, joint_data):
        colors_path = os.path.join("scripts/pose_data", "colors.json")

        with open(colors_path) as f:
            color_map = json.load(f)

        self.name = name
        self.children = []

        # for animation
        self.joint_to_parent = Vec3(*joint_data['joint_to_parent'])
        self.joint_from_parent = Vec3(*joint_data['joint_from_parent'])

        self.rotation = Quaternion()  # identity quaternion
        self.offset = Vec3(0.0, 0.0, 0.0)

        self.vertices = []
        self.indices = []
        self.colors = []

        vertex_offset = 0

        for unit in unit_boxes:
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

    def get_transform(self, parent_matrix):
        # 1. 부모의 joint 위치로 이동
        T_from = Mat4.from_translation(self.joint_from_parent)

        # 2. 자식 기준 joint를 원점으로 옮기기 위해 역변환
        T_to = Mat4.from_translation(-self.joint_to_parent)

        # 3. 회전만 적용 (쿼터니언 -> 4x4 행렬)
        R = self.rotation.to_mat4()

        if self.name == "Belly":
            print(self.rotation)

        # 4. 로컬 변환 행렬 = 부모 joint 이동 → 회전 → 자식 joint 기준 역이동
        return parent_matrix @ T_from @ R @ T_to

    def get_mesh(self):
        return self.vertices, self.indices, self.colors
