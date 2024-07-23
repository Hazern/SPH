import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

import random
from PIL import Image as PILImage

class PuzzleTile(Button):
    def __init__ (self, image, pos, **kwargs):
        super().__init__(**kwargs)
        self.image = image
        self.pos = pos
        self.update_image()

    def update_image(self):
        self.background_normal = ''
        self.background_color = (1, 1, 1, 1)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(
                texture = self.image.texture,
                pos = self.pos,
                size = self.size
            )

class SlidingPuzzleGame(GridLayout):
    def __init__ (self, rows = 3, cols = 3, **kwargs):
        super().__init__(**kwargs)
        self.rows = rows
        self.cols = cols
        self.tiles = []
        self.image = None
        
        self.build_grid()
    
    def build_grid(self):
        self.clear_widgets()
        self.tiles = []

        if self.image:
            self.image_size = self.image_size
            tile_width = self.image_size[0] // self.cols
            tile_height = self.image_size[1] // self.cols

            tile_images = []

            for row in range(self.rows):
                for col in range(self.cols):
                    tile_image = self.image.crop((col * tile_width, row * tile_height, (col + 1) * tile_width, (row + 1) * tile_height))

                    tile_images.append(tile_image)

            random.shuffle(tile_images)

            for idx, tile_image in enumerate(tile_images):
                row = idx // self.cols
                col = idx % self.cols
                texture = self.image_to_texture(tile_image)
                tile = PuzzleTile(texture, pos = (col * tile_width, row * tile_height))
                self.add_widget(tile)
                self.tiles.append(tile)
        
    def image_to_texture(self, image):
        pil_image = PILImage.fromarray(image)
        data = pil_image.tobytes()
        texture = Texture.create(size = pil_image.size)
        texture.blit_buffer(data, colorfmt = 'rgb', bufferfmt = 'ubyte')
        return texture
    
    def load_image(self, path):
        self.image = PILImage.open(path)
        self.build_grid()

class SlidingPuzzleApp(App):
    def build(self):
        self.game = SlidingPuzzleGame()
        return self.game
    
    def on_start(self):
        self.show_file_chooser()
        
    def show_file_chooser(self):
        content = FileChooserIconView(on_selection = self.load_image)
        popup = Popup(title = "Select an Image", content = content, size_hint = (0.9, 0.9))
        popup.open()

    def load_image(self, selection):
        if selection:
            self.game.load_image(selection[0])
        self.popup.dismiss()

if __name__ == '__main__':
    SlidingPuzzleApp.run()