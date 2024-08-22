import pygame

class CustomSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        self.square_list = []
        pygame.sprite.Group.__init__(self)
    
    def draw_resized_finish(self):
        for sprite in self.sprites():
            sprite.draw_high_res_svg()

            if sprite.selected:
                sprite.draw_overlay()
            
    
    def update_squares_move(self, src, dest, piece_symbol, colour):
        self.square_list[src].clear_piece()
        self.square_list[dest].clear_piece()
        self.square_list[dest].set_colour(colour)
        self.square_list[dest].set_piece(piece_symbol)