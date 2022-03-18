#Importing
import sys, pygame, time, fixtures, pygame_textinput

#Initialization
WIDTH = 1920
HEIGHT = 1080
FPS = 60
BackColor = (15, 15, 15)
pygame.init()
smallfont = pygame.font.Font('ROBOTO-MEDIUM.ttf',25)
smallerfont = pygame.font.Font('ROBOTO-MEDIUM.ttf',20)
evensmallerfont = pygame.font.Font('ROBOTO-MEDIUM.ttf',16)
bigfont = pygame.font.Font('ROBOTO-MEDIUM.ttf',35)
active = False
textinput = pygame_textinput.TextInputVisualizer(font_object=smallfont, font_color=(255,255,255), cursor_color=(255,255,255))
textinput.antialias = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trigger")
clock = pygame.time.Clock()
rect = pygame.Rect(50, 60, 200, 80)
dmxBuffer = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0,24:0,25:0,26:0,27:0,28:0,29:0,30:0,31:0,32:0,33:0,34:0,35:0,36:0,37:0,38:0,39:0,40:0,41:0,42:0,43:0,44:0,45:0,46:0,47:0,48:0,49:0,50:0,51:0,52:0,53:0,54:0,55:0,56:0,57:0,58:0,59:0,60:0,61:0,62:0,63:0,64:0,65:0,66:0,67:0,68:0,69:0,70:0,71:0,72:0,73:0,74:0,75:0,76:0,77:0,78:0,79:0,80:0,81:0,82:0,83:0,84:0,85:0,86:0,87:0,88:0,89:0,90:0,91:0,92:0,93:0,94:0,95:0,96:0,97:0,98:0,99:0,100:0,101:0,102:0,103:0,104:0,105:0,106:0,107:0,108:0,109:0,110:0,111:0,112:0,113:0,114:0,115:0,116:0,117:0,118:0,119:0,120:0,121:0,122:0,123:0,124:0,125:0,126:0,127:0,128:0,129:0,130:0,131:0,132:0,133:0,134:0,135:0,136:0,137:0,138:0,139:0,140:0,141:0,142:0,143:0,144:0,145:0,146:0,147:0,148:0,149:0,150:0,151:0,152:0,153:0,154:0,155:0,156:0,157:0,158:0,159:0,160:0,161:0,162:0,163:0,164:0,165:0,166:0,167:0,168:0,169:0,170:0,171:0,172:0,173:0,174:0,175:0,176:0,177:0,178:0,179:0,180:0,181:0,182:0,183:0,184:0,185:0,186:0,187:0,188:0,189:0,190:0,191:0,192:0,193:0,194:0,195:0,196:0,197:0,198:0,199:0,200:0,201:0,202:0,203:0,204:0,205:0,206:0,207:0,208:0,209:0,210:0,211:0,212:0,213:0,214:0,215:0,216:0,217:0,218:0,219:0,220:0,221:0,222:0,223:0,224:0,225:0,226:0,227:0,228:0,229:0,230:0,231:0,232:0,233:0,234:0,235:0,236:0,237:0,238:0,239:0,240:0,241:0,242:0,243:0,244:0,245:0,246:0,247:0,248:0,249:0,250:0,251:0,252:0,253:0,254:0,255:0,256:0,257:0,258:0,259:0,260:0,261:0,262:0,263:0,264:0,265:0,266:0,267:0,268:0,269:0,270:0,271:0,272:0,273:0,274:0,275:0,276:0,277:0,278:0,279:0,280:0,281:0,282:0,283:0,284:0,285:0,286:0,287:0,288:0,289:0,290:0,291:0,292:0,293:0,294:0,295:0,296:0,297:0,298:0,299:0,300:0,301:0,302:0,303:0,304:0,305:0,306:0,307:0,308:0,309:0,310:0,311:0,312:0,313:0,314:0,315:0,316:0,317:0,318:0,319:0,320:0,321:0,322:0,323:0,324:0,325:0,326:0,327:0,328:0,329:0,330:0,331:0,332:0,333:0,334:0,335:0,336:0,337:0,338:0,339:0,340:0,341:0,342:0,343:0,344:0,345:0,346:0,347:0,348:0,349:0,350:0,351:0,352:0,353:0,354:0,355:0,356:0,357:0,358:0,359:0,360:0,361:0,362:0,363:0,364:0,365:0,366:0,367:0,368:0,369:0,370:0,371:0,372:0,373:0,374:0,375:0,376:0,377:0,378:0,379:0,380:0,381:0,382:0,383:0,384:0,385:0,386:0,387:0,388:0,389:0,390:0,391:0,392:0,393:0,394:0,395:0,396:0,397:0,398:0,399:0,400:0,401:0,402:0,403:0,404:0,405:0,406:0,407:0,408:0,409:0,410:0,411:0,412:0,413:0,414:0,415:0,416:0,417:0,418:0,419:0,420:0,421:0,422:0,423:0,424:0,425:0,426:0,427:0,428:0,429:0,430:0,431:0,432:0,433:0,434:0,435:0,436:0,437:0,438:0,439:0,440:0,441:0,442:0,443:0,444:0,445:0,446:0,447:0,448:0,449:0,450:0,451:0,452:0,453:0,454:0,455:0,456:0,457:0,458:0,459:0,460:0,461:0,462:0,463:0,464:0,465:0,466:0,467:0,468:0,469:0,470:0,471:0,472:0,473:0,474:0,475:0,476:0,477:0,478:0,479:0,480:0,481:0,482:0,483:0,484:0,485:0,486:0,487:0,488:0,489:0,490:0,491:0,492:0,493:0,494:0,495:0,496:0,497:0,498:0,499:0,500:0,501:0,502:0,503:0,504:0,505:0,506:0,507:0,508:0,509:0,510:0,511:0}
parkedChans = [1]
consoleFixtures = []
input_rect = pygame.Rect(0, 1040, 1920, 40)
mouse = (0,0)
uiButtons = []
menuSelected = 2
fixSelection = 0
fixButtons = []
textBoxRender = False
textBoxPos = (0,0)

#Functions
def select(self):
    for x in uiButtons:
        x.deselect()
    self.select()
    global menuSelected
    menuSelected = self.args

def selectFixture(fixture):
        global menuSelected
        menuSelected = 8
        global fixSelection
        fixSelection = fixture

def newFixture(garbage):
    newFix = fixtures.fixture(1,1,False,"Fixture " + str(len(consoleFixtures)))
    consoleFixtures.append(newFix)
    print(str(len(consoleFixtures)))

def updateConsole(test):
    pygame.quit()
    time.sleep(0.5)
    exec(open("updater.py").read())
    time.sleep(0.5)
    sys.exit()

def setChan(channel, value):
    dmxBuffer[channel] = value

def parkChans(chansToPark):
    for chan in chansToPark:
        setChan(chan-1, 255)

#Classes
class UIButton(object):
    def __init__(self, x, y, width, height, text, callback, args, start_selected, funtionalPage, sendself):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = smallfont.render(text , True , (255,255,255))
        self.width = width
        self.height = height
        self.x = x
        self.sendself = sendself
        self.y = y
        self.callback = callback
        self.args = args
        self.selected = start_selected
        uiButtons.append(self)
        self.funcPage = funtionalPage
    
    def draw(self, surface):
        if self.selected:
            pygame.draw.rect(surface,(50,50,50),self.rect)
        else:
            if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
                pygame.draw.rect(surface,(140,140,140),self.rect) 
            else:
                pygame.draw.rect(surface,(100,100,100),self.rect)

        screen.blit(self.text , (self.x+5,self.y+5))
    
    def update(self):
        if self.funcPage == 0:
            if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
                if self.sendself:
                    self.callback(self)
                else:
                    self.callback(self.args)
        elif menuSelected == self.funcPage:
            if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
                if self.sendself:
                    self.callback(self)
                else:
                    self.callback(self.args)
    
    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

def showTextBox(x,y,clear):
    if clear:
        textinput.value = ""
    global textBoxPos
    textBoxPos = (x,y)
    global textBoxRender
    textBoxRender = True
    

#DMX Channel Parking
parkChans(parkedChans)

#UI Elements
dmxBufferWindow = UIButton(10,1000,200,37, "Color Picker", select, 1, False, 0, True)
dmxFixtures = UIButton(215,1000,200,37, "Fixtures", select, 2, True, 0, True)
Patch = UIButton(420,1000,200,37, "Patch", select, 3, False, 0, True)
SequenceEditor = UIButton(625,1000,200,37, "Sequence Editor", select, 4, False, 0, True)
faderEditor = UIButton(830,1000,200,37, "Faders", select, 5, False,0, True)
liveDisplay = UIButton(1035,1000,200,37, "Live Display", select, 6, False,0, True)
setup = UIButton(1240,1000,200,37, "Settings", select, 7, False,0, True)
rename = UIButton(20,65,250,37, "Rename Fixture", select, 7, False,0, True)
update = UIButton(20,65,190,37, "Update Console", updateConsole, None, False,7,True)
addFixture = UIButton(1750,20,57,36, "Add", newFixture, None, False,2,False)

#Return Funcs
def goToMenu(self):
    select(dmxFixtures)

backFixture = UIButton(1680,20,190,37, "Back", goToMenu, 2, False, 0 , True)

#Run Loop
running = True
while running:
    events = pygame.event.get()
    # Feed it with events every frame
    textinput.update(events)
    #Event Loop
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for x in uiButtons:
                    x.update()

    screen.fill(BackColor)
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (50,50,50), pygame.Rect(0, 0, 1920, 1000))
    pygame.draw.rect(screen, (50,50,50), pygame.Rect(1620, 1030, 300, 50))
    pygame.draw.rect(screen, BackColor, pygame.Rect(4, 4, 1912, 992))
    dmxBufferWindow.draw(screen)
    dmxFixtures.draw(screen)
    Patch.draw(screen)
    SequenceEditor.draw(screen)
    faderEditor.draw(screen)
    liveDisplay.draw(screen)
    setup.draw(screen)

    #Different Screens
    match menuSelected:
        case 1:
            titleText = bigfont.render("Color Picker" , True , (255,255,255))
        case 2:
            titleText = bigfont.render("All Fixtures" , True , (255,255,255))
            addFixture.draw(screen)
            for fixes in range(len(consoleFixtures)):
                if len(fixButtons) < len(consoleFixtures):
                    fixButtons.append(UIButton(20, len(fixButtons)*50+65,1850,50, str(consoleFixtures[len(fixButtons)].name), selectFixture, int(len(fixButtons)), False, 2, False))
                elif len(fixButtons) > len(consoleFixtures):
                    fixButtons = []
            for button in fixButtons:
                button.draw(screen)
        case 3:
            titleText = bigfont.render("Patch Display" , True , (255,255,255))
            warningone = smallfont.render("Parked Channels Will Be Purple", True, (255,255,255))
            warningtwo = smallfont.render("Double-Patched Channels Will Be Red", True, (255,255,255))
            screen.blit(warningone,(10,930))
            screen.blit(warningtwo,(10,960))
            for chans in range(32):
                for layer in range(16):
                    if ((chans+1+layer*32) in parkedChans):
                        channelValue = evensmallerfont.render(str(dmxBuffer.get(chans+layer*32)), True, (150,0,255))
                        text = smallerfont.render(str(chans+1+layer*32), True, (150,0,255))
                    else:
                        channelValue = evensmallerfont.render(str(dmxBuffer.get(chans+layer*32)), True, (255,255,255))
                        text = smallerfont.render(str(chans+1+layer*32), True, (255,255,255))
                    screen.blit(text, ((chans*59)+20, layer*52+70))
                    screen.blit(channelValue, ((chans*59)+20, (layer*52+70)+20))
        case 4:
            titleText = bigfont.render("Edit Sequences" , True , (255,255,255))
        case 5:
            titleText = bigfont.render("Edit Control Surface" , True , (255,255,255))
        case 6:
            titleText = bigfont.render("Live Show" , True , (255,255,255))
        case 7:
            titleText = bigfont.render("Settings" , True , (255,255,255))
            update.draw(screen)
            versionText = smallfont.render("Firmware 0.0.1C", True, (255,255,255))
            screen.blit(versionText,(10,960))
        case 8:
            fixture = consoleFixtures[fixSelection]
            titleText = bigfont.render(str(fixture.name) , True , (255,255,255))
            backFixture.draw(screen)
            rename.draw(screen)

    if textBoxRender:
        screen.blit(textinput.surface, (10, 10))
    screen.blit(titleText,(20,20))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()