from pyglet.math import Vec3, Vec4, Quaternion, Mat4
import json, os
from scripts.primitives import Cube

class Hand:
    def __init__(self, hand_name: str, animation_manager):
        with open("scripts/pose_data/body_objects.json") as f:
            data = json.load(f)
        with open("scripts/pose_data/colors.json") as f:
            color_map = json.load(f)
        with open("scripts/pose_data/hand_animation_config.json") as f:
            self.hand_animations = json.load(f)

        self.name = hand_name
        self.animation_manager = animation_manager
        self.rotation = Quaternion()
        self.transform_mat = Mat4()

        self.vertices = []
        self.indices = []
        self.colors = []

        vertex_offset = 0

        # === base pose transform 설정 ===
        if hand_name == "Right_Hand_P":
            units = data["Hip"]["Belly"]["Chest"]["Right_Arm"]["Right_Forearm"]["Right_Hand"]["unit_boxes"]
            base_pose = self.hand_animations["base_pose"]["Right_Hand_P"]
        else:
            units = data["Hip"]["Belly"]["Chest"]["Left_Arm"]["Left_Forearm"]["Left_Hand"]["unit_boxes"]
            base_pose = self.hand_animations["base_pose"]["Left_Hand_P"]

        location = Vec3(*base_pose["location"])
        rotation = Quaternion(*base_pose["rotation"])
        self.transform_mat = Mat4.from_translation(location) @ rotation.to_mat4()

        # === vertex setup ===
        for unit in units:
            pos = unit["position"]
            color = tuple(color_map[unit["color"]])
            cube = Cube(scale=Vec3(1, 1, 1), color=color)

            for i in range(0, len(cube.vertices), 3):
                v = Vec3(cube.vertices[i], cube.vertices[i+1], cube.vertices[i+2])
                translated = v + Vec3(*pos)
                self.vertices.extend([translated.x, translated.y, translated.z])

            self.colors.extend(cube.colors)
            self.indices.extend([i + vertex_offset for i in cube.indices])
            vertex_offset += len(cube.vertices) // 3

        self.set_origin_to_center()
        self.scale_hand(3)

    def scale_hand(self, scale):
        for i in range(0, len(self.vertices), 3):
            self.vertices[i] *= scale
            self.vertices[i+1] *= scale
            self.vertices[i+2] *= scale

    def set_origin_to_center(self):
        center = Vec3(2.5, 1.5, 2.5)
        for i in range(0, len(self.vertices), 3):
            self.vertices[i] -= center.x
            self.vertices[i+1] -= center.y
            self.vertices[i+2] -= center.z

    def get_transform(self):
        return self.transform_mat

    def update_transform(self, new_mat: Mat4):
        self.transform_mat = new_mat

    def add_part(self, renderer):
        renderer.add_custom_shape(self, self.get_transform(), self.vertices, self.indices, self.colors)

    def bind_window(self, renderer):
        self.window = renderer
        self._init_hover_bounds()
        self._init_screen_bounds()
        
        renderer.push_handlers(self) # binded window에서 mouse motion 발생 시 Hand class의 on_mouse_motion() 호출
        renderer.interactive_parts.append(self)

    def _init_hover_bounds(self):
        transformed = []

        for i in range(0, len(self.vertices), 3):
            local_v = Vec4(self.vertices[i], self.vertices[i+1], self.vertices[i+2], 1.0)
            world_v = self.transform_mat @ local_v
            transformed.append(world_v)

        xs = [v.x for v in transformed]
        ys = [v.y for v in transformed]
        zs = [v.z for v in transformed]

        self.hover_bounds = {
            "min": Vec3(min(xs), min(ys), min(zs)),
            "max": Vec3(max(xs), max(ys), max(zs)),
        }

    def _init_screen_bounds(self):
        # Get 8 corners of AABB
        min_v = self.hover_bounds["min"]
        max_v = self.hover_bounds["max"]
        corners = [
            Vec3(min_v.x, min_v.y, min_v.z), Vec3(min_v.x, min_v.y, max_v.z),
            Vec3(min_v.x, max_v.y, min_v.z), Vec3(min_v.x, max_v.y, max_v.z),
            Vec3(max_v.x, min_v.y, min_v.z), Vec3(max_v.x, min_v.y, max_v.z),
            Vec3(max_v.x, max_v.y, min_v.z), Vec3(max_v.x, max_v.y, max_v.z),
        ]

        screen_points = []
        for v in corners:
            v4 = Vec4(v.x, v.y, v.z, 1.0)
            clip = self.window.view_proj @ v4

            # Avoid division by 0 (though rare)
            if abs(clip.w) < 1e-6:
                continue

            ndc = clip.xyz / clip.w  # Normalized Device Coordinates (-1 ~ 1)

            screen_x = (ndc.x * 0.5 + 0.5) * self.window.width
            screen_y = (ndc.y * 0.5 + 0.5) * self.window.height
            screen_points.append((screen_x, screen_y))

        xs = [pt[0] for pt in screen_points]
        ys = [pt[1] for pt in screen_points]

        self.screen_bounds = {
            "min": (min(xs), min(ys)),
            "max": (max(xs), max(ys))
        }


    def on_mouse_motion(self, x, y, dx, dy):
        if self.is_screen_hovered(x, y):
            if self.name == "Right_Hand_P":
                self.animation_manager.trigger_hover_on_right()
            else :
                self.animation_manager.trigger_hover_on_left()
                    

    def is_screen_hovered(self, x, y):
        min_x, min_y = self.screen_bounds["min"]
        max_x, max_y = self.screen_bounds["max"]
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def recalculate_screen_bounds(self):
        self._init_screen_bounds()


    


