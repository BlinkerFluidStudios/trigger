import json, pygame, sys, math, colorsys

console = "Delta1"
version = "Delta v0.01 (unstable)"

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def truncate(number, digits) -> int:
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

menu = 1
FPS = 60

def init(trash):
    global dmxOutputBuffer
    global parkedChans
    global fixes
    global ocupdChans
    global layoutbuttons
    global canPatch
    global selectedFix
    global patchSelectedFix
    global fixpage
    global playbacks
    global playPage
    dmxOutputBuffer = {}
    parkedChans=[]
    fixes = []
    ocupdChans = []
    layoutbuttons = []
    canPatch = True
    selectedFix = []
    patchSelectedFix = None
    fixpage = 0
    playbacks = []

fixselbuttons = []
pagebuttons = []
fixpage = 0
fixselbuttons = []
playPage = 0
input_boxes = []

init(None)

newfixtype = "RGBW LED PAR"
newfixchans = []

def getListOfKeys(dict):
    return list(dict.keys())

class fixture():
    def __init__(self, Name, Type, StartChannel):
        self.Name = Name
        self.Type = Type
        self.startChan = StartChannel
        self.intens = 100
        self.x = 400
        self.y = 200
        self.layoutbutton = layoutbutton(self)
        self.outr = 0
        self.outg = 0
        self.outb = 0
        self.outw = 0
        self.r = 0
        self.g = 0
        self.b = 0
        self.w = 0
        self.cereal = None
        match self.Type:
            case "RGBW LED PAR":
                self.r = 0
                self.g = 0
                self.b = 0
                self.w = 0
                self.chans = [self.outr, self.outg, self.outb, self.outw]
                self.playbackParams = [self.r,self.g,self.b,self.intens]
                self.chansUsed = [int(StartChannel), int(StartChannel)+1, int(StartChannel)+2, int(StartChannel)+3]
                self.dmxsize = 4
                dmxOutputBuffer[int(StartChannel)]=self.r
                dmxOutputBuffer[int(StartChannel)+1]=self.g
                dmxOutputBuffer[int(StartChannel)+2]=self.b
                dmxOutputBuffer[int(StartChannel)+3]=self.w
            case "Generic Dimmer":
                self.chans = [self.intens]
                self.playbackParams = [self.intens]
                self.dmxsize = 1
                dmxOutputBuffer[int(StartChannel)]=self.intens
                self.chansUsed = [int(StartChannel)]
                self.gelR = 1
                self.gelB = 1
                self.gelG = 1
    def intensCalc(self):
        if self.Type == "RGBW LED PAR":
            self.outr = (self.r*self.intens/100)
            self.outg = (self.g*self.intens/100)
            self.outb = (self.b*self.intens/100)
            self.outw = (self.w*self.intens/100)
            self.playbackParams = [self.r,self.g,self.b,self.intens]
        elif self.Type == "Generic Dimmer":
            self.playbackParams = [self.intens]
    def makeCereal(self):
        self.cereal = [self.Name, self.Type, self.r,self.g,self.b,self.w,self.intens,self.startChan,self.x,self.y]

class playback():
    def __init__(self, Name):
        self.data = {}
        self.name = Name
        playbacks.append(self)

    def record(self):
        for fix in fixes:
            if fix.Type == "RGBW LED PAR":
                self.data[fix] = [fix.r,fix.g,fix.b,fix.intens]
            elif fix.Type == "Generic Dimmer":
                self.data[fix] = [fix.intens]

    def play(self):
        for fix in fixes:
                if fix.Type == "RGBW LED PAR":
                    fixData = self.data[fix]
                    if fixData[0] > 0:
                        fix.r = fixData[0]
                    if fixData[1] > 0:
                        fix.g = fixData[1]
                    if fixData[2] > 0:
                        fix.b = fixData[2]
                    if fixData[3] > 0:
                        fix.intens = fixData[3]
                    fix.intensCalc()
                if fix.Type == "Generic Dimmer":
                    fixData = self.data[fix]
                    if fixData[0] > 0:
                        fix.intens = fixData[0]
                    fix.intensCalc()

def save(trash):
    global fixes
    global dmxOutputBuffer
    fixdict = {}
    x = open("save.dat", "r+")
    x.seek(0)
    x.truncate()
    for fix in fixes:
        fix.makeCereal()
    with open('save.dat', 'w') as f:
        for index, fix in enumerate(fixes):
            fixdict[index] = fix.cereal
        data = json.dumps(fixdict)
        f.write(data)
            
def load(trash):
    init(None)
    x = open("save.dat","r")
    contents = x.read()
    fixdict = json.loads(contents)
    for x in fixdict.values():
        x = list(x)
        myfix = fixture(x[0],x[1],int(x[7]))
        myfix.r = x[2]
        myfix.g = x[3]
        myfix.b = x[4]
        myfix.intens = x[6]
        myfix.x = x[8]
        myfix.y = x[9]
        myfix.intensCalc()
        fixes.append(myfix)


pygame.init() 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
mouse = (0,0)
mouseDown = False
shift = False
colorpickerImg = pygame.image.load("5d107b5ed8fdb8964fbad44174bc9b18.png")
font = pygame.font.Font('Roboto-Regular.ttf', 32)
smallfont = pygame.font.Font('Roboto-Medium.ttf', 12)
screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()     ## For syncing the FPS

w, h = pygame.display.get_surface().get_size()
layoutviewtext = font.render("Layout View", True, WHITE)
patchTexts = [smallfont.render("DMX Start Address (letters unsupported)", True, WHITE),smallfont.render("Fixture Name", True, WHITE),smallfont.render("Fixture Type", True, WHITE)]

def setPage(page):
    global menu
    menu = page
    for buttons in pagebuttons:
        buttons.update(menu)

def updatePatchView(trash=None):
    global canPatch
    global newfixchans
    newfixchans.clear()
    if newfixtype == "RGBW LED PAR":
        for chans in range(4):
            if int(startChan.text)+3 > 512:
                canPatch = False
            else:
                canPatch = True
            newfixchans.append(int(startChan.text)+chans)
    elif newfixtype == "Generic Dimmer":
            if int(startChan.text) > 512:
                canPatch = False
            else:
                canPatch = True
            newfixchans.append(int(startChan.text))

def setNewFix(fix):
    global newfixtype
    newfixtype = fix
    updatePatchView()
    for buttons in fixselbuttons:
        buttons.update(newfixtype)

class pagebutton():
    def __init__(self,x,y,w,h,text,lightColor,darkColor,selColor,borderradius,latch,page):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = font.render(str(text), True, WHITE)
        self.lightCol = lightColor
        self.darkCol = darkColor
        self.selColor = selColor
        self.latch = latch
        self.border = borderradius
        self.val = False
        self.mypage = page
        pagebuttons.append(self)
    
    def draw(self):
        if self.x <= mouse[0] <= self.x+self.w and self.y <= mouse[1] <= self.y+self.h and mouseDown:
            pygame.draw.rect(screen,self.selColor,[self.x,self.y,self.w,self.h],border_radius=self.border)
            self.val = True
            setPage(self.mypage)
            if not self.latch:
                if mouseDown == False and self.val:
                    self.val = False
        elif self.latch and self.val:
            pygame.draw.rect(screen,self.selColor,[self.x,self.y,self.w,self.h],border_radius=self.border)
        elif self.x <= mouse[0] <= self.x+self.w and self.y <= mouse[1] <= self.y+self.h:
            pygame.draw.rect(screen,self.lightCol,[self.x,self.y,self.w,self.h],border_radius=self.border)
        else:
            pygame.draw.rect(screen,self.darkCol,[self.x,self.y,self.w,self.h],border_radius=self.border)
        screen.blit(self.text, [self.x+10,self.y+10,self.w,self.h])

    def update(self, page):
        if page != self.mypage:
            self.val = False

class fixselectbutton():
    def __init__(self,x,y,w,h,text,lightColor,darkColor,selColor,borderradius,fix):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = font.render(str(text), True, WHITE)
        self.lightCol = lightColor
        self.darkCol = darkColor
        self.selColor = selColor
        self.latch = True
        self.border = borderradius
        self.val = False
        self.myfix = fix
        fixselbuttons.append(self)
    
    def draw(self):
        if self.x <= mouse[0] <= self.x+self.w and self.y <= mouse[1] <= self.y+self.h and mouseDown:
            pygame.draw.rect(screen,self.selColor,[self.x,self.y,self.w,self.h],border_radius=self.border)
            self.val = True
            setNewFix(self.myfix)
            if not self.latch:
                if mouseDown == False and self.val:
                    self.val = False
        elif self.latch and self.val:
            pygame.draw.rect(screen,self.selColor,[self.x,self.y,self.w,self.h],border_radius=self.border)
        elif self.x <= mouse[0] <= self.x+self.w and self.y <= mouse[1] <= self.y+self.h:
            pygame.draw.rect(screen,self.lightCol,[self.x,self.y,self.w,self.h],border_radius=self.border)
        else:
            pygame.draw.rect(screen,self.darkCol,[self.x,self.y,self.w,self.h],border_radius=self.border)
        screen.blit(self.text, [self.x+10,self.y+6,self.w,self.h])

    def update(self, fix):
        if fix != self.myfix:
            self.val = False

class InputBox:
    def __init__(self, x, y, w, h, text='',callback = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (40,40,40)
        self.text = text
        self.txt_surface = font.render(text, True, (255,255,255))
        self.active = False
        self.callback = callback
        input_boxes.append(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (100,100,200) if self.active else (40,40,40)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    try:
                        self.callback(self.text)
                    except:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, (255,255,255))

    def draw(self, screen):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)

class button():
    def __init__(self,x,y,w,h,text,lightColor,darkColor,selColor,borderradius,callback,args=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = font.render(str(text), True, WHITE)
        self.lightCol = lightColor
        self.darkCol = darkColor
        self.selColor = selColor
        self.border = borderradius
        self.args = args
        self.callback = callback
        self.calledback = False
    
    def draw(self):
        if self.x <= mouse[0] <= self.x+self.w and self.y <= mouse[1] <= self.y+self.h and mouseDown:
            pygame.draw.rect(screen,self.selColor,[self.x,self.y,self.w,self.h],border_radius=self.border)
            if self.calledback == False:
                self.calledback = True
                self.callback(self.args)
        elif self.x <= mouse[0] <= self.x+self.w and self.y <= mouse[1] <= self.y+self.h:
            pygame.draw.rect(screen,self.lightCol,[self.x,self.y,self.w,self.h],border_radius=self.border)
            self.calledback = False
        else:
            pygame.draw.rect(screen,self.darkCol,[self.x,self.y,self.w,self.h],border_radius=self.border)
        screen.blit(self.text, [self.x+10,self.y+6,self.w,self.h])

class layoutbutton():
    global fixes
    def __init__(self,fix):
        self.x = fix.x
        self.y = fix.y
        self.w = 30
        self.h = 30
        self.r = 0
        self.g = 0
        self.b = 0
        self.fix = fix
        try:
            self.text = smallfont.render(str(fixes.index(self.fix)), True, WHITE)
        except:
            self.text = smallfont.render("X", True, RED)
        self.border = 5
        self.calledback = False
    
    def draw(self):
        global selectedFix
        try:
            self.x = self.fix.x
            self.y = self.fix.y
        except:
            pass
        if self.fix.Type == "RGBW LED PAR":
            self.r = self.fix.outr*2.55
            self.g = self.fix.outg*2.55
            self.b = self.fix.outb*2.55
        elif self.fix.Type == "Generic Dimmer":
            self.r = (self.fix.intens*2.55)*self.fix.gelR
            self.g = (self.fix.intens*2.55)*self.fix.gelG
            self.b = (self.fix.intens*2.55)*self.fix.gelB
        if (self.x+(w/2+10)) <= mouse[0] <= (self.x+(w/2+10))+self.w and self.y <= mouse[1] <= self.y+self.h and mouseDown:
            pygame.draw.rect(screen,(self.r,self.g,self.b),[self.x+(w/2+10),self.y,self.w,self.h],border_radius=self.border)

            if self.calledback == False:
                self.calledback = True
                if shift:
                    if self.fix not in selectedFix:
                        selectedFix.append(self.fix)
                        Intensity.text = str(self.fix.intens)
                        Intensity.txt_surface = font.render(str(self.fix.intens), True, (255,255,255))
                else:
                    selectedFix.clear()
                    selectedFix.append(self.fix)
                    Intensity.text = str(self.fix.intens)
                    Intensity.txt_surface = font.render(str(self.fix.intens), True, (255,255,255))
                if self.fix.Type == "RGBW LED PAR":
                    Red.text = str(self.fix.r)
                    Red.txt_surface = font.render(str(self.fix.r), True, WHITE)
                    Green.text = str(self.fix.g)
                    Green.txt_surface = font.render(str(self.fix.g), True, WHITE)
                    Blue.text = str(self.fix.b)
                    Blue.txt_surface = font.render(str(self.fix.b), True, (255,255,255))
        elif (self.x+(w/2+10)) <= mouse[0] <= (self.x+(w/2+10))+self.w and self.y <= mouse[1] <= self.y+self.h:
            pygame.draw.rect(screen,(self.r,self.g,self.b),[self.x+(w/2+10),self.y,self.w,self.h],border_radius=self.border)
        else:
            pygame.draw.rect(screen,(self.r,self.g,self.b),[self.x+(w/2+10),self.y,self.w,self.h],border_radius=self.border)
            self.calledback = False
            self.added = False
        screen.blit(self.text, [self.x+10+(w/2+10),self.y+6,self.w,self.h])
        if self.fix in selectedFix:
            pygame.draw.rect(screen,(255,150,100),[self.x+(w/2+10),self.y,self.w,self.h],border_radius=self.border,width=2)
        else:
            pygame.draw.rect(screen,WHITE,[self.x+(w/2+10),self.y,self.w,self.h],border_radius=self.border,width=2)

RGBW = fixselectbutton(w-350,200, 280, 50,"RGBW PAR",(200,200,200),(80,80,80),(40,40,40),5,"RGBW LED PAR")
GenDim = fixselectbutton(w-350,255, 280, 50,"Dimmer",(200,200,200),(80,80,80),(40,40,40),5,"Generic Dimmer")
fixName = InputBox(w-350,125, 280, 50, text="Fixture Name")
startChan = InputBox(w-350,50, 280, 50, text="1",callback=updatePatchView)

def movelayoutbutton(where):
    try:
        for fix in selectedFix:
            match where:
                case "up":
                    if fix.y-10>90:
                        fix.y -= 10
                case "down":
                    if fix.y+10<h-235:
                        fix.y += 10
                case "left":
                    if (fix.x+(w/2+10))-10>(w/2+10):
                        fix.x -= 10
                case "right":
                    if (fix.x+(w/2+10))+50<((w/2+10)+(w/2-30)):
                        fix.x += 10
    except:
        pass

def renameFix(newName):
    global patchSelectedFix
    patchSelectedFix.Name = newName

fixRename = InputBox(20,125, 280, 50, text="Fixture Name", callback=renameFix)

def openFixPage(fixtureRef):
    global menu
    global patchSelectedFix
    menu = 3.2
    patchSelectedFix = fixtureRef
    fixRename.text = str(fixtureRef.Name)
    fixRename.txt_surface = font.render(str(fixtureRef.Name), True, (255,255,255))

def openPlaybackPage(fixtureRef):
    global menu
    global selectedPlayback
    menu = 2.1
    selectedPlayback = fixtureRef
    fixRename.text = str(fixtureRef.Name)
    fixRename.txt_surface = font.render(str(fixtureRef.Name), True, (255,255,255))

def setFixPage(direction):
    global fixpage
    match direction:
        case 1:
            fixpage += 1
        case -1:
            fixpage -= 1

def setPlayPage(direction):
    global playPage
    match direction:
        case 1:
            playPage += 1
        case -1:
            playPage -= 1

def deleteFix(trash):
    global patchSelectedFix
    global dmxOutputBuffer
    global fixpage
    global menu
    for chans in patchSelectedFix.chansUsed:
        del dmxOutputBuffer[chans]
    fixes.remove(patchSelectedFix)
    fixpage = 0
    menu = 3.1

def refreshFixVals():
        try:
            Red.text = str(selectedFix[0].r)
            Red.txt_surface = font.render(str(selectedFix[0].r), True, WHITE)
            Green.text = str(selectedFix[0].g)
            Green.txt_surface = font.render(str(selectedFix[0].g), True, WHITE)
            Blue.text = str(selectedFix[0].b)
            Blue.txt_surface = font.render(str(selectedFix[0].b), True, (255,255,255))
        except:
            pass

RemovePatch = button(20, 190, 250, 50,"Delete Fixture",(200,100,100),(100,50,50),(40,40,40),5,deleteFix)

def patchFix(trash):
    global selectedFix
    selectedFix = None
    newfix = fixture(fixName.text,newfixtype,startChan.text)
    fixes.append(newfix)
    startchan = int(startChan.text)
    match newfixtype:
        case "RGBW LED PAR":
            startChan.text = str(startchan + 4)
            startChan.txt_surface = font.render(str(startchan + 4), True, (255,255,255))
        case "Generic Dimmer":
            startChan.text = str(startchan + 1)
            startChan.txt_surface = font.render(str(startchan + 1), True, (255,255,255))
    updatePatchView()

MainView = pagebutton(15, h-75, 200, 50,"Programmer",(200,200,200),(50,50,50),(25,25,25),5,True,1)
Cues = pagebutton(220, h-75, 200, 50,"Playbacks",(200,200,200),(50,50,50),(25,25,25),5,True,2)
Patch = pagebutton(425,h-75, 200, 50,"Patch",(150,150,200),(50,50,100),(25,25,25),5,True,3.1)
Setup = pagebutton(630,h-75, 200, 50,"Settings",(200,200,200),(50,50,50),(25,25,25),5,True,4)
AddPatch = button(w-350,h-400, 280, 50,"Patch New Fixture",(100,200,100),(50,100,50),(40,40,40),5,patchFix)
backbutton1 = button(15, h-155, 200, 50,"< Back",(100,100,100),(15,15,15),(40,40,40),5,setPage,args=3.1)
down = button(220, h-155, 200, 50,"Page Down",(100,100,100),(15,15,15),(40,40,40),5,setFixPage,args=-1)
up = button(425, h-155, 200, 50,"Page Up",(100,100,100),(15,15,15),(40,40,40),5,setFixPage,args=1)

down1 = button(w/2+150, h-140, 100, 50,"Down",(100,100,100),(15,15,15),(40,40,40),5,movelayoutbutton,args="down")
up1 = button(w/2+150, h-195, 100, 50,"Up",(100,100,100),(15,15,15),(40,40,40),5,movelayoutbutton,args="up")
left = button(w/2+40, h-168, 100, 50,"<",(100,100,100),(15,15,15),(40,40,40),5,movelayoutbutton,args="left")
right = button(w/2+260, h-168, 100, 50,">",(100,100,100),(15,15,15),(40,40,40),5,movelayoutbutton,args="right")

down2 = button(220, h-155, 200, 50,"Page Down",(100,100,100),(15,15,15),(40,40,40),5,setPlayPage,args=-1)
up2 = button(425, h-155, 200, 50,"Page Up",(100,100,100),(15,15,15),(40,40,40),5,setPlayPage,args=1)

saveShow = button(20, 80, 280, 50,"Save Show",(100,100,100),(15,15,15),(40,40,40),5,save)
loadShow = button(20, 140, 280, 50,"Load Show",(100,100,100),(15,15,15),(40,40,40),5,load)
newShow = button(20, 200, 280, 50,"New Show",(100,100,100),(15,15,15),(40,40,40),5,init)

def recordPlayback(Name):
    myplayback = playback(Name)
    myplayback.record()
def playPlayback(trash):
    print(str(len(playbacks)))
    playbacks[0].play()

def setFixIntens(intens):
    for fix in selectedFix: 
        if intens == "":
            intens = 0
        x = clamp(int(intens),0,100)
        fix.intens = x
        fix.intensCalc()
def setFixRed(intens):
    for fix in selectedFix: 
        if intens == "":
            intens = 0
        x = clamp(int(intens),0,100)
        if fix.Type == "RGBW LED PAR":
            fix.r = x
            fix.intensCalc()
def setFixGreen(intens):
    for fix in selectedFix: 
        if intens == "":
            intens = 0
        x = clamp(int(intens),0,100)
        if fix.Type == "RGBW LED PAR":
            fix.g = x
            fix.intensCalc()
def setFixBlue(intens):
    for fix in selectedFix: 
        if intens == "":
            intens = 0
        x = clamp(int(intens),0,100)
        if fix.Type == "RGBW LED PAR":
            fix.b = x
            fix.intensCalc()

Intensity = InputBox(30,90, 280, 50,callback=setFixIntens)
Red = InputBox(30,150, 280, 50,callback=setFixRed)
Green = InputBox(30,210, 280, 50,callback=setFixGreen)
Blue = InputBox(30,270, 280, 50,callback=setFixBlue)
FixParamLabels = [font.render("Intensity", True, (255,255,255)),font.render("Red", True, (255,255,255)),font.render("Green", True, (255,255,255)),font.render("Blue", True, (255,255,255))]

mode = "view"
def setMode(newmode):
    global mode
    if mode == "edit":
        mode = "view"
        modebutton.text = font.render("Edit", True, WHITE)
    else:
        mode = "edit"
        modebutton.text = font.render("View", True, WHITE)
modebutton = button(w-172, 30, 140, 50,"Edit",(100,100,100),(15,15,15),(40,40,40),5,setMode)

setupTexts = [font.render("Console: "+str(console),True,WHITE),font.render(str(version),True,WHITE),font.render("Dangerous Stuff (don't touch during a show)",True,WHITE)]

recPlayback = button(20, 20, 280, 50,"Record Playback",(100,100,100),(15,15,15),(40,40,40),5,recordPlayback,args="turd")
plPlayback = button(20, 80, 280, 50,"Play Playback",(100,100,100),(15,15,15),(40,40,40),5,playPlayback)

running = True
while running:
    #1 Process input/event
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
        for box in input_boxes:
                box.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        shift = True
    else:
        shift = False
    if mode == "edit":
        if keys[pygame.K_UP]:
            movelayoutbutton("up")
        if keys[pygame.K_DOWN]:
            movelayoutbutton("down")
        if keys[pygame.K_LEFT]:
            movelayoutbutton("left")
        if keys[pygame.K_RIGHT]:
            movelayoutbutton("right")

    mouse = pygame.mouse.get_pos()
    screen.fill(BLACK)
    MainView.draw()
    Cues.draw()
    Patch.draw()
    Setup.draw()
    pygame.draw.rect(screen, (25,25,25), pygame.Rect(10, 10, w-20, h-75),border_radius=5)
    match menu:
        case 1:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(w/2+10, 20, w/2-30, h-95),border_radius=5)
            screen.blit(layoutviewtext, [w/2+20, 25, w/2-30, h-95])
            for fix in fixes:
                mybutton = layoutbutton(fix)
                mybutton.draw()
            if mode == "edit":
                pygame.draw.rect(screen, (5,5,5), pygame.Rect(w/2+20, h-200, w/2-50, 115),border_radius=5)
                down1.draw()
                up1.draw()
                left.draw()
                right.draw()
                screen.blit((smallfont.render("Use arrow keys to move fast.",True,WHITE)),[w/2+400, h-150, w/2-50, 115])
            modebutton.draw()
            if selectedFix != None:
                try:
                    fixNameText = font.render(str(selectedFix[0].Name), True, WHITE)
                    screen.blit(fixNameText,[30,30,100,100])
                    match selectedFix[0].Type:
                        case "Generic Dimmer":
                            Intensity.draw(screen)
                            screen.blit(FixParamLabels[0],(250,95,10,10))
                        case "RGBW LED PAR":
                            Intensity.draw(screen)
                            screen.blit(FixParamLabels[0],(250,95,10,10))
                            Red.draw(screen)
                            screen.blit(FixParamLabels[1],(250,155,10,10))
                            Green.draw(screen)
                            screen.blit(FixParamLabels[2],(250,215,10,10))
                            Blue.draw(screen)
                            screen.blit(FixParamLabels[3],(250,275,10,10))
                            screen.blit(colorpickerImg,(20,345,300,300))
                            if ((mouse[0] - 170)**2 + (mouse[1] - 495)**2 < 22500) and mouseDown:
                                radiiToMouse = math.atan2(mouse[1]-495, mouse[0]-170)
                                degsToMouseX = math.degrees(radiiToMouse)
                                degsToMouse = translate(degsToMouseX,-180,180,0,360)+90
                                distToMouse = math.dist((170,495),(mouse[0],mouse[1]))
                                color = list(colorsys.hsv_to_rgb(degsToMouse/360,distToMouse/150,1))
                                for fix in selectedFix:
                                    try:
                                        fix.r = math.floor(color[0]*100)
                                        fix.g = math.floor(color[1]*100)
                                        fix.b = math.floor(color[2]*100)
                                        fix.intensCalc()
                                        refreshFixVals()
                                    except:
                                        pass
                except:
                    pass
        case 2:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(w/2+10, 20, w/2-30, h-95),border_radius=5)
            screen.blit(layoutviewtext, [w/2+20, 25, w/2-30, h-95])
            for fix in fixes:
                mybutton = layoutbutton(fix)
                mybutton.draw()
            recPlayback.draw()
            if len(playbacks) > 4:
                if (playPage+1)*4 < len(playbacks):
                    up2.draw()
                if playPage > 0:
                    down2.draw()
                try:
                    for layer in range(4):
                        num = layer+playPage*4
                        playRef = playbacks[num]
                        mybutton = button(20,90+layer*55, 550, 50, str(num)+" "+str(playRef.name) ,(100,100,100),(15,15,15),(40,40,40),5,openPlaybackPage)
                        mybutton.draw()
                except:
                    pass
            else:
                for index,playbac in enumerate(playbacks):
                    mybutton = button(20,90+index*55, 550, 50, str(index)+" "+str(playbac.name) ,(100,100,100),(15,15,15),(40,40,40),5,openPlaybackPage)
                    mybutton.draw()

        case 3.1:
            pygame.draw.rect(screen, (15,15,15), pygame.Rect(w-360,20, 300, 450),border_radius=5)
            if canPatch:
                AddPatch.draw()
            RGBW.draw()
            GenDim.draw()
            fixName.draw(screen)
            startChan.draw(screen)
            screen.blit(patchTexts[0], [w-350,30, 280, 50])
            screen.blit(patchTexts[1], [w-350,105, 280, 50])
            screen.blit(patchTexts[2], [w-350,180, 280, 50])
            dmxKeys = getListOfKeys(dmxOutputBuffer)
            for chans in range(32):
                for layer in range(16):
                    if newfixchans.count(chans+1+layer*32) >= 1:
                        pygame.draw.rect(screen, (5,5,200), pygame.Rect(chans*27+15,layer*25+18, 27,25))
                    if dmxKeys.count(chans+1+layer*32) >= 1:
                        pygame.draw.rect(screen, (5,200,200), pygame.Rect(chans*27+15,layer*25+18, 27,25))
                    if dmxKeys.count(chans+1+layer*32) >= 1 and newfixchans.count(chans+1+layer*32) >= 1:
                        pygame.draw.rect(screen, (200,5,5), pygame.Rect(chans*27+15,layer*25+18, 27,25))
                    mytext = smallfont.render(str(chans+1+layer*32), True, WHITE)
                    screen.blit(mytext,[chans*27+20,layer*25+20, 280, 50])
            if len(fixes) > 4:
                if (fixpage+1)*4 < len(fixes):
                    up.draw()
                if fixpage > 0:
                    down.draw()
                try:
                    for layer in range(4):
                        num = layer+fixpage*4
                        fixtureRef = fixes[num]
                        mybutton = button(20,420+layer*55, 850, 50, str(num)+" "+str(fixtureRef.Name)+"   Type: "+str(fixtureRef.Type)+"  DMX Start: "+str(fixtureRef.startChan) ,(100,100,100),(15,15,15),(40,40,40),5,openFixPage,args=fixtureRef)
                        mybutton.draw()
                except:
                    pass
            else:
                for index,fixtures in enumerate(fixes):
                    try:
                        fixtureRef = fixes[index]
                    except:
                        pass
                    mybutton = button(20,420+index*55, 850, 50, str(index)+" "+str(fixtureRef.Name)+"   Type: "+str(fixtureRef.Type)+"  DMX Start: "+str(fixtureRef.startChan) ,(100,100,100),(15,15,15),(40,40,40),5,openFixPage,args=fixtureRef)
                    mybutton.draw()
        case 3.2:
            fixRename.draw(screen)
            backbutton1.draw()
            RemovePatch.draw()
            try:
                texts = [font.render(str(patchSelectedFix.Name), True, (255,255,255)),font.render("Start DMX Address: "+str(patchSelectedFix.startChan), True, (255,255,255)),font.render("DMX Channels Used: "+str(patchSelectedFix.dmxsize), True, (255,255,255)),font.render(str(patchSelectedFix.Type), True, (255,255,255)),font.render("Fixture "+str(fixes.index(patchSelectedFix)), True, (255,255,255))]
            except:
                pass
            screen.blit(texts[0],[20,20, 280, 50])
            screen.blit(texts[3],[20,55, 280, 50])
            screen.blit(texts[1],[20,90, 280, 50])
            screen.blit(texts[4],[20,350, 280, 50])
        case 4:
            screen.blit(setupTexts[2],[20,20, 280, 50])
            screen.blit(setupTexts[0],[20,650, 280, 60])
            screen.blit(setupTexts[1],[20,690, 280, 50])
            saveShow.draw()
            loadShow.draw()
            newShow.draw()
    pygame.display.flip()
pygame.quit()