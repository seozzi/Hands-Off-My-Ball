import json
import os
from scripts.body_part import BodyPart
from pyglet.math import Mat4

class Character:
    '''
    Has hierarchy of body parts
    '''

    def __init__(self):
        json_path = os.path.join("scripts/pose_data", "body_objects.json")

        with open(json_path) as f:
            data = json.load(f)

        self.parts = {}
        self.root = self.build_hierarchy("Hip", data["Hip"])

    def build_hierarchy(self, name, current_data):
        '''
        DFS parsing of body_parts.json
        Returns nested Dict of BodyParts
        '''
        part = BodyPart(
            name,
            current_data.get("unit_boxes"),
            current_data.get("joint_data")
            )
        self.parts[name] = part

        for key, val in current_data.items():
            if key != "unit_boxes" and key != "joint_data": # children of this body part
                child_part = self.build_hierarchy(key, val)
                part.children.append(child_part)

        return part

    def add_parts(self, renderer):
        self._add_part(self.root, Mat4(), renderer)

    def _add_part(self, part, parent_matrix, renderer):
        world_matrix = part.get_transform(parent_matrix)

        vertices, indices, colors = part.get_mesh()
        renderer.add_custom_shape(part, world_matrix, vertices, indices, colors)

        for child in part.children:
            self._add_part(child, world_matrix, renderer)
