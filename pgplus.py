import pygame as pg
pg.font.init()

"""Version 1.0"""

def init():
    global font,surface,consts
    
    font=pg.font.Font(None,20)
    surface=None

    class consts:
        asciivalues=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','-','_']
    
class camera:
    def __init__(self,wh,wantedwh):
        self.wh=wh
        self.wantedwh=wantedwh
        self.x=0
        self.y=0
        self.scale=(wh[0]/wantedwh[0],wh[1]/wantedwh[1])
    def get_camrect(self):
        return pg.Rect(self.x,self.y,self.x+self.wh[0],self.y+self.wh[1])
    def goto(self,pos):
        self.x=pos[0]
        self.y=pos[1]
    def move(self,pos):
        self.x+=pos[0]
        self.y+=pos[1]

def blit(surf1:pg.Surface,cam,surf2:pg.Surface,x:int|pg.Rect,y=None,gui=True):
    """x can be rect or just int - but if x is int must fill out y"""
    if type(x) is pg.Rect:
        y=x.y
        x=x.x
    w,h=surf2.get_size()
    w*=cam.scale[0]
    h*=cam.scale[1]
    surf2=pg.transform.scale(surf2,(w,h))

    x,y=point.get_smart_point([x,y],cam,gui)

    surf1.blit(surf2,(x,y))

class draw:
    @staticmethod
    def rect(surf,cam,color,_rect:pg.Rect,w=0,gui=True,border_radius=-1):
        global rect
        _rect=_rect.copy()
        _rect=rect.get_smart_rect(_rect.copy(),cam,gui).copy()
        pg.draw.rect(surf,color,_rect,w,border_radius)

    @staticmethod
    def TextBox(surf,cam,textbox,gui=True,border_radius=-1):
        draw.rect(surf,cam,textbox.bgColor,textbox.Rect,gui=gui,border_radius=border_radius)
        renderedfont=textbox.font.render(textbox.text,True,textbox.textColor)
        if not renderedfont.get_size()[0]>textbox.Rect.w:
            blit(surf,cam,renderedfont,textbox.Rect,gui=gui)
        else:
            size=textbox.font.get_height()
            while renderedfont.get_size()[0]>textbox.Rect.w:
                size-=1
                font=pg.font.Font(textbox.fontname,size) if textbox.fonttype=="Font" else pg.font.SysFont(textbox.fontname,size)
                renderedfont=font.render(textbox.text,True,textbox.textColor)
            blit(surf,cam,renderedfont,textbox.Rect,gui=gui)

class point:
    @staticmethod
    def get_smart_point(point:list,cam,gui=True):
        point=point.copy()
        if gui==False:
            point[0]-=cam.x
            point[1]-=cam.y

        point[0]*=cam.scale[0]
        point[1]*=cam.scale[1]
        return point
    @staticmethod
    def get_smart_point2(x,y,cam,gui=True):
        """Only used for mousex and mousey"""
        
        if gui==False:
            x-=cam.x
            y-=cam.y

        x*=1/cam.scale[0]
        y*=1/cam.scale[1]
        return [x,y]

class rect:
    @staticmethod
    def get_smart_rect(_rect,cam,gui=True):
        """Tool"""
        _rect=_rect.copy()
        if gui==False:
            _rect.x-=cam.x
            _rect.y-=cam.y

        _rect.x*=cam.scale[0]
        _rect.y*=cam.scale[1]
        _rect.w*=cam.scale[0]
        _rect.h*=cam.scale[1]
        return _rect
    @staticmethod
    def collidepoint(cam,_rect:pg.Rect,x,y,gui=True):
        """Rect turns smart not point"""
        _rect=rect.get_smart_rect(_rect,cam,gui)
        return _rect.collidepoint(x,y)

    @staticmethod
    def colliderect1(cam,rect1,rect2):
        """Rect 1 gets smart - if you want 2 smart just use Rect.colliderect"""
        rect1=rect.get_smart_rect(rect1,cam,False)
        if rect1.colliderect(rect2):
            return True
        return False

    @staticmethod
    def collidelistpoint(cam,rectlist,x,y):
        """All rects become smart"""
        smartlist=[]
        for _rect in rectlist:
            smartlist.append(rect.get_smart_rect(_rect,cam,False))
        for i,smart in enumerate(smartlist):
            if rect.collidepoint(cam,smart,x,y,False):
                return i
        return -1

    @staticmethod
    def collidelistpoint2(rectlist,x,y):
        """#pgQOL just collidepoint but for more rects"""
        for i,rect in enumerate(rectlist):
            if rect.collidepoint(x,y):
                return i
        return -1



class advanced:
    @staticmethod
    class TextBox:
        def __init__(self,rect:pg.Rect,bgColor="white",textColor="black",font=pg.font.Font(None,50),fonttype="Font",fontname=None):
            """fonttype is either Font or Sysfont"""
            self.Rect=rect
            self.bgColor=bgColor
            self.textColor=textColor
            self.font=font
            self.fonttype=fonttype
            self.fontname=fontname

            self.text=""

        def step(self,events,drawSelf=True,surf=None,cam=None):
            """If drawSelf is True, must fill out surf,cam | Returns if pressed key return/kp_enter"""
            b=0
            for event in events:
                if event.type==pg.KEYDOWN:
                    
                    
                    if event.key==pg.K_BACKSPACE:
                        self.text=self.text[:-1]
                    elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                        b=1

                    elif event.unicode.lower() in consts.asciivalues: self.text+=event.unicode

            if drawSelf:
                draw.TextBox(surf,cam,self)
            
            return b
            

        def getText(self):
            return self.text

class experimental:
    @staticmethod
    def setsurf(surf):
        global surface
        surface=surf
    @staticmethod
    def quickblit(text,pos:list=None):
        if pos is None:
            pos=[0,0]
        
        surface.blit(font.render(text,True,"white"),pos)

class pyplus:
    @staticmethod
    def roundint(n,divisable):
        """for example if n=103 and divisable=100 n will become 100 (424,200->400,...)"""
        return (n//divisable)*divisable

