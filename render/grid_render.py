import pygame
import numpy as np

from level.grid import Grid
from level.obstacle import Obstacle, pixel_size, colors

from math import *


class GridRender:
    """"
    To make things faster, a GridRender class is necessary : it will manage the calculus of each frame by taking a cache
    image already calculated
    """

    def __init__(self,
                 grid):
        """
        The GridRender __init__ function will generate an image of the grid that will be reused
        instead of being calculated again

        Parameters:
        grid (Grid): the grid Object to render
        """

        self.image = pygame.Surface((grid.size[0] * pixel_size, grid.size[1] * pixel_size))
        self.grid = grid

        # calculate base model of special obstacles (like color switcher that are animated)

        self.base_color_switcher = pygame.Surface((pixel_size, pixel_size), pygame.SRCALPHA)
        circle_surface = pygame.Surface((pixel_size, pixel_size), pygame.SRCALPHA)  # temporary surface

        # red arc
        pygame.draw.circle(circle_surface, colors["red"], (pixel_size / 2, pixel_size / 2),
                           pixel_size / 2,
                           0)
        self.base_color_switcher.blit(
            circle_surface.subsurface(pygame.Rect(pixel_size / 2, 0, pixel_size / 2, pixel_size / 2)),
            (pixel_size / 2, 0))
        # yellow arc
        pygame.draw.circle(circle_surface, colors["yellow"], (pixel_size / 2, pixel_size / 2),
                           pixel_size / 2, 0)
        self.base_color_switcher.blit(circle_surface.subsurface(pygame.Rect(0, 0, pixel_size / 2, pixel_size / 2)),
                                      (0, 0))
        # green arc
        pygame.draw.circle(circle_surface, colors["green"], (pixel_size / 2, pixel_size / 2),
                           pixel_size / 2, 0)
        self.base_color_switcher.blit(
            circle_surface.subsurface(pygame.Rect(0, pixel_size / 2, pixel_size / 2, pixel_size / 2)),
            (0, pixel_size / 2))
        # blue arc
        pygame.draw.circle(circle_surface, colors["blue"], (pixel_size / 2, pixel_size / 2),
                           pixel_size / 2,
                           0)

        self.base_color_switcher.blit(circle_surface.subsurface(
            pygame.Rect(pixel_size / 2, pixel_size / 2, pixel_size / 2, pixel_size / 2)),
            (pixel_size / 2, pixel_size / 2))

        # calculate everything and put it into image

        height, width = grid.size
        for i in range(height):
            for j in range(width):
                if grid.obstacles[i, j] is not None:
                    if grid.obstacles[i, j].start:  # draw the centralesupelec logo
                        pygame.draw.rect(self.image, colors["darkblue"],
                                         pygame.Rect(i * pixel_size,
                                                     j * pixel_size, pixel_size,
                                                     pixel_size))

                        pygame.draw.arc(self.image, colors["Volkswagen Taupe"],
                                        pygame.Rect(i * pixel_size + pixel_size / 8,
                                                    j * pixel_size + pixel_size / 8,
                                                    pixel_size / 2,
                                                    pixel_size / 2), pi / 2, 7 * pi / 4, 1)
                        pygame.draw.circle(self.image, colors["Volkswagen Taupe"], (

                            i * pixel_size + pixel_size * 11 / 32,
                            j * pixel_size + pixel_size * 11 / 32), 3)

                        pygame.draw.arc(self.image, grid.obstacles[i, j].color,
                                        pygame.Rect(i * pixel_size + pixel_size * 7 / 16,
                                                    j * pixel_size + pixel_size * 7 / 16,
                                                    pixel_size / 2,
                                                    pixel_size / 2), -pi / 2, 3 * pi / 4, 2)

                        pygame.draw.circle(self.image, grid.obstacles[i, j].color, (
                            i * pixel_size + pixel_size * 21 / 32,
                            j * pixel_size + pixel_size * 21 / 32), 3)
                    elif grid.obstacles[i, j].end:  # draw a star
                        pygame.draw.rect(self.image, colors["darkblue"],
                                         pygame.Rect(i * pixel_size,
                                                     j * pixel_size,
                                                     pixel_size, pixel_size))

                        L = []
                        for k in range(10):
                            if k % 2 == 0:
                                L += [
                                    (i * pixel_size + pixel_size / 2 + (pixel_size / 2) * np.cos(
                                        2 * pi * k / 10 - pi / 2),
                                     j * pixel_size + pixel_size / 2 + (pixel_size / 2) * np.sin(
                                         2 * pi * k / 10 - pi / 2))]
                            else:
                                L += [
                                    (i * pixel_size + pixel_size / 2 + (pixel_size / 5) * np.cos(
                                        2 * pi * k / 10 - pi / 2),
                                     j * pixel_size + pixel_size / 2 + (pixel_size / 5) * np.sin(
                                         2 * pi * k / 10 - pi / 2))]

                        pygame.draw.polygon(self.image, grid.obstacles[i, j].color, L, 0)
                    elif grid.obstacles[i, j].color_switcher:  # draw the color_switcher
                        pygame.draw.rect(self.image, colors["darkblue"],
                                         pygame.Rect(i * pixel_size, j * pixel_size, pixel_size, pixel_size))

                        self.image.blit(self.base_color_switcher, (i * pixel_size, j * pixel_size))

                        pygame.draw.circle(self.image, grid.obstacles[i, j].color,
                                           (i * pixel_size + pixel_size / 2, j * pixel_size + pixel_size / 2),
                                           pixel_size / 4, 0)
                    else:  # draw a colored not special obstacle
                        pygame.draw.rect(self.image, grid.obstacles[i, j].color,
                                         pygame.Rect(i * pixel_size, j * pixel_size, pixel_size, pixel_size))
                else:  # draw an empty tile
                    pygame.draw.rect(self.image, colors["darkblue"],
                                     pygame.Rect(i * pixel_size, j * pixel_size, pixel_size, pixel_size))

    def render(self, surface, time):
        """
        The render function will blit the already calculated 'self.image' to the surface you want to draw the grid on.
        There are no massive 'for' functions and lots of calls to pygame.draw anymore

        Parameters:
        surface (py_surface): The Pygame Surface you want to draw the grid on
        time (float): The relative time of the level
        """

        surface.blit(self.image, (0, 0))

        # only color switchers have to be updated
        height, width = self.grid.size
        for i in range(height):
            for j in range(width):
                if self.grid.obstacles[i, j] is not None:
                    if self.grid.obstacles[i, j].color_switcher:
                        pygame.draw.rect(self.image, colors["darkblue"],
                                         pygame.Rect(i * pixel_size, j * pixel_size, pixel_size, pixel_size))

                        rotated_surface = pygame.transform.rotate(self.base_color_switcher, time * 100)
                        rect = rotated_surface.get_rect(center=self.base_color_switcher.get_rect(
                            center=(i * pixel_size + pixel_size / 2, j * pixel_size + pixel_size / 2)).center)

                        surface.blit(rotated_surface, rect)

                        pygame.draw.circle(surface, colors["darkblue"],
                                           (i * pixel_size + pixel_size / 2, j * pixel_size + pixel_size / 2),
                                           pixel_size / 2.5, 0)

                        pygame.draw.circle(surface, self.grid.obstacles[i, j].color,
                                           (i * pixel_size + pixel_size / 2, j * pixel_size + pixel_size / 2),
                                           pixel_size / 4, 0)
