import pyglet
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3
from pyglet.gl import *

from scripts.primitives import CustomGroup



class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    def __init__(self, animation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.cam_eye = Vec3(0, 0, 100)


        self.cam_target = Vec3(0,0,0)
        self.cam_vup = Vec3(0,1,0)
        self.view_mat = None
        '''
        Projection parameters
        '''
        self.z_near = 0.1
        self.z_far = 150
        self.fov = 60
        self.proj_mat = None

        self.shapes = []
        self.setup()

        self.animation = animation
        self.interactive_parts = []


    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
        
        # 2. Create a projection matrix 
        self.proj_mat = Mat4.perspective_projection(
            aspect = self.width/self.height, 
            z_near=self.z_near, 
            z_far=self.z_far, 
            fov = self.fov)
        
        self.view_proj = self.proj_mat @ self.view_mat


    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()


    def update(self, dt):
        self.animation.update(dt, self)
        for part in self.interactive_parts: # right_hand, left_hand
            if hasattr(part, "update"):
                part.update(dt, self)


    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height,
            z_near=self.z_near,
            z_far=self.z_far,
            fov = self.fov
        )

        for part in self.interactive_parts: # right_hand, left_hand
            part.recalculate_screen_bounds()
            return pyglet.event.EVENT_HANDLED


    def add_custom_shape(self, part, transform, vertice, indice, color):
        '''
        Assign a group for each shape
        '''
        shape = CustomGroup(part.name, transform, len(self.shapes))
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES,
                        batch = self.batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color))
        shape.shader_program["view_proj"] = self.view_proj

        self.shapes.append(shape)
         

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    