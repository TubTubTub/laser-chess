from data.states.game.components.piece_group import CustomSpriteGroup
from archive.square import Square
from data.components.cursor import Cursor
from data.helpers.data_helpers import get_settings_json
self._cursor = Cursor()
self.game_settings = get_settings_json()
self._board_size = self.calculate_board_size(self.screen)
self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)

self._square_size = self._board_size[0] / 10
self._square_group = self.initialize_square_group()
self.game_settings = get_settings_json()

self._gui_elements = []


def fire_laser(self):
if self.bitboards.active_colour == Colour.BLUE:
    laser_colour = self.game_settings.laserColourBlue
else:
    laser_colour = self.game_settings.laserColourRed
laser = Laser(screen=self.screen, laser_colour=laser_colour, bitboards=self.bitboards)

captured_square, laser_shapes = laser.calculate_trajectory()
self._laser_shapes = laser_shapes
if captured_square:
    print('captured_square:')
    bb_helpers.print_bitboard(captured_square)
    print(captured_square)
    self.capture_piece(captured_square)

def draw_laser(self):
for shape, index in self._laser_shapes:
    position = (index[0] * self._square_size + self._board_origin_position[0], self._board_origin_position[1] - self._square_size * (index[1] + 1))
    pygame.draw.rect(self.screen, 'red', (position[0], position[1], shape.width, shape.height))
def rotate_piece(self, clockwise=True):
if self._selected_square is None:
    print('No square selected to rotate (board.py)!')
    return

src_rotation = self.bitboards.get_rotation_on(self._selected_square.to_bitboard())

if clockwise:
    self.apply_rotation(self._selected_square, src_rotation.get_clockwise())
else:
    self.apply_rotation(self._selected_square, src_rotation.get_anticlockwise())


rotate_piece_clockwise = partial(self.board.rotate_piece, clockwise=True)
rotate_piece_anticlockwise = partial(self.board.rotate_piece, clockwise=False)
self._gui_elements = {
    'label': Label(screen=screen, position=(10, 300), text="jamesdssdss", text_colour=(0, 0, 0), margin=15, label_colour=(20, 100, 1), border_radius=50, border_width=0),
    'clockwise_button': Button(screen=screen, position=(30, 10), text="clockwise", func=rotate_piece_clockwise, text_colour=(255, 0, 0), label_colour=(0, 255, 255), width=100, height=50),
    'anticlockwise_button': Button(screen=screen, position=(30, 100), text="anticlockwise", func=rotate_piece_anticlockwise, text_colour=(0, 0, 0), label_colour=(0, 255, 0), margin=50),
}


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
# def check_valid_src(self, src_square):
#     return (src_square & self.bitboards.combined_colour_bitboards[self.bitboards.active_colour]) != EMPTY_BB

def apply_move(self, move):
    piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)

    if piece_symbol is None:
        raise ValueError('Invalid move - no piece found on source square')
    elif piece_symbol == Piece.SPHINX:
        raise ValueError('Invalid move - sphinx piece is immovable')

    if move.move_type == MoveType.MOVE:
        possible_moves = self.get_valid_squares(move.src)
        if bb_helpers.is_occupied(move.dest, possible_moves) is False:
            raise ValueError('Invalid move - destination square is occupied')

        piece_rotation = self.bitboards.get_rotation_on(move.src)

        # self._square_group.update_squares_move(src_square.to_list_position(), dest_square.to_list_position(), piece_symbol, self.bitboards.active_colour, rotation)

        self.bitboards.update_move(move.src, move.dest)
        self.bitboards.update_rotation(move.src, move.dest, piece_rotation)

    elif move.move_type == MoveType.ROTATE:
        # src_bitboard = src_square.to_bitboard()
        # src_list_position = src_square.to_list_position()

        piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)
        piece_rotation = self.bitboards.get_rotation_on(move.src)

        if move.direction == RotationDirection.CLOCKWISE:
            new_rotation = piece_rotation.get_clockwise()
        elif move.direction == RotationDirection.ANTICLOCKISE:
            new_rotation = piece_rotation.get_anticlockwise()

        # self._square_group.update_squares_rotate(src_list_position, piece_symbol, self.bitboards.active_colour, new_rotation=new_rotation)
        self.bitboards.update_rotation(move.src, move.src, new_rotation)

    self.alert_listeners(GameEvent.create_event(EventType.UPDATE_PIECES))
    print(f'PLAYER MOVE: {self.bitboards.active_colour.name}')

def remove_piece(self, square_bitboard):
    self.bitboards.clear_square(square_bitboard, Colour.BLUE)
    self.bitboards.clear_square(square_bitboard, Colour.RED)

    # self._square_group.clear_square(square_bitboard)

    self._selected_square = None
    self._pressed_on_board = False
    self._paused = False

@property
def clicked(self):
    return self._pressed_on_board and not self._paused