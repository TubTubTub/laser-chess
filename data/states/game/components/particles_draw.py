import pygame
from random import randint
from data.constants import ImageType
from data.utils.asset_helpers import get_perimeter_sample, get_vector, get_angle_between_vectors, get_next_corner
from data.states.game.components.piece_sprite import create_piece

class ParticlesDraw:
    def __init__(self, gravity=0.2, rotation=180, shrink=0.5, opacity=150):
        self._particles = [] # (image, image_copy, position, velocity, lifespan)
        self._glow_particles = []

        self._gravity = gravity
        self._rotation = rotation
        self._shrink = shrink
        self._opacity = opacity
    
    def fragment_image(self, image, number):
        image_size = image.get_rect().size
        center = image.get_rect().center
        corner_list = get_perimeter_sample(image_size, number)
        fragment_list = []
        
        corner_list.append(corner_list[0])

        for i in range(len(corner_list) - 1):
            vertex_1 = corner_list[i]
            vertex_2 = corner_list[i + 1]
            vector_1 = get_vector(center, vertex_1)
            vector_2 = get_vector(center, vertex_2)
            angle = get_angle_between_vectors(vector_1, vector_2)

            cropped_image = pygame.Surface(image_size, pygame.SRCALPHA)
            cropped_image.fill((0, 0, 0, 0))
            cropped_image.blit(image, (0, 0))

            corners_to_draw = None

            if vertex_1[0] == vertex_2[0] or vertex_1[1] == vertex_2[1]: # same side, touches no corners
                corners_to_draw = 4
            
            elif abs(vertex_1[0] - vertex_2[0]) == image_size[0] or abs(vertex_1[1] - vertex_2[1]) == image_size[1]: # opposite sides, touches two corners
                corners_to_draw = 2
                
            elif angle < 180: # touches one corner
                corners_to_draw = 3
            
            else: # touches three corners
                corners_to_draw
            
            corners_list = []
            for j in range(corners_to_draw):
                if len(corners_list) == 0:
                    corners_list.append(get_next_corner(vertex_2, image_size))
                else:
                    corners_list.append(get_next_corner(corners_list[-1], image_size))

            pygame.draw.polygon(cropped_image, (0, 0, 0, 0), (center, vertex_2, *corners_list, vertex_1))

            fragment_list.append(cropped_image)

        return fragment_list
    
    def add_captured_piece(self, piece, colour, rotation, position, size):
        piece_sprite = create_piece(piece, colour, rotation)
        piece_sprite.set_geometry((0, 0), size)
        piece_sprite.set_image(ImageType.LOW_RES)

        particles = self.fragment_image(piece_sprite.image, 5)

        for particle in particles:
            self.add_particle(particle, position)
    
    def add_sparks(self, radius, colour, position):
        for i in range(randint(10, 15)):
            velocity = [randint(-15, 15) / 10, randint(-20, 0) / 10]
            random_colour = [min(max(val + randint(-20, 20), 0), 255) for val in colour]
            self._particles.append([None, [radius, random_colour], [*position], velocity, 0])
    
    def add_particle(self, image, position):
        velocity = [randint(-15, 15) / 10, randint(-20, 0) / 10]

        self._particles.append([image, image.copy(), [*position], velocity, 0])

    def update(self):
        for i in range(len(self._particles) - 1, -1, -1):
            particle = self._particles[i]

            #update position
            particle[2][0] += particle[3][0]
            particle[2][1] += particle[3][1]

            #update lifespan
            self._particles[i][4] += 0.01

            if self._particles[i][4] >= 1:
                self._particles.pop(i)
                continue

            if isinstance(particle[1], pygame.Surface): # Draw surface
                # update velocity
                particle[3][1] += self._gravity
                
                # update size
                image_size = particle[1].get_rect().size
                end_size = ((1 - self._shrink) * image_size[0], (1 - self._shrink) * image_size[1])
                target_size = (image_size[0] - particle[4] * (image_size[0] - end_size[0]), image_size[1] - particle[4] * (image_size[1] - end_size[1]))

                # update rotation
                rotation = (self._rotation if particle[3][0] <= 0 else -self._rotation) * particle[4] 

                updated_image = pygame.transform.scale(pygame.transform.rotate(particle[1], rotation), target_size)
            
            elif isinstance(particle[1], list): # Draw circle
                # update size
                end_radius = (1 - self._shrink) * particle[1][0]
                target_radius = particle[1][0] - particle[4] * (particle[1][0] - end_radius)

                updated_image = pygame.Surface((target_radius * 2, target_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(updated_image, particle[1][1], (target_radius, target_radius), target_radius)

            # update opacity
            alpha = 255 - particle[4] * (255 - self._opacity)

            updated_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            
            particle[0] = updated_image
    
    def draw(self, surface):
        surface.blits([
            (particle[0], particle[2]) for particle in self._particles
        ])