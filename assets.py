import pygame
from core_functions import *

ROBOT_WIDTH, ROBOT_HEIGHT = [64,64]

def resize_animation(frames,width,height):
    """
    Resizes a list of pygame images to the given dimensions.

    Parameters:
        frames (list): List of pygame.Surface objects to be resized.
        width (int): The width to resize the image to.
        height (int): The height to resize the image to.

    Returns:
        list: A list of resized pygame.Surface objects.
    """
    fframes = []
    for frame in frames:
        resized_image = pygame.transform.scale(frame, (width, height))
        fframes.append(resized_image)
    return fframes

def background_assets():
    """
    Loads the images used for the background from the file system.

    No Parameters.

    Returns:
        tuple: A tuple containing pygame.Surface objects for top floor tiles,
        bottom floor tiles, desks, stands, and background images.
    """
    top_floor_tiles = pygame.image.load("assets/Tiles/tile_2_2.png").convert_alpha()
    bottom_floor_tiles = pygame.image.load("assets/Tiles/tile_0_4.png").convert_alpha()
    desks = pygame.image.load("assets/Lab Items/862-0.png").convert_alpha()
    stands = pygame.image.load("assets/Lab Items/907-0.png").convert_alpha()
    background_images = pygame.image.load("assets/Backgrounds/820-0.png").convert_alpha()
    return top_floor_tiles, bottom_floor_tiles,desks,stands,background_images

def background_animation_assets():
    """
    Loads and resizes the animated background assets.

    No Parameters.

    Returns:
        tuple: A tuple containing lists of pygame.Surface objects for each rotating and teleporting animation.
    """
    rotatingOBJ_frames = resize_animation([pygame.image.load(f"assets/Backgrounds/animation/rotating/tile_{i}.png").convert_alpha() for i in range(7)], 150,150)
    teleporter_frames =  resize_animation([pygame.image.load(f"assets/Backgrounds/animation/teleporter/tile_{i}.png").convert_alpha() for i in range(7)], 150, 150)
    return rotatingOBJ_frames, teleporter_frames

def robot_animation_assets():
    """
    Loads and resizes the robot-related animation assets.

    No Parameters.

    Returns:
        tuple: A tuple containing lists of pygame.Surface objects for each robot animation frame.
    """

    # Your code here
    blue_explosion_frames = resize_animation([pygame.image.load(f"assets/Robot/Blue_explosion/tile_{i}.png").convert_alpha() for i in range(4)],ROBOT_WIDTH,ROBOT_HEIGHT)

    # Robot Animations
    robot_idle_frames = resize_animation([pygame.image.load(f"assets/Robot/Idle/tile_{i}.png").convert_alpha() for i in range(5)],ROBOT_WIDTH,ROBOT_HEIGHT)
    robot_runRight_frames = resize_animation([pygame.image.load(f"assets/Robot/Run/tile_{i}.png").convert_alpha() for i in range(3)],ROBOT_WIDTH,ROBOT_HEIGHT)
    robot_runLeft_frames = [pygame.transform.flip(img, True, False) for img in robot_runRight_frames]
    robot_jump_frames = resize_animation([pygame.image.load(f"assets/Robot/Jump/tile_{i}.png").convert_alpha() for i in range(2)],ROBOT_WIDTH,ROBOT_HEIGHT)
    robot_fall_frame =  pygame.transform.scale(pygame.image.load("assets/Robot/Falling/falling.png").convert_alpha(), (ROBOT_WIDTH,ROBOT_HEIGHT))
    robot_land_frame = pygame.transform.scale(pygame.image.load("assets/Robot/Land/tile_0_2.png").convert_alpha(), (ROBOT_WIDTH,ROBOT_HEIGHT))
    robot_flying_frame = pygame.transform.scale(pygame.image.load("assets/Robot/flying/tile_1.png").convert_alpha(), (ROBOT_WIDTH,ROBOT_HEIGHT))

    return robot_flying_frame, blue_explosion_frames, robot_idle_frames,robot_runRight_frames,robot_runLeft_frames, robot_jump_frames,robot_fall_frame,robot_land_frame