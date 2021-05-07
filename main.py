import sys
from random import randint
import pygame
from utils import load_image,SpriteSheet,load_sound
from models import GameObject,Dragon,Female,Fireball,Plasma,Laser

class MAINGAME:
    WIN_W,WIN_H=1080,480
    def __init__(self):
        pygame.init()
        self.canvas=pygame.Surface((self.WIN_W,self.WIN_H))
        self.window=pygame.display.set_caption('Dragon v/s Fe-Male')
        self.window=pygame.display.set_mode((self.WIN_W,self.WIN_H))
        self.background=load_image('space.jpg')
        self.end_message=SpriteSheet('healthend.png')
        GameObject(self.window)
        self.ishurt_dragon=False
        self.dr_blood=1
        self.fe_blood=1

    def game_loop(self):
        count=0
        self.laser_count=1
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                    sys.exit()
            if self.dr_blood != 15 and self.fe_blood != 15:
                self.game_logic()
                self.dragon_action()
                self.render_backgroud()
            else:
                if count == 0:
                    self.epilogue()
                    count+=1

    def epilogue(self):
        if self.dr_blood >= 15:
            self.dragon.choose_action('dead')
            stand=SpriteSheet('fe_stand.png')
            fe_img=stand.parse_sprite('fe-stand1.png')
            closure=self.end_message.parse_sprite('title4.png')
            load_sound('you_win.wav')
            pygame.mixer.music.play()
        else:
            load_sound('dr_wins.wav')
            pygame.mixer.music.play()
            dead=SpriteSheet('fe_hurt.png')
            fe_img=dead.parse_sprite('fe-hurt4.png')
            self.dragon.choose_action('stand')
            closure=self.end_message.parse_sprite('title3.png')
        for i in range(1,6):
            self.window.blit(self.background, (0,0))
            self.window.blit(fe_img,(900,280))
            self.dragon.draw(i-1)
            self.window.blit(closure, (150,50))
            pygame.display.update()
            pygame.time.delay(150)
            

    def game_logic(self):
        self.female=Female(self.window)
        self.female.choose_action('stand')
        self.load_plasma=False
        self.load_laser=False
        for _ in range(100):
            key_pressed=pygame.key.get_pressed()            
            if key_pressed[pygame.K_SPACE]:
                self.load_plasma=True
                self.female.choose_action('attack')
            elif key_pressed[pygame.K_RETURN]:
                if self.laser_count < 4:
                    self.load_laser=True
                    self.female.choose_action('attack2')
                else:
                    self.load_plasma=True
                    self.female.choose_action('attack')

    def dragon_action(self):
        num=randint(1, 100)
        self.dragon=Dragon(self.window)
        self.load_fireball=False
        if self.ishurt_dragon or (num >= 50 or num<=25):
            self.dragon.choose_action('stand')
        elif 25<num<50 :    
            self.dragon.choose_action('attack')
            self.load_fireball=True


    def render_backgroud(self):
        self.fireball=Fireball(self.window,(270,200))
        self.plasma=Plasma(self.window,(870,300))
        self.laser=Laser(self.window, (935,305))
        frame_count=0
        self.ishurt_dragon=False
        if self.load_fireball:
            load_sound('dr_attack.wav')
            pygame.mixer.music.play()
        elif self.load_laser:
            self.laser_count+=1
            load_sound('fe_laser.wav')
            pygame.mixer.music.play()
        elif self.load_plasma:
            load_sound('fe_attack.wav')
            pygame.mixer.music.play()
        while True:
            self.canvas.blit(self.background,(0,0))
            self.window.blit(self.canvas,(0,0))
            self.dragon.draw(frame_count)
            self.dragon.get_score(self.dr_blood)
            self.female.draw(frame_count)            
            self.female.get_score(self.fe_blood)
            self.fireball.draw(self.load_fireball,frame_count)
            self.plasma.draw(self.load_plasma,frame_count)
            self.laser.draw(self.load_laser, frame_count)
            pygame.display.update()
            if (self.load_plasma or self.load_fireball or self.load_laser) and frame_count == 9:
                if self.load_plasma or self.load_laser:
                    load_sound('dr_hurt.wav')
                    pygame.mixer.music.play()
                    self.ishurt_dragon=True
                    self.dragon.choose_action('hurt')
                    if self.load_laser:
                        self.dr_blood+=2
                    else:
                        self.dr_blood+=1
                else:
                    self.dragon.choose_action('stand')
                if self.load_fireball:
                    load_sound('fe_hurt.wav')
                    pygame.mixer.music.play()
                    self.female.choose_action('hurt')
                    self.fe_blood+=2
                else:
                    self.female.choose_action('stand')
                frame_count=0
                if self.dr_blood >= 15 or self.fe_blood >= 15:
                    break
                while True:
                    self.canvas.blit(self.background,(0,0))
                    self.window.blit(self.canvas,(0,0))
                    self.dragon.draw(frame_count)
                    self.dragon.get_score(self.dr_blood)
                    self.female.draw(frame_count)
                    self.female.get_score(self.fe_blood)
                    pygame.display.update()
                    pygame.time.delay(100)
                    if frame_count == 9:
                        break
                    frame_count+=1            
            if frame_count == 9:
                break
            frame_count+=1
            pygame.time.delay(100)

    




        

    