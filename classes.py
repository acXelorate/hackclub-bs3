from consts import *
from text import *

class Unit:
    def __init__(self,rect:pg.Rect,side,stats):
        """Side is -1 (good) and 1 (evil)"""
        self.stats=stats
        s=stats
        self.Rect=rect
        self.side=side
        
        self.sprite=s["sprite"]
        self.range=s["range"]
        self.mspeed=s["mspeed"]*self.side
        self.aspeed=s["aspeed"]
        self.dmg=s["dmg"]
        self.hp=s["hp"]
        self.kb=s["kb"]
        self.p=s["p"]
        
        p=self.p
        
        if "pierce" not in p:
            self.pierce=1
        else:
            self.pierce=p["pierce"]
            
        if "x" not in p:
            self.xOffset=0
        else:
            self.xOffset=p["x"]
            
        if "fps" not in p:
            self.fps=5
        else:
            self.fps=p["fps"]
        
        self.atick=0
        self.state=0 #0 is move, 1 is charge, 2 is attack, 3 is kb
        self.animtick=0
        self.animframe=0
        
        self.animmoveclamp=[0,2] if "animmoveclamp" not in self.p else self.p["animmoveclamp"]
        self.animchargeclamp=[3,3]if "animchargeclamp" not in self.p else self.p["animchargeclamp"]
        self.animattackclamp=[4,4]if "animattackclamp" not in self.p else self.p["animattackclamp"]
        
        
        self.cash=50
        
        if self.side==1:
            new=[]
            for sprite in self.sprite:
                new.append(pg.transform.flip(sprite,1,0))
                
            self.sprite=new
        
    def draw(self):
        #pgp.draw.rect(window,cam,self.sprite,self.Rect,gui=False)
        if self.animtick==60//self.fps:
            self.animtick=0
            if self.state==0:
                self.animframe+=1
                if not self.animmoveclamp[0]<=self.animframe<=self.animmoveclamp[1]:
                    self.animframe=self.animmoveclamp[0]
                
            if self.state==1:
                self.animframe+=1
                if not self.animchargeclamp[0]<=self.animframe<=self.animchargeclamp[1]:
                    self.animframe=self.animchargeclamp[0]
                    
            if self.state==2:
                self.animframe+=1
                if not self.animattackclamp[0]<=self.animframe<=self.animattackclamp[1]:
                    if self.animframe>self.animattackclamp[1]:
                        self.state=0
                        self.animtick=0
                        self.animframe=self.animattackclamp[0]
                    self.animframe=self.animattackclamp[0]
                    
        else: self.animtick+=1
        
        drawrect=self.sprite[0].get_rect(centerx=self.Rect.centerx,y=self.Rect.y)
        drawrect.x-=self.xOffset/2*self.side
        #pgp.draw.rect(window,cam,"black",self.Rect,5)
        pgp.blit(window,cam,self.sprite[self.animframe],drawrect,gui=False)
        
        rangerect=pg.Rect(0,self.Rect.y,self.range,5)
        rangerect.centerx=self.Rect.centerx
        rangerect.x+=self.side*self.Rect.w//2
        rangerect.x-=self.side*self.xOffset//2
        #pgp.draw.rect(window,cam,"red",rangerect)
        
    def move(self):
        if self.state==0:
            self.Rect.x+=self.mspeed
    
    def attack(self,enemy,towerRect,towerHp):
        enemy=enemy.copy()
        enemy.sort(key=lambda unit: unit.Rect.x)
        if self.side==-1:
            enemy.reverse()
        enemyrects=[i.Rect for i in enemy]
        rangerect=pg.Rect(0,self.Rect.y,self.range,5)
        rangerect.centerx=self.Rect.centerx
        rangerect.x+=self.side*self.Rect.w//2
        rangerect.x-=self.side*self.xOffset//2
        
        if self.state == 0:
            
            
            collision=rangerect.collidelist(enemyrects)
            
            if collision!=-1 or rangerect.colliderect(towerRect):
                self.state=1
            
                
        elif self.state==1:
            if self.atick==self.aspeed:
                self.atick=0
                self.state=2
                self.animtick=0
                self.animframe=self.animattackclamp[0]
                hits=self.pierce
                gothit=0 
                for i,rect in enumerate(enemyrects):
                    if rangerect.colliderect(rect):
                        enemy[i].hp-=self.dmg
                        
                        hits-=1
                        gothit+=1
                        if hits==0:
                            break
                        
                if hits!=0:
                    if rangerect.colliderect(towerRect):
                        towerHp-=self.dmg
                        gothit=0
                        random.seed()
                        random.choice(tHitSfx).play()
                        
                if gothit>0:
                    random.seed()
                    random.choice(hitSfx).play()
                
            else:
                self.atick+=1
        
        return towerHp
        
        #elif self.state==2: #TODO
            
            
    def die(self,army:list,mon):
        if self.hp<=0:
            army.remove(self)
            mon+=self.cash
        return mon
        
    def step(self,army,enemy,towerRect,towerHp,mon):
        """Returns tower hp,mon"""
        hp=self.attack(enemy,towerRect,towerHp)
        self.move()
        self.draw()
        self.die(army,mon)
        return hp,mon