from math import sqrt
from utils import SpriteSheet,load_image
from pygame import font


red=(255,0,0)

class GameObject:
    def __init__(self,screen):
        self.screen=screen
        self.status=SpriteSheet('heal_full.png')
        self.title=SpriteSheet('heroandfoe.png')
        self.animate_dragon()
        self.animate_female()

    def animate_dragon(self):
        dragon_stand=SpriteSheet('dr_stand.png')
        dr_stand=[dragon_stand.parse_sprite(f'dr_stand{v}.png') for v in range(1,5)]
        dr_stand.extend(dr_stand)
        self.dr_stand_animation=dr_stand+[dr_stand[-2]]+[dr_stand[-1]]
        dragon_attack=SpriteSheet('dr_attack.png')
        attack_animation=[dragon_attack.parse_sprite(f'dr_attack{v}.png') for v in range(1,8)]
        self.dr_attack_animation=attack_animation+[attack_animation[6]]+[attack_animation[1]]+[attack_animation[0]]
        dragon_hurt=SpriteSheet('dr_hurt.png')
        img1,img2,img3,img4=[dragon_hurt.parse_sprite(f'dr_hurt{v}.png') for v in range(1,5)]
        self.dr_hurt_animation=[img1]*3+[img2]*2+[img3]*2+[img4]*3
        dead=SpriteSheet('dr_dead.png')
        self.dr_dead_animation=[dead.parse_sprite(f'dr_dead{v}.png') for v in range(1,6)]


    def animate_female(self):
        female_stand=SpriteSheet('fe_stand.png')
        img1,img2=[female_stand.parse_sprite(f'fe-stand{v}.png') for v in range(1,3)]
        self.fe_stand_animation=[img1]*5+[img2]*5
        female_attack=SpriteSheet('fe_attack.png')
        attack_animation=[female_attack.parse_sprite(f'fe-attack{v}.png') for v in range(1,8)]
        self.fe_attack_animation=attack_animation+[attack_animation[-1]]*3
        female_attack=SpriteSheet('fe_attack2.png')
        img1,img2,img3=[female_attack.parse_sprite(f'fe-attack1{v}.png') for v in range(1,4)]
        self.fe_attack2_animation=[img1]+[img2]+[img3]*6+[img1]*2
        female_hurt=SpriteSheet('fe_hurt.png')
        img1,img2,img3,img4=[female_hurt.parse_sprite(f'fe-hurt{v}.png') for v in range(1,5)]
        self.fe_hurt_animation=[img1]+[img2]+[img3]+[img4]*7
        laser=SpriteSheet('hlaser.png')
        self.laser_animation=[laser.parse_sprite(f'laser{v}.png') for v in range(1,7)]


class Dragon(GameObject):
    def __init__(self,screen):
        super().__init__(screen)
    
    def draw(self,frame_count):
        img=self.anime[frame_count]
        size=img.get_rect()
        self.screen.blit(img,(50,450-size[3]))
        
    def choose_action(self,action):
        if action == 'stand':
            self.anime=self.dr_stand_animation
        elif action == 'attack':
            self.anime=self.dr_attack_animation
        elif action == 'hurt':
            self.anime=self.dr_hurt_animation
        else:
            self.anime=self.dr_dead_animation

    def get_score(self,val):
        blood=self.status.parse_sprite(f'status{val}.png')
        name=self.title.parse_sprite(f'title{1}.png')
        name.set_colorkey((0,0,0))
        blood.set_colorkey((0,0,0))
        self.screen.blit(blood, (20+(20*(val-1)),0))
        self.screen.blit(name,(20,40))

class Female(GameObject):
    def __init__(self,screen):
        super().__init__(screen)
        
    def draw(self,frame_count):
        img=self.anime[frame_count]
        self.screen.blit(img,(900,280))
        
    def choose_action(self,action):
        if action == 'stand':
            self.anime=self.fe_stand_animation
        elif action == 'attack':
            self.anime=self.fe_attack_animation
        elif action == 'attack2':
            self.anime=self.fe_attack2_animation
        elif action == 'hurt':
            self.anime=self.fe_hurt_animation

    def get_score(self,val):
        blood=self.status.parse_sprite(f'status{val}.png')
        name=self.title.parse_sprite(f'title{2}.png')
        name.set_colorkey((0,0,0))
        blood.set_colorkey((0,0,0))
        self.screen.blit(blood,(730,0))
        self.screen.blit(name,(730,40))


class Fireball(GameObject):
    def __init__(self,screen,position):
        super().__init__(screen)
        self.position=position
        self.img=load_image('fireball.png')

    def draw(self,set_draw,frame_count):
        if set_draw and frame_count > 1:
            self.img.set_colorkey((0,0,0))    
            self.screen.blit(self.img,self.position)
            self.position=self.get_path(self.position)

    def get_path(self,curr_pos):
        x,y=curr_pos
        x=x+100
        y=450-(-0.002569*pow(x,2)+3.114*x-543.5)
        return (x,y)


class Plasma(GameObject):
    def __init__(self,screen,position):
        super().__init__(screen)
        self.position=position
        self.img=load_image('plasma.png')

    def draw(self,set_draw,frame_count):
        if set_draw and 2<frame_count:
            self.img.set_colorkey((0,0,0))
            self.screen.blit(self.img,self.position)
            self.position=(self.position[0]-90,self.position[1])

class Laser(GameObject):
    def __init__(self, screen,position):
        super().__init__(screen)
        self.position=position

    def draw(self,set_draw,frame_count):
        if set_draw and 2<frame_count<9:
            img=self.laser_animation[frame_count-3]
            size=img.get_rect()
            self.screen.blit(img,(self.position[0]-size[2],self.position[1]))

        
    
