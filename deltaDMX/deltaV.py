import pygame,sys,math,colorsys

def init():
    global fixtures
    global windows
    global layoutViews
    global UIbuttons
    global UIinputBoxes
    global hardwareFaders
    global cueLists
    global playbacks
    global effects
    global dmxOutputBuffer
    global mouseDown
    fixtures = []
    windows = []
    layoutViews = []
    UIbuttons = []
    UIinputBoxes = []
    hardwareFaders = []
    cueLists = []
    playbacks = []
    effects = []
    dmxOutputBuffer = {}
    mouseDown = False

init()
pygame.init()
colorpickerImg = pygame.image.load("5d107b5ed8fdb8964fbad44174bc9b18.png")
font = pygame.font.Font('Roboto-Regular.ttf', 32)
smallfont = pygame.font.Font('Roboto-Medium.ttf', 12)
screen = pygame.display.set_mode((1280, 800))
clock = pygame.time.Clock()

class patchWindow():
    def

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
        for box in UIinputBoxes:
                box.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    
    mouse = pygame.mouse.get_pos()
    screen.fill((0,0,0))