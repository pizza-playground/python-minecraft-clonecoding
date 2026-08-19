import pyglet

# OpenGL 컨텍스트 생성 시 불필요한 shadow window 비활성화
pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

import pyglet.gl as gl


class Window(pyglet.window.Window):
    def __init__(self, **args):
        super(Window, self).__init__(**args)

    def on_draw(self):
        # 프레임 렌더링 전 화면을 초기화
        gl.glClearColor(1.0, 0.5, 1.0, 1.0)
        self.clear()

    def on_resize(self, width, height):
        print(f"resize {width} * {height}")


class Game:
    def __init__(self):
        # Minecraft 스타일의 3D 렌더링을 위해 OpenGL 3.x 컨텍스트 사용
        self.config = gl.Config(major_version=3)

        self.window = Window(
            config=self.config,
            width=800,
            height=600,
            caption="Minecraft clone",
            resizable=True,
            vsync=False,
        )

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.run()