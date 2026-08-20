import ctypes
import pyglet

# OpenGL 컨텍스트 생성 시 불필요한 shadow window 비활성화
pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl

import matrix
import shader
import math

class Window(pyglet.window.Window):
    def __init__(self, **args):
        super(Window, self).__init__(**args)

        # Vertex Array Object 생성
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)
        
        # Vertex Buffer Object 생성
        self.vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        
        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        ctypes.sizeof(gl.GLfloat * len(vertex_positions)),
                        (gl.GLfloat * len(vertex_positions)) (*vertex_positions),
                        gl.GL_STATIC_DRAW
                        )
        
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)
        
        # Index buffer object 생성
        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.ibo))
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
                        ctypes.sizeof(gl.GLuint * len(indices)),
                        (gl.GLuint * len(indices)) (*indices),
                        gl.GL_STATIC_DRAW
                        )

        # shader 생성
        self.shader = shader.Shader("vert.glsl", "grag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        self.shader.use()

        # matrices 생성
        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()
        
        self.x = 0
        pyglet.clock.schedule_interval(self.update, 1.0/60)
        
    def update(self, delta_time):
        self.x += delta_time

    def on_draw(self):
        
        # projection matrix 생성
        self.p_matrix.load_identity()
        self.p_matrix.perspective(90, float(self.width) / self.height, 0.1, 500)
        
        # modelview matrix 생성
        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -1)
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)
        
        # modelviewprojection matrix
        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.use()
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)
        
        # 아무거나 그리기w
        gl.glClearColor(1.0, 0.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(indices),
            gl.GL_UNSIGNED_INT,
            None
        )

    def on_resize(self, width, height):
        print(f"resize {width} * {height}")
        gl.glViewport(0, 0, width, height)


class Game:
    def __init__(self):
        self.window = Window(
            width=800,
            height=600,
            caption="Minecraft clone",
            resizable=True,
            vsync=False,
        )
        
        print("OpenGL Version:", gl.gl_info.get_version())
        print("Renderer:", gl.gl_info.get_renderer())

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.run()
    
    
