import pygame  
import json

def load_image(file_name):
    path=f'/home/kira/pygame-tuts/game/sprites/{file_name}'
    img=pygame.image.load(path)
    return img.convert()

def load_sound(filename):
    path=f'/home/kira/pygame-tuts/game/sounds/{filename}'
    pygame.mixer.music.load(path)

class SpriteSheet:
    def __init__(self,filename):
        self.filename=filename
        self.sprite_sheet=load_image(filename)
        if self.filename[0]=='d':
            self.meta_data='dino-sprites.json'
        elif self.filename[0]=='h':
            self.meta_data='misc.json'
        else:
            self.meta_data='fe-sprites.json'
        with open(self.meta_data) as f:
            self.data=json.load(f)
        f.close()

    def get_sprite(self,x,y,w,h):
        sprite=pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0,0),(x,y,w,h))
        return sprite

    def parse_sprite(self,filename):
        dim=self.data['frames'][filename]['frame']
        x,y,w,h=dim['x'],dim['y'],dim['w'],dim['h']
        image=self.get_sprite(x, y, w, h)
        return image

