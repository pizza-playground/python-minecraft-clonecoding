import numbers


class Block_type:
    def __init__(
        self,
        texture_manager,
        name="unknown",
        block_face_textures={"all": "cobblestone"},
    ):
        self.name = name

        self.vertex_positions = numbers.vertex_positions
        self.tex_coords = numbers.tex_coords.copy()
        self.shading_values = numbers.shading_values

        def set_block_face(face, texture):
            self.tex_coords[face] = self.tex_coords[face].copy()

            for vertex in range(4):
                self.tex_coords[face][vertex * 3 + 2] = texture

        for face in block_face_textures:
            texture = block_face_textures[face]
            texture_manager.add_texture(texture)

            texture_index = texture_manager.textures.index(texture)

            if face == "all":
                for face_index in range(6):
                    set_block_face(face_index, texture_index)
            elif face == "sides":
                for face_index in (0, 1, 4, 5):
                    set_block_face(face_index, texture_index)
            else:
                set_block_face(
                    ["right", "left", "top", "bottom", "front", "back"].index(
                        face
                    ),
                    texture_index,
                )
