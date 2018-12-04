import pygame


class Keyboard(object):

    def __init__(self):
        pygame.init()

    def terminate(self):
        pygame.quit()

    def get_key(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_k]:
            return 12
        if keys[pygame.K_j]:
            return 11
        if keys[pygame.K_u]:
            return 10
        if keys[pygame.K_h]:
            return 9
        if keys[pygame.K_y]:
            return 8
        if keys[pygame.K_g]:
            return 7
        if keys[pygame.K_t]:
            return 6
        if keys[pygame.K_f]:
            return 5
        if keys[pygame.K_d]:
            return 4
        if keys[pygame.K_e]:
            return 3
        if keys[pygame.K_s]:
            return 2
        if keys[pygame.K_w]:
            return 1
        if keys[pygame.K_a]:
            return 0
        return None
