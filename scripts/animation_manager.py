from scripts.animation import AnimationName

class AnimationManager:
    def __init__(self):
        self.current_anim_name = AnimationName.Idle_R
        self.next_anim_name = self.current_anim_name

    def trigger_hover_on_right(self):
        print(f"🖐 Hovering over Right_Hand_P!")

        """Triggered when mouse hovers over right hand."""
        if self.current_anim_name == AnimationName.Idle_L and self.next_anim_name != AnimationName.Cross_LtoR:
            self.set_next_animation(AnimationName.Cross_LtoR)

    def trigger_hover_on_left(self):
        print(f"🖐 Hovering over Left_Hand_P!")

        """Triggered when mouse hovers over left hand."""
        if self.current_anim_name == AnimationName.Idle_R and self.next_anim_name != AnimationName.Cross_RtoL:
            self.set_next_animation(AnimationName.Cross_RtoL)

    def set_next_animation(self, anim_name):
        self.next_anim_name = anim_name

    def get_current_animation_name(self):
        self.current_anim_name = self.next_anim_name

        if self.current_anim_name == AnimationName.Cross_RtoL:
            self.next_anim_name = AnimationName.Idle_L
        elif self.current_anim_name == AnimationName.Cross_LtoR:
            self.next_anim_name = AnimationName.Idle_R

        print(f"다음거 불려가는 거 -> {self.current_anim_name}")
        return self.current_anim_name
