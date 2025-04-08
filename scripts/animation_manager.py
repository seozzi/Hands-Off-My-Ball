import json
from scripts.animation import Animation, AnimationName

class AnimationManager:
    def __init__(self):
        self.current_anim_name = AnimationName.Idle_R
        self.next_anim_name = self.current_anim_name

    def trigger_hover_on_right(self):
        """Triggered when mouse hovers over right hand."""
        if self.current_anim_name == AnimationName.Idle_R:
            self.set_next_animation(AnimationName.Cross_RtoL)
        elif self.current_anim_name == AnimationName.Idle_L:
            self.set_next_animation(AnimationName.Cross_LtoR)

    def trigger_hover_on_left(self):
        """Triggered when mouse hovers over left hand."""
        if self.current_anim_name == AnimationName.Idle_R:
            self.set_next_animation(AnimationName.Cross_RtoL)
        elif self.current_anim_name == AnimationName.Idle_L:
            self.set_next_animation(AnimationName.Cross_LtoR)

    def set_next_animation(self, anim_name):
        if anim_name != self.current_anim_name:
            self.next_anim_name = anim_name


    def get_current_animation_name(self):
        self.current_anim_name = self.next_anim_name

        if self.current_anim_name == AnimationName.Cross_RtoL:
            self.next_anim_name = AnimationName.Idle_L
        elif self.current_anim_name == AnimationName.Cross_LtoR:
            self.next_anim_name = AnimationName.Idle_R

        return self.current_anim_name
