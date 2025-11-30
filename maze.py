import pygame
from constants import *
import numpy as np
import time
class Maze:
    """Maze class that handles the game board and collision detection"""
    
    def __init__(self):
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT

        # 1️⃣ Créer le layout AVANT d'utiliser get_valid_positions()
        self.layout = np.array([
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ])

        self.portal_positions = []
        self.portails()

    def is_wall_collision(self, hitbox):
        """Check if the given rectangle collides with any walls"""
        # TODO: Écrire votre code ici
        centre_x, centre_y = hitbox.center

        
        col_center = int(centre_x // self.cell_width)
        row_center = int(centre_y // self.cell_height)

        for row in range(row_center - 1, row_center + 2):
            for col in range(col_center - 1, col_center + 2):
                if 0 <= row < self.height and 0 <= col < self.width:
                    if self.layout[row, col] == 1: 
                        wall_rect = pygame.Rect(
                            col * self.cell_width,
                            row * self.cell_height,
                            self.cell_width,
                            self.cell_height
                        )
                        if hitbox.colliderect(wall_rect):
                            return True
        return False
    
    def draw(self, screen):
        """Draw the maze on the screen"""
        
        for row in range(self.height):
            for col in range(self.width):
                if self.layout[row,col] == 1:  # Wall
                    x = col * self.cell_width
                    y = row * self.cell_height
                    wall_rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
                    pygame.draw.rect(screen, BLUE, wall_rect)
                    
                    # Add border for better visibility
                    pygame.draw.rect(screen, WHITE, wall_rect, 1)
        self.draw_portals(screen)
    def get_valid_positions(self):
        """Get all valid (non-wall) positions for placing objects"""
        valid_positions = []
        
        for row in range(self.height):
            for col in range(self.width):
                if self.layout[row,col] == 0:  # Empty space
                    x = col * self.cell_width + self.cell_width // 2
                    y = row * self.cell_height + self.cell_height // 2
                    valid_positions.append((x, y))

        return valid_positions

    def portails(self):
        valid_positions = self.get_valid_positions()

        if len(valid_positions) < 2:
            self.portal_positions = []
            return

        import random
        self.portal_positions = random.sample(valid_positions, 2)

    
    def draw_portals(self, screen):
        if len(self.portal_positions) != 2:
            return

        (x1, y1), (x2, y2) = self.portal_positions
        radius = self.cell_width // 3

        pygame.draw.circle(screen, ORANGE, (int(x1), int(y1)), radius, 4)
        pygame.draw.circle(screen, BLUE,   (int(x2), int(y2)), radius, 4)

    def portal_teleportation(self, obj):
        if len(self.portal_positions) != 2:
            return

        (x1, y1), (x2, y2) = self.portal_positions
        rect_obj = obj.get_rect()

        current_time = time.time()
        if current_time - obj.last_teleport_time < 0.3:
            return

        portal_rect1 = pygame.Rect(
            x1 - self.cell_width//3, y1 - self.cell_height//3,
            self.cell_width*2//3, self.cell_height*2//3
        )

        portal_rect2 = pygame.Rect(
            x2 - self.cell_width//3, y2 - self.cell_height//3,
            self.cell_width*2//3, self.cell_height*2//3
        )

        if rect_obj.colliderect(portal_rect1):
            obj.x = x2 - obj.width // 2
            obj.y = y2 - obj.height // 2
            obj.last_teleport_time = current_time

        elif rect_obj.colliderect(portal_rect2):
            obj.x = x1 - obj.width // 2
            obj.y = y1 - obj.height // 2
            obj.last_teleport_time = current_time
