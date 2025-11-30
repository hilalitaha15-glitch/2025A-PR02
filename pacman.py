import pygame
import math
from game_object import GameObject
from constants import *

class Pacman(GameObject):
    """Pacman player class"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CELL_WIDTH//1.8, CELL_HEIGHT//1.8, YELLOW)
        self.start_x = x
        self.start_y = y
        self.direction = 0  # 0=right, 1=down, 2=left, 3=up
        self.next_direction = 0
        self.speed = PACMAN_SPEED
        self.mouth_open = True
        self.mouth_timer = 0
        self.x = x - self.width // 2
        self.y = y - self.height // 2

    def handle_input(self, key):
        """Handle keyboard input for movement"""
        # TODO: Écrire votre code ici
        if key == pygame.K_RIGHT:
            self.next_direction = 0
        elif key == pygame.K_DOWN:
            self.next_direction = 1
        elif key == pygame.K_LEFT:
            self.next_direction = 2
        elif key == pygame.K_UP:
            self.next_direction = 3

    def update(self, maze):
        """Update Pacman's position and state"""
        # Update mouth animation
        self.mouth_timer += 1
        if self.mouth_timer >= 10:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
        
        # Get next position based on next_direction
        new_x, new_y, hitbox = self.get_next_position()

        # Check if there is collision with a wall
        if not maze.is_wall_collision(hitbox):
            self.direction = self.next_direction
            self.x = new_x
            self.y = new_y

    def get_next_position(self):
        """
        Get the next position based on direction

        The hitbox will be used to detect collisions before moving.
        Returns new_x, new_y, hitbox
        """
        new_x, new_y = self.x, self.y
        hitbox = None

        # TODO: Écrire votre code ici

        if self.next_direction == 0:  
            new_x += self.speed
        elif self.next_direction == 1:  
            new_y += self.speed
        elif self.next_direction == 2:  
            new_x -= self.speed
        elif self.next_direction == 3:  
            new_y -= self.speed
        hitbox = pygame.Rect(new_x, new_y, self.width, self.height)
        return new_x, new_y, hitbox
    
    def draw(self, screen):
        """Draw Pacman with mouth animation"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        radius = self.width // 2

        # TODO: Écrire votre code ici
        # Draw Pacman body
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
        if self.direction == 0:     
            angle_milieu = 0
        elif self.direction == 1:    
            angle_milieu = 90
        elif self.direction == 2:   
            angle_milieu = 180
        else:                       
            angle_milieu = 270
        angle_bouche = 40  

        a1 = math.radians(angle_milieu - angle_bouche / 2)
        a2 = math.radians(angle_milieu + angle_bouche / 2)

        p1 = (center_x, center_y)
        p2 = (center_x + radius * math.cos(a1),
                center_y - radius * math.sin(a1))
        p3 = (center_x + radius * math.cos(a2),
                center_y - radius * math.sin(a2))

        pygame.draw.polygon(screen, BLACK, [p1, p2, p3])

        # Draw Pacman eye
        eye_offset = radius // 2
        eye_x, eye_y = center_x, center_y

        if self.direction == 0:     
            eye_x = center_x + eye_offset // 2
            eye_y = center_y - eye_offset // 2
        elif self.direction == 1:   
            eye_x = center_x + eye_offset // 2
            eye_y = center_y + eye_offset // 4
        elif self.direction == 2:    
            eye_x = center_x - eye_offset // 2
            eye_y = center_y - eye_offset // 2
        elif self.direction == 3:   
            eye_x = center_x - eye_offset // 2
            eye_y = center_y - eye_offset

        pygame.draw.circle(screen, BLACK, (int(eye_x), int(eye_y)), radius // 6)

    def reset_position(self):
        """Reset Pacman to starting position"""
        self.x = self.start_x - self.width // 2
        self.y = self.start_y - self.height // 2
        self.direction = 0
        self.next_direction = 0
