import pygame


class Keyboard(object):

    def __init__(self):
        pygame.init()

    def terminate(self):
        pygame.quit()

    def update(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        #defaults
        self.quit = False
        self.octave_up = False
        self.octave_down = False
        # events
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.quit = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                self.octave_up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                self.octave_down = True
        # key
        self.key = None
        if keys[pygame.K_a]:
            self.key = 0
        if keys[pygame.K_w]:
            self.key = 1
        if keys[pygame.K_s]:
            self.key = 2
        if keys[pygame.K_e]:
            self.key = 3
        if keys[pygame.K_d]:
            self.key = 4
        if keys[pygame.K_f]:
            self.key = 5
        if keys[pygame.K_t]:
            self.key = 6
        if keys[pygame.K_g]:
            self.key = 7
        if keys[pygame.K_y]:
            self.key = 8
        if keys[pygame.K_h]:
            self.key = 9
        if keys[pygame.K_u]:
            self.key = 10
        if keys[pygame.K_j]:
            self.key = 11
        if keys[pygame.K_k]:
            self.key = 12
