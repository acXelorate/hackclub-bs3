import pygame as pg
pg.font.init()

"""Version 1.0.1 - bs3 release"""

def init():
    global webbrowser
    import webbrowser
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
            
    @staticmethod
    def polygon(surf,cam,color,points,w=0,gui=True):
        points=[point.get_smart_point(i,cam,gui) for i in points]
        pg.draw.polygon(surf,color,points,w)
        
    @staticmethod
    def line(surf,cam,color,startpos,endpos,w=1,gui=True):
        startpos=point.get_smart_point(startpos,cam,gui)
        endpos=point.get_smart_point(endpos,cam,gui)
        pg.draw.line(surf,color,startpos,endpos,w)
        
    @staticmethod
    def button(surf,cam,button,gui=True):
        _rect=button.Rect.copy()
        if button.fontType=="Font":
            font=pg.font.Font(button.fontName,button.fontSize)
        else:
            font=pg.font.SysFont(button.fontName,button.fontSize)
        if button.hoverEffect=="popup":
            center=_rect.center
            _rect.w*=button.scale
            _rect.h*=button.scale
            _rect.center=center
            if button.fontType=="Font":
                font=pg.font.Font(button.fontName,int(button.fontSize*button.scale))
            else:
                font=pg.font.SysFont(button.fontName,int(button.fontSize*button.scale))
                
        draw.rect(surf,cam,button.bgColor,_rect,gui=gui,border_radius=button.borderRadius)
        draw.rect(surf,cam,button.lineColor,_rect,5,gui=gui,border_radius=button.borderRadius)
        center=_rect.center
        txt=font.render(button.text,True,button.textColor)
        r=txt.get_rect(center=center)
        blit(surf,cam,txt,r,gui=gui)

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
        if type(_rect)!=pg.Rect:
            _rect=pg.Rect(*_rect)
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
        
    @staticmethod
    class Button:
        def __init__(self,rect,text:str,function,bgColor="white",lineColor="black",textColor="black",fontType="Font",fontName=None,fontSize=50,hoverEffect=None,borderRadius=-1,flags:dict={}):
            """fonttype is either Font or Sysfont, hovereffect: None, popup"""
            self.Rect=rect
            self.text=text
            self.function=function
            self.bgColor=bgColor
            self.lineColor=lineColor
            self.textColor=textColor
            self.fontType=fontType
            self.fontName=fontName
            self.fontSize=fontSize
            self.hoverEffect=hoverEffect
            self.borderRadius=borderRadius
            self.flags=flags
            
            self.hovering=False
            
            if self.hoverEffect=="popup":
                self.scale=1.0
                
            if "hoverSfx" in self.flags.keys():
                self.hoverSfx=pg.mixer.Sound(self.flags["hoverSfx"])
                
            if "clickSfx" in self.flags.keys():
                self.clickSfx=pg.mixer.Sound(self.flags["clickSfx"])
                
        def runFunction(self):
            if "functionParameters" in self.flags:
                self.function(*self.flags["functionParameters"])
            else: self.function()
            
            if "clickSfx" in self.flags.keys():
                self.clickSfx.play()
                
            self.hovering=False

            if self.hoverEffect=="popup":
                self.scale=1.0
            
        def step(self,surf,cam,mousex,mousey,leftclick,events=None,gui=True):
            """events should be filled if key in flags"""
            run=0
            if rect.collidepoint(cam,self.Rect,mousex,mousey):
                if "hoverSfx" in self.flags.keys():
                    if self.hovering==False:
                        self.hoverSfx.play()
                self.hovering=True
                
                if leftclick:
                    self.runFunction()
                    run=1
            else:
                self.hovering=False
                
            if "key" in self.flags:
                if run==0:
                    for event in events:
                        if event.type==pg.KEYDOWN:
                            if event.key==self.flags["key"]:
                                self.runFunction()
            
            if self.hovering==False:
                if self.hoverEffect=="popup":
                    if self.scale>1.0:
                        self.scale-=0.02
            else:
                if self.hoverEffect=="popup":
                    if self.scale<1.1:
                        self.scale+=0.02
            
            draw.button(surf,cam,self,gui)
            
    @staticmethod
    class Popup:
        def __init__(self,rect:pg.Rect,text:pg.Surface,bgColor="white",lineColor="black",textColor="black",buttons=[],borderRadius=-1,flags:dict={}):
            """Button rects are relative to the popup"""
            self.Rect=rect
            
            self.text=text
            self.rtext=self.text.get_rect(centerx=self.Rect.centerx,y=self.Rect.y+10)
            
            self.bgColor=bgColor
            self.lineColor=lineColor
            self.textColor=textColor
            self.borderRadius=borderRadius
            self.flags=flags
            
            self.buttons=buttons
            for button in self.buttons:
                button.Rect.x+=self.Rect.x
                button.Rect.y+=self.Rect.y
                
            if "closeButton" in self.flags.keys():
                rect=pg.Rect(0,self.Rect.y,100,100)
                rect.right=self.Rect.w
                rect.x+=self.Rect.x
                print(rect)
                self.buttons.append(advanced.Button(rect,"X",self.flags["closeButton"],"red",textColor="white",fontSize=100,borderRadius=self.borderRadius))
                
        def draw(self,surf,cam,gui=True):
            draw.rect(surf,cam,self.bgColor,self.Rect,gui=gui,border_radius=self.borderRadius)
            draw.rect(surf,cam,self.lineColor,self.Rect,gui=gui,border_radius=self.borderRadius,w=5)
            
            blit(surf,cam,self.text,self.rtext,gui=gui)
                
        def step(self,surf,cam,mousex,mousey,leftclick,events=None,gui=True):
            self.draw(surf,cam,gui)
            
            for button in self.buttons:
                button.step(surf,cam,mousex,mousey,leftclick,events,gui)
                
    def openLink(url, customLink=False, new=0, autoraise=True):
        """Display url using the default browser.
        
        customLink checks if you need https://
        
        If possible, open url in a location determined by new.
        - 0: the same browser window (the default).
        - 1: a new browser window.
        - 2: a new browser page ("tab").
        If possible, autoraise raises the window (the default) or not.
        """
        if not customLink: url=f"https://{url}"
        webbrowser.open(url,new,autoraise)
                
    @staticmethod
    class Link:
        def __init__(self,text:str,pos:list|pg.Rect,link,font:pg.font.Font,textColor,bgColor,hoverTextColor,borderRadius=-1,customLink=False,autoraise=True):
            """If customLink==True, then you must include https:// and www. else link should be just website.com , autoraise checks if the browser should automatically focus once link gets opened (windows only)"""
            self.text=text
            
            
            if not customLink: self.link=f"https://{link}"
            else: self.link=link
            
            self.font=font
            self.textColor=textColor
            self.bgColor=bgColor
            self.hoverTextColor=hoverTextColor
            
            self.borderRadius=borderRadius
            self.autoraise=autoraise
            
            self.txt=font.render(text,True,textColor)
            self.hoverTxt=font.render(text,True,hoverTextColor)
            
            if type(pos)==list:
                self.Rect=self.txt.get_rect(topleft=pos)
                
            else:
                self.Rect=pos
                
        def draw(self,surf,cam,hovering,gui=True):
            if hovering:
                draw.rect(surf,cam,self.bgColor,self.Rect,gui=gui,border_radius=self.borderRadius)
                blit(surf,cam,self.hoverTxt,self.Rect,gui=gui)
            else:
                blit(surf,cam,self.txt,self.Rect,gui=gui)
            
        def step(self,surf,cam,mousex,mousey,leftclick,gui=True):
            hovering=False
            
            if rect.collidepoint(cam,self.Rect,mousex,mousey,gui):
                hovering=True
                
                if leftclick:
                    webbrowser.open(self.link,autoraise=self.autoraise)
            
            self.draw(surf,cam,hovering,gui)
            
class text:
    @staticmethod
    def blit2color(surf:pg.Surface,cam:camera,col1,col2,font:pg.font.Font,font2:pg.font.Font,text:str,pos:list,gui:bool=True):
        """Blits text with shadow another color"""
        if type(pos)==pg.Rect:
            pos=[pos.x,pos.y]
        txt=font.render(text,True,col1)
        txt2=font2.render(text,True,col2)
        r1=txt.get_rect(x=pos[0],y=pos[1])
        r2=txt2.get_rect(center=r1.center)
        blit(surf,cam,txt2,r2,gui=gui)
        blit(surf,cam,txt,r1,gui=gui)
        
class Surface:
    @staticmethod
    def mergeSurface(*surfaces,center=True):
        """Returns New Surface with old surfaces stacked beneath each other, center is if the surfaces will be centered to the biggest surface"""
        width=0
        height=0
        for surf in surfaces:
            w,h=surf.get_size()
            if w>width:
                width=w
            height+=h
        
        surface=pg.Surface((width,height),pg.SRCALPHA)
        y=0
        for surf in surfaces:
            rect=surf.get_rect(y=y)
            if center==True:
                rect.centerx=width//2
            surface.blit(surf,rect)
            y+=surf.get_size()[1]

        return surface

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

    @staticmethod
    def getState(n):
        """Returns 1 if n>=0 and -1 if n<0"""
        return 1 if n>=0 else -1
    
    @staticmethod
    def fileExists(path):
        try:
            with open(path) as f:
                return True
        except FileNotFoundError: return False