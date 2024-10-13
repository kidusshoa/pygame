import pygame
pygame.init()

screen = pygame.display.set_mode((300,300))
screen.fill("white")
pygame.display.set_caption("Drawing shapes on surface")

pygame.draw.line(screen, "black", (0,0), (300, 300), 5)
pygame.draw.line(screen, "orange", True, [(100,100), (200,100), (100,200)], 4)

done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    
    pygame.display.flip()