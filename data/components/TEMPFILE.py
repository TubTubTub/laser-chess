
        self._board_size = self.calculate_board_size(self.screen)
        self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)

def initialize_square_group(self):
    square_group = CustomSpriteGroup()

    for i in range(80):
        x = i % 10
        y = i // 10


        if (x + y) % 2 == 0:
            square = Square(index=(x,y), size=self._square_size, board_colour=(self.game_settings.primaryBoardColour), anchor_position=self._board_origin_position)
        else:
            square = Square(index=(x,y), size=self._square_size, board_colour=(self.game_settings.secondaryBoardColour), anchor_position=self._board_origin_position)

        square_group.add(square)
        square_group.square_list.append(square)

        blue_piece_symbol = self.bitboards.get_piece_on(square.to_bitboard(), Colour.BLUE)
        red_piece_symbol = self.bitboards.get_piece_on(square.to_bitboard(), Colour.RED)
        rotation = self.bitboards.get_rotation_on(square.to_bitboard())

        if (blue_piece_symbol):
            square.set_piece(piece_symbol=blue_piece_symbol, colour=Colour.BLUE, rotation=rotation)
        elif (red_piece_symbol):
            square.set_piece(piece_symbol=red_piece_symbol, colour=Colour.RED, rotation=rotation)
    return square_group

def handle_events(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        self._pressed_on_board = True
    if event.type == pygame.VIDEORESIZE:
        self._square_group.handle_resize_end()

def handle_click(self):
    mouse_position = pygame.mouse.get_pos()
    self.process_board_press(mouse_position)
    self._pressed_on_board = False


def draw_board(self):
    self._cursor.update()
    self._square_group.draw(self.screen)
    self.draw_laser()

def handle_resize(self):
    self._board_size = self.calculate_board_size(self.screen)
    self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)
    self._square_size = self._board_size[0] / 10
    self._square_group.handle_resize(new_size=self._square_size, new_position=self._board_origin_position)


def calculate_board_size(self, screen):
    '''Returns board size based on screen parameter'''
    screen_width, screen_height = screen.get_size()

    target_height = screen_height * 0.64
    target_width = target_height / 0.8

    return (target_width, target_height)

def calculate_board_position(self, screen, board_size):
    '''Returns required board starting position to draw on center of the screen'''
    screen_x, screen_y = screen.get_size()
    board_x, board_y = board_size

    x = screen_x / 2 - (board_x / 2)
    y = screen_y / 2 + (board_y / 2)

    return (x, y)

def process_board_press(self, mouse_position):
    clicked_square = self._cursor.select_square(mouse_position, self._square_group)

    if (clicked_square is None):
        self._selected_square = None
        self._square_group.remove_valid_square_overlays()
        
    elif self._selected_square is None:
        if (clicked_square.piece is None) or not (self.check_valid_src(clicked_square.to_bitboard())):
            return
        elif clicked_square.piece != Piece.SPHINX:
            self._selected_square = clicked_square
            valid_squares = self.return_valid_squares(clicked_square.to_bitboard())
            self._square_group.add_valid_square_overlays(valid_squares)
            self._square_group.draw_valid_square_overlays()

    else:
        valid_squares = self.return_valid_squares(self._selected_square.to_bitboard())

        if (clicked_square.to_bitboard() & valid_squares != EMPTY_BB):
            self.apply_move(self._selected_square, clicked_square)

        self._square_group.remove_valid_square_overlays()
        self._selected_square = None


    def notation_to_list_index(self, notation):
        if (len(notation) == 2) and (notation[0].upper() in File._member_names_) and (notation[1] in [str(rank.value + 1) for rank in Rank]):
            rank = int(notation[1]) - 1
            file = int(File[notation[0].upper()])
            return (rank * 10 + file)
        else:
            raise ValueError('Invalid input - cannot convert input into list index')