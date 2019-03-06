import pygame
import random
from time import sleep, clock
class RenderObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
    def render(self):
        pass
    def handleVelocity(self, drag = True):
        self.x += self.vx
        self.y += self.vy
        if drag:
            if self.vx > 0:
                self.vx -= 1
            elif self.vx < 0:
                self.vx += 1
            if self.vy > 0:
                self.vy -= 1
            elif self.vy < 0:
                self.vy += 1
    def keepInBounds(self):
        if self.x < 0:
            self.x = 0
            self.vx *= -1
            #self.vy *= -1
        if self.y < 0:
            self.y = 0
            #self.vx *= -1
            self.vy *= -1
        if (self.x + self.width) > 1280:
            self.x = 1280 - self.width
            self.vx *= -1
            #self.vy *= -1
        if (self.y + self.height) > 720:
            self.y = 720 - self.height
            #self.vx *= -1
            self.vy *= -1
    def collide(self, renderList):
        for obj in renderList:
            if not obj == self:
                if (self.x < obj.x + obj.width and self.x + self.width > obj.x and self.y < obj.y + obj.height and self.y + self.height > obj.y):
                    self.bounce(True, True)
    def push(self, vx, vy):
        self.vx += vx
        self.vy += vy
    def bounce(self, xb, yb):
        if xb:
            self.vx *= -1
        if yb:
            self.vy *= -1
class Rect(RenderObject):
    def __init__(self, x, y, width, height, tex):
        RenderObject.__init__(self, x, y, width, height)
        self.tex = pygame.image.load(tex).convert()
    def render(self):
        self.handleVelocity(False)
        self.keepInBounds()
        self.collide(renderList)
        screen.blit(self.tex, (self.x, self.y))
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill((255, 255, 255))
pygame.display.flip()
renderList = []
renderList.append(Rect(0, 0, 32, 32, 'wall.png'))
renderList.append(Rect(128, 128, 32, 32, 'grass.png'))
renderList[1].push(10, 10)
for i in range(2, 10):
    renderList.append(Rect(random.randint(128, 1200), random.randint(128, 680), 32, 32, 'grass.png'))
    renderList[i].push(random.randint(1, 10), random.randint(1, 10))
done = False
frameLimiter = True
while not done:
    time = clock()
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen.fill((255, 255, 255))
                pygame.display.flip()
            if event.key == pygame.K_SPACE:
                for obj in renderList:
                    obj.push(obj.vx*1.2, obj.vy*1.2)
            if event.key == pygame.K_LSHIFT:
                frameLimiter = not frameLimiter
                print("FrameLimiter toggled")
            if event.key == pygame.K_n:
                renderList.append(Rect(random.randint(128, 1200), random.randint(128, 680), 32, 32, 'grass.png'))
                renderList[len(renderList)-1].push(random.randint(1, 10), random.randint(1, 10))
    for obj in renderList:
        obj.render()
    pygame.display.flip()
    print(clock()-time)
    if frameLimiter:
        sleep(.017)
exit()
