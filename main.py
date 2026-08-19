import ctypes
import pyglet

# OpenGL 컨텍스트 생성 시 불필요한 shadow window 비활성화
pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl

vertex_positions = [
    -0.5,    0.5,    1.0,
    -0.5,   -0.5,    1.0,
    0.5,    -0.5,    1.0,
    0.5,     0.5,    1.0,
]

indices = [
    0, 1, 2,    # first triangle
    0, 2, 3,    # second triangle
]

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

    def on_draw(self):
        # 프레임 렌더링 전 화면을 초기화
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
        # Minecraft 스타일의 3D 렌더링을 위해 OpenGL 3.x 컨텍스트 사용
        self.config = gl.Config(
            major_version=3,
            minor_version=3
        )

        self.window = Window(
            config=self.config,
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
    
    