import pygame
import random
import cProfile
pygame.init()
infoobject = pygame.display.Info()
pygame.mixer.init()

screent = pygame.display.set_mode((1440, 810), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWACCEL)
screen  = pygame.Surface((1440, 810))
uscreen = pygame.Surface((1440, 810), pygame.SRCALPHA)
display_size = screen.get_size()
oisplay_size = display_size
pdsize = None
new_render = True
pygame.display.set_caption("Game")

# Images
bg_img               = pygame.image.load("m1.png")
bg_mask_img          = pygame.image.load("m1_mask.png")
player_img           = pygame.image.load("player.png")
npc1_img             = pygame.image.load("npc1.png")
icon1_img            = pygame.image.load("icon1.png")
icon2_img            = pygame.image.load("icon2.png")
icon3_img            = pygame.image.load("icon3.png")
npc_spawn_mask_img   = pygame.image.load("npc_spawn_mask.png")

# Audio
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1,0.0)

# Player
player_pos_x = 312
player_pos_y = 44
player_speed = 4
player_score = 150
player_pscor = None
player_live  = 3

# Game
game_fps     = 30
game_over    = False
font         = pygame.font.SysFont(None, 24)
fontm        = pygame.font.SysFont("monospace", 12)
fontb        = pygame.font.SysFont("monospace", 40)
redc         = 0

screen_items = {"ui_help":False, "fps":True, "render_background":True}

# Masks
player_mask   = pygame.mask.from_surface(player_img)
bg_mask       = pygame.mask.from_surface(bg_mask_img)
npc_mask      = pygame.mask.from_surface(npc1_img)
npc_spaw_mask = pygame.mask.from_surface(npc_spawn_mask_img)
mouse_mask    = pygame.mask.from_surface(pygame.surface.Surface((10, 10)))

# NPCs
npc_count    = 100

def inw():
    if(bg_mask.overlap(player_mask, (player_pos_x, player_pos_y))==None):
        return(False)
    else:
        return(True)

#===============================================================================================    NPC
class npc_class:                                                   # npc_class
    def __init__(self, px, py, s):
        self.pos_x = px
        self.pos_y = py
        self.s = s
    def setup(self):
        while(True):
            no = False
            #print("t")
            for a in npcs:
                if(npc_mask.overlap(npc_mask, (self.pos_x-a.pos_x, self.pos_y-a.pos_y)) and a!=self):
                    no = True
            if(npc_spaw_mask.overlap(npc_mask, (self.pos_x, self.pos_y))!=None or no or npc_mask.overlap(player_mask, (self.pos_x-player_pos_x, self.pos_y-player_pos_y))):
                self.pos_x = random.randint(190, 430)
                self.pos_y = random.randint(120, 460)
            else:
                break
        self.new = True
    def render(self):
        if(len(str(self.s))>3):
            count = 0
            s_str = ""
            for a in range(len(str(self.s))):
                count += 1
                s_str = str(self.s)[(len(str(self.s))-1)-a] + s_str
                if(count>=3):
                    count = 0
                    s_str = "." + s_str
            if(s_str[0]=="."):
                s_str = s_str[1:]
        else:
            s_str = str(self.s)
        if(new_render or self.new):
            st = font.render(str(s_str), True, (0, 100, 0))
            if(display_size[1]>600):
                self.text_simg = pygame.transform.scale(st, (round(8*(st.get_rect().size[0]/st.get_rect().size[1])*(display_size[1]/600)), round(8*(display_size[1]/600))))
            else:
                self.text_simg = pygame.transform.scale(st, (round(8*(st.get_rect().size[0]/st.get_rect().size[1])*(display_size[1]/300)), round(8*(display_size[1]/300))))
            self.npc_simg = pygame.transform.scale(npc1_img, (round(16*(display_size[1]/600)), round(16*(display_size[1]/600))))
            self.new = False
        screen.blit(self.npc_simg, (round((display_size[0]//2)-(round(640*(display_size[1]/600))//2)+(self.pos_x*(display_size[1]/600))), round(self.pos_y*(display_size[1]/600))))
        if(display_size[1]>600):
            screen.blit(self.text_simg, ((round((display_size[0]//2)-(round(640*(display_size[1]/600))//2)+(self.pos_x*(display_size[1]/600)))), round((self.pos_y-8)*(display_size[1]/600))))
        else:
            screen.blit(self.text_simg, ((round((display_size[0]//2)-(round(650*(display_size[1]/600))//2)+(self.pos_x*(display_size[1]/600)))), round((self.pos_y-8)*(display_size[1]/600))))
    def dead(self):
        global npc_count
        dnpcs.append(self)
        npc_count -= 1
        if(npc_count>20):
            npcs.append(npc_class(random.randint(190, 430), random.randint(120, 460), random.randint(player_score//2, player_score*2)))
            npcs[-1].setup()
    def update(self):
        global player_score, player_live, redc
        if(player_mask.overlap(npc_mask, (self.pos_x-player_pos_x, self.pos_y-player_pos_y))!=None):
            self.dead()
            if(self.s<=player_score):
                player_score += self.s//5
            else:
                player_live -= 1
                player_score -= self.s//10
                redc = 10
        self.render()

                                                                        # Generate NPCS
dnpcs = []
npcs = [npc_class(player_pos_x+16, player_pos_y, random.randint(100, 150))]
for a in range(20):
    npcs.append(npc_class(random.randint(190, 430), random.randint(120, 460), random.randint(100, 500)))
for a in npcs:
    a.setup()
#=======================================================================================================
# Render Background


def render_background(newRender):
    if(render_background.offset>display_size[1]):
        render_background.offset = 0
    global bgimg
    if(newRender):
        newBackgroundImage()
    screen.blit(bgimg, (0,0), ((0, display_size[1] - render_background.offset), display_size))
    render_background.offset += 5
render_background.offset=0

def newBackgroundImage():
    star_list = []
    global bgimg
    for a in range(random.randint(1000, 3000)):
        star_list.append((random.randint(0, display_size[0]-1), random.randint(0, display_size[1]-1)))
    bgimg = pygame.Surface((display_size[0],2*display_size[1]))
    for a in star_list:
        bgimg.fill((0xff,0xff,0xff),((a[0],a[1]),(1,1)))
        bgimg.fill((0xff,0xff,0xff),((a[0],display_size[1]+a[1]),(1,1)))


#========================================================================================================
def dg(keys, fps):                                                     # Game
    global player_pos_x, player_pos_y, dnpcs, game_over, player_live, game_win, player_score, pdsize, bg2_simg, bg_simg, icon1_simg, icon2_simg, icon3_simg, new_render, player_pscor, player_simg, player_score_texts
    pygame.display.set_caption("Game  "+str(round(fps))+" FPS")

    if(player_score<100):
        player_live = -1
        player_score = 0

    if(player_live<0):
        game_over = True
        game_win = False
        player_live = 0

    if(npc_count==0):
        game_over = True
        game_win = True



    dnpcs = []
    if(game_over==False):
        if(keys["key_up"]):                                                # Player_Move
            player_pos_y -= player_speed
            if(inw()):
                player_pos_y += player_speed
        if(keys["key_down"]):
            player_pos_y += player_speed
            if(inw()):
                player_pos_y -= player_speed
        if(keys["key_left"]):
            player_pos_x -= player_speed
            if(inw()):
                player_pos_x += player_speed
        if(keys["key_right"]):
            player_pos_x += player_speed
            if(inw()):
                player_pos_x -= player_speed

    screen.fill((0, 0, 0))

    if(display_size!=pdsize):
        pdsize = display_size
        new_render = True
        bg_simg    = pygame.transform.scale(bg_img, (round(640*(display_size[1]/600)), round(640*(display_size[1]/600))))
        icon1_simg = pygame.transform.scale(icon1_img, (round(16*(display_size[1]/600)), round(16*(display_size[1]/600))))
        icon2_simg = pygame.transform.scale(icon2_img, (round(16*(display_size[1]/600)), round(16*(display_size[1]/600))))
        icon3_simg = pygame.transform.scale(icon3_img, (round(16*(display_size[1]/600)), round(16*(display_size[1]/600))))
    else:
        new_render = False

    if(screen_items["render_background"]):
        render_background(new_render)                                                                                                     # Background2 Image
    screen.blit(bg_simg, ((display_size[0]//2)-(round(640*(display_size[1]/600))//2), 0))                                         # Background_Image
    uscreen.blit(icon1_simg, (round(10*(display_size[1]/600)), round(570*(display_size[1]/600))))                                  # Icon1_Image
    uscreen.blit(icon2_simg, (round(50*(display_size[1]/600)), round(572*(display_size[1]/600))))                                  # Icon2_Image
    uscreen.blit(icon3_simg, (round(110*(display_size[1]/600)), round(570*(display_size[1]/600))))

    if(len(str(player_score))>3):
        count = 0
        player_score_str = ""
        for a in range(len(str(player_score))):
            count += 1
            player_score_str = str(player_score)[(len(str(player_score))-1)-a] + player_score_str
            if(count>=3):
                count = 0
                player_score_str = "." + player_score_str
        if(player_score_str[0]=="."):
            player_score_str = player_score_str[1:]
    else:
        player_score_str = str(player_score)
                                                                           # Player_Lives_Text

    player_live_text  = font.render(str(player_live), True, (255, 0, 0))
    npc_count_text    = font.render(str(npc_count),   True, (255, 255, 0))
    player_score_text = font.render(player_score_str, True, (0, 255, 0))
    # .get_rect().size
    uscreen.blit(pygame.transform.scale(player_live_text,  (round(16*(player_live_text.get_rect().size[0] /player_live_text.get_rect().size[1] )*(display_size[1]/600)), round(16*(display_size[1]/600)))), (round(30*(display_size[1]/600)),  round(573*(display_size[1]/600))))
    uscreen.blit(pygame.transform.scale(npc_count_text,    (round(16*(npc_count_text.get_rect().size[0]   /npc_count_text.get_rect().size[1]   )*(display_size[1]/600)), round(16*(display_size[1]/600)))), (round(70*(display_size[1]/600)),  round(573*(display_size[1]/600))))
    uscreen.blit(pygame.transform.scale(player_score_text, (round(16*(player_score_text.get_rect().size[0]/player_score_text.get_rect().size[1])*(display_size[1]/600)), round(16*(display_size[1]/600)))), (round(130*(display_size[1]/600)), round(573*(display_size[1]/600))))

                  # Player_Image

    if(new_render or player_score!=player_pscor):
        player_score_text = font.render(player_score_str, True, (100, 0, 0))
        if(display_size[1]>600):
            player_score_texts = pygame.transform.scale(player_score_text, (round(8*(player_score_text.get_rect().size[0]/player_score_text.get_rect().size[1])*(display_size[1]/600)), round(8*(display_size[1]/600))))
        else:
            player_score_texts = pygame.transform.scale(player_score_text, (round(8*(player_score_text.get_rect().size[0]/player_score_text.get_rect().size[1])*(display_size[1]/300)), round(8*(display_size[1]/300))))
        player_simg = pygame.transform.scale(player_img, (round(16*(display_size[1]/600)), round(16*(display_size[1]/600))))
        player_pscor = player_score
    screen.blit(player_simg, (round((display_size[0]//2)-(round(640*(display_size[1]/600))//2)+(player_pos_x*(display_size[1]/600))), round(player_pos_y*(display_size[1]/600))))
    if(display_size[1]>600):
        screen.blit(player_score_texts, ((round((display_size[0]//2)-(round(640*(display_size[1]/600))//2)+(player_pos_x*(display_size[1]/600)))), round((player_pos_y-8)*(display_size[1]/600))))
    else:
        screen.blit(player_score_texts, ((round((display_size[0]//2)-(round(650*(display_size[1]/600))//2)+(player_pos_x*(display_size[1]/600)))), round((player_pos_y-8)*(display_size[1]/600))))
                                                                           # Player_Text



    for a in npcs:                                                     # dnpcs
        a.update()
    for a in dnpcs:
        npcs.remove(a)

#    print(pygame.mouse.get_pos())

#    print("\033[1A", player_pos_x, ", ", player_pos_y, "            ") # Print player_pos
    if(screen_items["ui_help"]):
        uscreen.blit(fontm.render("------[ Help ]------", True, (100, 255, 100)), (1, 12*1))
        uscreen.blit(fontm.render("Show FPS         : F", True, (100, 255, 100)), (1, 12*2))
        uscreen.blit(fontm.render("Show Help        : H", True, (100, 255, 100)), (1, 12*3))
        uscreen.blit(fontm.render("Render Background: B", True, (100, 255, 100)), (1, 12*4))
        uscreen.blit(fontm.render("Fullscreen       : F11", True, (100, 255, 100)), (1, 12*5))
    if(screen_items["fps"]):
        uscreen.blit(fontm.render(f"{round(fps)} FPS", True, (255, 100, 100)), (1, 1))
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def toggle(i):
    if(i==True):
        i = False
    elif(i==False):
        i = True
    return(i)

run = True
clock = pygame.time.Clock()
keys = {"key_up":False, "key_down":False, "key_left":False, "key_right":False}
while(run):
    display_size = screent.get_size()
    if(display_size!=oisplay_size):
        screen  = pygame.Surface(display_size)
        uscreen = pygame.Surface(display_size, pygame.SRCALPHA)
        oisplay_size = display_size

    for e in pygame.event.get():
        if(e.type==pygame.QUIT):
            run = False
        elif(e.type==pygame.KEYDOWN):
            if(e.key in (pygame.K_UP, pygame.K_w)):
                keys["key_up"] = True
            elif(e.key in (pygame.K_DOWN, pygame.K_s)):
                keys["key_down"] = True
            elif(e.key in (pygame.K_LEFT, pygame.K_a)):
                keys["key_left"] = True
            elif(e.key in (pygame.K_RIGHT, pygame.K_d)):
                keys["key_right"] = True
            elif(e.key==pygame.K_q):
                run = False
            elif(e.key==pygame.K_h):
                screen_items["ui_help"] = toggle(screen_items["ui_help"])
            elif(e.key==pygame.K_f):
                screen_items["fps"] = toggle(screen_items["fps"])
            elif(e.key==pygame.K_b):
                screen_items["render_background"] = toggle(screen_items["render_background"])
                newBackgroundImage()
            elif(e.key==pygame.K_F11):
                pygame.display.set_mode((infoobject.current_w, infoobject.current_h), pygame.FULLSCREEN)
        elif(e.type==pygame.KEYUP):
            if(e.key in (pygame.K_UP, pygame.K_w)):
                keys["key_up"] = False
            elif(e.key in (pygame.K_DOWN, pygame.K_s)):
                keys["key_down"] = False
            elif(e.key in (pygame.K_LEFT, pygame.K_a)):
                keys["key_left"] = False
            elif(e.key in (pygame.K_RIGHT, pygame.K_d)):
                keys["key_right"] = False

    dg(keys, clock.get_fps())
    if(game_over):
        text = fontb.render("Game Over", True, (200, 100, 0))
        text_img = pygame.transform.scale(text, (round(64*(text.get_rect().size[0]/text.get_rect().size[1])*(display_size[1]/600)), round(64*(display_size[1]/600))))
        uscreen.blit(text_img, ((display_size[0]//2) - (text_img.get_rect().size[0]//2), (display_size[1]//6)))
        if(game_win):
            text = fontb.render("You Win", True, (0, 200, 150))
            text_img = pygame.transform.scale(text, (round(32*(text.get_rect().size[0]/text.get_rect().size[1])*(display_size[1]/600)), round(32*(display_size[1]/600))))
            uscreen.blit(text_img, ((display_size[0]//2) - (text_img.get_rect().size[0]//2), (display_size[1]//4)))
        else:
            text = fontb.render("You Lose", True, (100, 0, 0))
            text_img = pygame.transform.scale(text, (round(32*(text.get_rect().size[0]/text.get_rect().size[1])*(display_size[1]/600)), round(32*(display_size[1]/600))))
            uscreen.blit(text_img, ((display_size[0]//2) - (text_img.get_rect().size[0]//2), (display_size[1]//4)))
    screent.blit(pygame.transform.scale(screen, (display_size[0]*2, display_size[1]*2)), (0-round((player_pos_x/600)*display_size[1]), 0-round((player_pos_y/600)*display_size[1])))
    #uscreen.set_alpha(70)
    screent.blit(uscreen, (0, 0))
    uscreen.fill((255, 0, 0, redc*25))
    if(redc>0):
        redc -= 1
    pygame.display.flip()
    clock.tick(game_fps)
pygame.quit()
