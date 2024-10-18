import pygame
pygame.init()

w_width = 1000 
w_height = 500
screen = pygame.display.set_mode((w_width,w_height))

pygame.display.set_caption("Arbegna")

clock = pygame.time.Clock()
bg_img = pygame.image.load("../basic/img/bg.png")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1,10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1,10)]
char = pygame.image.load('soldier/standing.png')
moveRight = [pygame.image.load(f'enemy/R{i}.png') for i in range(1,10)]
moveLeft = [pygame.image.load(f'enemy/L{i}.png') for i in range(1,10)]
font = pygame.font.SysFont("helvetica", 30, 1, 1)
score = 0
bulletsound = pygame.mixer.Sound("sounds/Bulletsound.mp3")
hitsound = pygame.mixer.Sound("sounds/hit_local.mp3")
hurtsound = pygame.mixer.Sound("sounds/oyne.mp3")
music = pygame.mixer.music.load("sounds/Ethiopian_Patriotic.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 5 
        self.damage_taken = 0 

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        self.draw_health_bar(screen)
        
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, 50, 10))  
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, 50 * (self.health / 5), 10))  

    def touch(self):
        self.x = 0
        self.y = w_height - self.height
        self.is_jump = False
        self.jump_count = 10

class projectile():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class enemy():
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = 3
        self.path = [x, end]
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 10
        self.visible = True
        
    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if self.vel > 0:
                screen.blit(moveRight[self.walkCount//3], (self.x, self.y))
            else:
                screen.blit(moveLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
            self.hit = pygame.Rect(self.hitbox)
            pygame.draw.rect(screen, "grey", (self.hitbox[0], self.hitbox[1] + 3, 50, 10), 0)
            pygame.draw.rect(screen, "green", (self.hitbox[0], self.hitbox[1] + 3, 50 - (5.5 + (9 - self.health)), 10), 0)
                 
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    
    def touch(self):
        hitsound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

def DrawInGameloop():
    screen.blit(bg_img, (0, 0))
    clock.tick(25)
    text = font.render("Score : " + str(score), 4, "white")
    screen.blit(text, (0, 10))
    soldier.draw(screen)
    for enemy_inst in enemies:
        enemy_inst.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()

soldier = player(210, 435, 64, 64)
bullets = []
enemies = []
shoot = 0

enemy_spawn_time = 5000  
last_spawn_time = pygame.time.get_ticks()
spawn_rate_multiplier = 1  
next_double_time = pygame.time.get_ticks() + 30000 

done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= enemy_spawn_time:
        for _ in range(spawn_rate_multiplier):
            new_enemy = enemy(0, w_height - 64, 64, 64, w_width)
            enemies.append(new_enemy)
        last_spawn_time = current_time

    if current_time >= next_double_time:
        spawn_rate_multiplier *= 2
        next_double_time = current_time + 30000  
    for enemy_inst in enemies:
        if enemy_inst.visible and soldier.hit.colliderect(enemy_inst.hit):
            soldier.damage_taken += 0.25  
            hurtsound.play()
            if soldier.damage_taken >= 1:  
                soldier.health -= 1
                soldier.damage_taken = 0  

            if soldier.health <= 0:
                print("Soldier is dead!")
                done = False  
                
    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0
    
    for bullet in bullets[:]: 
   
        for enemy_inst in enemies:
            if enemy_inst.visible:
                if bullet.y - bullet.radius < enemy_inst.hitbox[1] + enemy_inst.hitbox[3] and bullet.y + bullet.radius > enemy_inst.hitbox[1]:
                    if bullet.x + bullet.radius > enemy_inst.hitbox[0] and bullet.x - bullet.radius < enemy_inst.hitbox[0] + enemy_inst.hitbox[2]:
                        if bullet in bullets:
                            bullets.remove(bullet) 
                        score += 1
                        enemy_inst.touch()
                        
        bullet.x += bullet.vel  
        if bullet.x < 0 or bullet.x > w_width:  
            if bullet in bullets:
                bullets.remove(bullet) 

    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and shoot == 0:
        bulletsound.play()
        direction = 1 if soldier.right else -1
        if len(bullets) < 5:
            bullets.append(projectile((soldier.x + soldier.width // 2), (soldier.y + soldier.height // 2), 6, "black", direction))
        shoot = 1
    if keys[pygame.K_LEFT] and soldier.x > 0:
        soldier.x -= soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:
        soldier.x += soldier.vel
        soldier.right = True
        soldier.left = False
        soldier.standing = False
    else:
        soldier.standing = True
        soldier.walkCount = 0
    if not soldier.is_jump:
        if keys[pygame.K_UP]:
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.jump_count >= -10:
            neg = 1 if soldier.jump_count >= 0 else -1
            soldier.y -= (soldier.jump_count ** 2) * 0.5 * neg
            soldier.jump_count -= 1
        else:
            soldier.is_jump = False
            soldier.jump_count = 10
    
    DrawInGameloop()

pygame.quit()
