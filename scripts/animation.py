import json
import math
from pyglet.math import Vec3, Vec4, Mat4, Quaternion

class Animation:
    '''
    Controls the Animation state for Dribble(Idle/Cross)
    Moves Character's BodyPart with update()
    '''
    def __init__(self, character, ball):
        self.character = character
        self.ball = ball
        self.time = 0.0

        with open("scripts/pose_data/pose_config.json") as f:
            self.animations = json.load(f)

        self.keyframes = [int(k) for k in self.animations.keys()]
        self.keyframes.sort()

    def update(self, dt):
        self.time += dt
        t_total = self.time % 0.5  # loop every 0.5 second
        t = t_total * 24           # frame time in 24fps

        # Pick two keyframes to interpolate between
        for i in range(len(self.keyframes)):
            kf1 = self.keyframes[i]
            kf2 = self.keyframes[(i + 1) % len(self.keyframes)]

            if kf1 <= t < kf2 or (kf2 < kf1 and (t >= kf1 or t < kf2)):
                frame_frac = (t - kf1) / (kf2 - kf1) if kf2 > kf1 else (t + 24 - kf1) / (kf2 + 24 - kf1)
                pose1 = self.animations[str(kf1)]
                pose2 = self.animations[str(kf2)]

                for part_name in self.character.parts:
                    if part_name in pose1 and part_name in pose2:
                        q1 = Quaternion(*pose1[part_name])  # w, x, y, z
                        q2 = Quaternion(*pose2[part_name])

                        # Apply quadratic easing based on keyframe ranges
                        if kf1 <= 6:
                            # Use ease-in for the first segment (slow start, fast end)
                            adjusted_frac = frame_frac ** 2
                        elif kf1 > 6:
                            # Use ease-out for the second segment (fast start, slow end)
                            adjusted_frac = 1 - (1 - frame_frac) ** 2
                        else:
                            adjusted_frac = frame_frac

                        q_interp = slerp(q1, q2, adjusted_frac)
                        self.character.parts[part_name].rotation = q_interp

    def adjust_foot_to_ground(self, side):
        hip = self.character.root
        thigh = self.character.parts[f"{side}_Thigh"]
        leg = self.character.parts[f"{side}_Leg"]
        foot = self.character.parts[f"{side}_Foot"]

        world_rot = hip.get_transform() @ thigh.get_transform() @ leg.get_transform()
        local_y = Vec4(0, 1, 0, 0)
        world_y4 = world_rot @ local_y
        world_y3 = Vec3(world_y4.x, world_y4.y, world_y4.z)
        up = Vec3(0, 1, 0)

        axis = world_y3.cross(up)
        if axis.length() > 1e-6:
            angle_cos = world_y3.normalize().dot(up)
            angle = math.acos(angle_cos)
            correction_quat = quaternion_from_axis_angle(axis, angle)
            foot.rotation = correction_quat @ foot.rotation


    def update_parts_transformation(self, renderer):
        self._update_part(self.character.root, renderer)

    def _update_part(self, part, renderer, parent_matrix=None):
        if parent_matrix is None:
            parent_matrix = Mat4()

        # if part.name == "Left_Foot":
        #     self.adjust_foot_to_ground("Left")
        # elif part.name == "Right_Foot":
        #     self.adjust_foot_to_ground("Right")

        world_matrix = part.get_transform(parent_matrix)

        for shape in renderer.shapes:
            if shape.name == part.name:
                shape.update_transform(world_matrix)
                break

        for child in part.children:
            self._update_part(child, renderer, world_matrix)

# === Utility functions ===

def quaternion_from_axis_angle(axis: Vec3, angle_rad: float) -> Quaternion:
    axis = axis.normalize()
    half_angle = angle_rad / 2
    sin_half = math.sin(half_angle)
    cos_half = math.cos(half_angle)
    return Quaternion(
        cos_half,                      # w
        axis.x * sin_half,            # x
        axis.y * sin_half,            # y
        axis.z * sin_half             # z
    )

def slerp(q1: Quaternion, q2: Quaternion, t: float) -> Quaternion:
    dot = q1.w*q2.w + q1.x*q2.x + q1.y*q2.y + q1.z*q2.z
    if dot > 0.9995: # 너무 가까울 경우 ㅣinear interpolation
        result = Quaternion(
            q1.w + t*(q2.w - q1.w),
            q1.x + t*(q2.x - q1.x),
            q1.y + t*(q2.y - q1.y),
            q1.z + t*(q2.z - q1.z)
        )
        return result.normalize()

    theta_0 = math.acos(dot)
    sin_theta_0 = math.sin(theta_0)
    theta = theta_0 * t
    sin_theta = math.sin(theta)

    s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0

    return Quaternion(
        (q1.w * s0) + (q2.w * s1),
        (q1.x * s0) + (q2.x * s1),
        (q1.y * s0) + (q2.y * s1),
        (q1.z * s0) + (q2.z * s1)
    )
