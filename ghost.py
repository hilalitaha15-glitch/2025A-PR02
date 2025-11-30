import pygame
import random
from game_object import GameObject
from constants import *

class Ghost(GameObject):
    """Base Ghost class"""
    
    def __init__(self, x, y, color):
        super().__init__(x, y, int(CELL_WIDTH//2), int(CELL_HEIGHT//1.2), color)
        self.start_x = x
        self.start_y = y
        self.direction = random.randint(0, 3)
        self.speed = GHOST_SPEED
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.vulnerable_duration = 300  # frames
        self.step = "left"
        self.step_timer = 0
        self.last_RL_direction = 0
        self.x = x - self.width // 2
        self.y = y - self.height // 2

    def update(self, maze, pacman):
        """Update ghost position and state"""
        # Update vulnerable state
        if self.vulnerable:
            self.vulnerable_timer += 1
            if self.vulnerable_timer >= self.vulnerable_duration:
                self.vulnerable = False
                self.vulnerable_timer = 0
        
        # Update ghost animation
        self.step_timer += 1
        if self.step_timer >= 10:
            self.step = "right" if self.step == "left" else "left"
            self.step_timer = 0
        
        # Move ghost
        self.move(maze, pacman)
    
    def move(self, maze, pacman):
        """Basic ghost movement (random direction on collision)"""
        new_x, new_y, hitbox = self.get_next_position()
        
        # Check for collision with walls
        if maze.is_wall_collision(hitbox):
            # Change direction randomly
            self.direction = random.randint(0, 3)
        else:
            self.x = new_x
            self.y = new_y
    
    def get_next_position(self):
        """Get next position based on current direction"""
        new_x, new_y = self.x, self.y
        hitbox = None

        if self.direction in [0, 2]:  # Right or Left
            self.last_RL_direction = self.direction
        
        # TODO: Écrire votre code ici
        if self.direction == 0:  
            new_x += self.speed
        elif self.direction == 1:  
            new_y += self.speed
        elif self.direction == 2:  
            new_x -= self.speed
        elif self.direction == 3:  
            new_y -= self.speed
        hitbox = pygame.Rect(new_x, new_y, self.width, self.height)

        return new_x, new_y, hitbox
            
    def draw(self, screen):
        """Load ghost image"""
        # TODO: Écrire votre code ici
        if self.vulnerable:
            img = "imgs/weak_ghost.png"
        else:
            if self.color == "red":
                img = "imgs/red_ghost.png"
            elif self.color == "pink":
                img = "imgs/pink_ghost.png"
            elif self.color == "blue":
                img = "imgs/blue_ghost.png"
            elif self.color == "orange":
                img = "imgs/orange_ghost.png"
            else:
                img = "imgs/red_ghost.png" 

        image = pygame.image.load(img)
        image = pygame.transform.scale(image, (self.width, self.height))

        if self.last_RL_direction == 2:  
            image = pygame.transform.flip(image, True, False)
        
        if self.step == "right":
            angle = 10
        else:
            angle = -10

        image = pygame.transform.rotate(image, angle)

        screen.blit(image, (self.x, self.y))
    
    def make_vulnerable(self):
        """Make the ghost vulnerable to being eaten"""
        self.vulnerable = True
        self.vulnerable_timer = 0
    
    def reset_position(self):
        """Reset ghost to starting position"""
        self.x = self.start_x - self.width // 2
        self.y = self.start_y - self.height // 2
        self.vulnerable = False
        self.vulnerable_timer = 0

class RedGhost(Ghost):
    """Red ghost - aggressive, chases Pacman directly"""
    
    def __init__(self, x, y, color="red"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Aggressive movement - chase Pacman directly"""
        if self.vulnerable:
            # Run away from Pacman when vulnerable
            self.flee_from_pacman(maze, pacman)
        else:
            # Chase Pacman
            self.chase_pacman(maze, pacman)
    
    def chase_pacman(self, maze, pacman):
        """Move towards Pacman"""
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici
        dx = pacman_x - self.x
        dy = pacman_y - self.y

        if abs(dx) >= abs(dy):
            self.direction = 0 if dx > 0 else 2
        else:
            self.direction = 1 if dy > 0 else 3

        new_x, new_y, hitbox = self.get_next_position()
        if hitbox is None:
            hitbox = pygame.Rect(new_x, new_y, self.width, self.height)

        if maze.is_wall_collision(hitbox):
            self.direction = random.randint(0, 3)
            new_x, new_y, hitbox = self.get_next_position()
            if hitbox is None:
                hitbox = pygame.Rect(new_x, new_y, self.width, self.height)
            if maze.is_wall_collision(hitbox):
                return

        self.x = new_x
        self.y = new_y

    def flee_from_pacman(self, maze, pacman):
        """Run away from Pacman when vulnerable"""
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici
        dx = pacman_x - self.x
        dy = pacman_y - self.y

       
        if abs(dx) >= abs(dy):
            
            self.direction = 2 if dx > 0 else 0  
        else:
           
            self.direction = 3 if dy > 0 else 1  

        new_x, new_y, hitbox = self.get_next_position()

        if maze.is_wall_collision(hitbox):
            self.direction = random.randint(0, 3)
            new_x, new_y, hitbox = self.get_next_position()
            if maze.is_wall_collision(hitbox):
                return  

        self.x = new_x
        self.y = new_y

class PinkGhost(Ghost):
    """Pink ghost - tries to ambush Pacman"""

    def __init__(self, x, y, color="pink"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Ambush movement - try to get ahead of Pacman"""
        if self.vulnerable:
            super().move(maze, pacman)  
        else:
            self.ambush_pacman(maze, pacman)

    def ambush_pacman(self, maze, pacman):
        """Try to position ahead of Pacman"""
    
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici

class BlueGhost(Ghost):
    """Blue ghost - patrol behavior"""

    def __init__(self, x, y, color="blue"):
        super().__init__(x, y, color)
        self.patrol_timer = 0
        self.patrol_duration = 120
    
    def move(self, maze, pacman):
        """Patrol movement - changes direction periodically"""
        self.patrol_timer += 1
        
        # TODO: Écrire votre code ici

class OrangeGhost(RedGhost):
    """Orange ghost - mixed behavior"""

    def __init__(self, x, y, color="orange"):
        super().__init__(x, y, color)
        self.behavior_timer = 0
        self.chase_mode = True
        self.behavior_duration = 180  # frames
    
    def move(self, maze, pacman):
        """Mixed behavior - alternates between chasing and fleeing"""
        self.behavior_timer += 1
        
        # TODO: Écrire votre code ici


ghosts_dict = {
            "red": RedGhost,
            "pink": PinkGhost,
            "blue": BlueGhost,
            "orange": OrangeGhost
        }
