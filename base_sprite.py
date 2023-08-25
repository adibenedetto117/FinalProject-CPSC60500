import pygame

class BaseSprite(pygame.sprite.Sprite):

    """
    BaseSprite class for handling sprite animations for different states.
    
    Attributes:
        current_frame (int): The index of the current animation frame.
        animation_speed (int): How quickly to cycle through animation frames.
        state (str): Current state the sprite is in (e.g., 'idle', 'runRight', etc.)
        idle (list): Animation frames for idle state.
        runRight (list): Animation frames for running right.
        runLeft (list): Animation frames for running left.
        jump (list): Animation frames for jumping.
        fall (pygame.Surface): Single frame for falling.
        land (pygame.Surface): Single frame for landing.
        flying (pygame.Surface): Single frame for flying.
    """

    def __init__(self, sprite_idle_frames, sprite_runRight_frames, sprite_runLeft_frames, sprite_jump_frames, sprite_fall_frame, sprite_land_frame, robot_flying_frame):

        """
        Initialize the BaseSprite object.
        
        Parameters:
            sprite_idle_frames (list): List of frames for idle animation.
            sprite_runRight_frames (list): List of frames for running right animation.
            sprite_runLeft_frames (list): List of frames for running left animation.
            sprite_jump_frames (list): List of frames for jump animation.
            sprite_fall_frame (pygame.Surface): Single frame for falling.
            sprite_land_frame (pygame.Surface): Single frame for landing.
            robot_flying_frame (pygame.Surface): Single frame for flying.
        """

        super().__init__()

        self.current_frame = 0
        self.animation_speed = 6
        self.state = 'idle'

        # Animation frames
        self.idle = sprite_idle_frames
        self.runRight = sprite_runRight_frames
        self.runLeft = sprite_runLeft_frames
        self.jump = sprite_jump_frames
        self.fall = sprite_fall_frame
        self.land = sprite_land_frame
        self.flying = robot_flying_frame

    def update_animation(self):
        """
        Update the animation frame based on the sprite's current state.
        """
        current_animation = getattr(self, self.state)

        if self.animation_speed <= 0:
            self.animation_speed = 1  # Prevent division by zero

    # Only update frame every few game ticks, based on animation speed
        if pygame.time.get_ticks() % self.animation_speed == 0:
            self.current_frame += 1

        if isinstance(current_animation, list):
            if self.current_frame >= len(current_animation):
                self.current_frame = 0

    def render(self, screen):
        """
        Render the sprite on the screen based on its current animation frame.
        
        Parameters:
            screen (pygame.Surface): The pygame surface on which to render the sprite.
        """
        try:
            current_animation = getattr(self, self.state)
            if isinstance(current_animation, list):
                screen.blit(current_animation[self.current_frame], (self.rect.x, self.rect.y))
            else:
                screen.blit(current_animation, (self.rect.x, self.rect.y))
        except:
            self.current_frame = 0
