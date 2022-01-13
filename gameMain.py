import pygame

'''
Game Variables
'''

window = (800, 800)
screen = pygame.display.set_mode(window)
clock = pygame.time.Clock()
fps = 30
ani = 16

'''
World
'''

background = pygame.Surface(window)

'''
Player
'''

slime = pygame.image.load('images/slimeFront.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):

        # sprite placement
        pygame.sprite.Sprite.__init__(self)
        self.moveX = 0
        self.moveY = 0
        self.frame = 0

        # facing table
        self.face = {
            'up': False,
            'right': False,
            'down': False,
            'left': False
        }

        # initializes the sprite image
        self.images = []
        for i in range(1, 7):
            img = pygame.transform.scale(pygame.image.load(f'images/Player Sprites/playerSprite{i}.png'), (64, 64))

            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

        # attacks
        self.fireball = FireBall(self)

    def sprite_move(self, x, y):

        # moves sprite position based on x or y input
        self.moveX += x
        self.moveY += y

    def sprite_update(self):

        # update sprite position
        self.rect.x = self.rect.x + self.moveX
        self.rect.y = self.rect.y + self.moveY

        # animation
        if self.frame % 2 != 0:
            if self.frame >= 5 * ani:
                self.frame = 0
            self.frame += 1

        else:
            if self.frame >= 6 * ani:
                self.frame = 0
            self.frame += 2

        self.image = self.images[self.frame // ani]


    # stores the last facing position of the player
    def facing(self, face):
        for f in self.face:
            self.face[f] = False
            if face == f:
                self.face[f] = True



'''
Attacks
'''

class FireBall(pygame.sprite.Sprite):
    def __init__(self, caster):

        pygame.sprite.Sprite.__init__(self)
        self.moveX = 10
        self.moveY = 10
        self.caster = caster

        self.images = []
        for i in range(1, 7):
            img = pygame.image.load(f'images/fireBall/fireBall1.png').convert()
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            

    def cast(self):
        self.rect.x = self.caster.rect.x
        self.rect.y = self.caster.rect.y
        for num, i in enumerate(self.caster.face):
            if self.caster.face[i]:
                if num == 0:
                    self.rect.y -= self.moveY
                if num == 1:
                    self.rect.x += self.moveX
                if num == 2:
                    self.rect.y += self.moveY
                if num == 3:
                    self.rect.x -= self.moveX

        screen.blit(self.image, (16, 16))




'''
Player initialization
'''

player = Player()

# sprite starting position
player.rect.x = 0
player.rect.y = 0

# adds the player sprite to a sprite list
player_list = pygame.sprite.Group()
player_list.add(player)

# the number of pixels the sprite moves per frame
speed = 5

print(player.images)
'''
Game Loop
'''

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.KEYDOWN:
            if player.frame % 2 != 0:
                player.frame += 1
            if event.key == ord('a'):
                player.sprite_move(-speed, 0)
                player.facing('left')
            if event.key == ord('d'):
                player.sprite_move(speed, 0)
                player.facing('right')
            if event.key == ord('w'):
                player.sprite_move(0, -speed)
                player.facing('up')
            if event.key == ord("s"):
                player.sprite_move(0, speed)
                player.facing('down')
            if event.key == pygame.K_SPACE:
                player.fireball.cast()
                print('SPACE')

        if event.type == pygame.KEYUP:
            if event.key == ord('a'):
                player.sprite_move(0, 0)
                player.moveX = 0
            if event.key == ord('d'):
                player.sprite_move(0, 0)
                player.moveX = 0
            if event.key == ord('w'):
                player.sprite_move(0, 0)
                player.moveY = 0
            if event.key == ord("s"):
                player.sprite_move(0, 0)
                player.moveY = 0

    print(player.frame // ani)
    screen.blit(background, (0, 0))
    player.sprite_update()
    player_list.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
