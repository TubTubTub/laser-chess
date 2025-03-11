import pygame
from data.utils.enums import Colour, StatusText, Miscellaneous, ShaderType
from data.states.game.components.overlay_draw import OverlayDraw
from data.states.game.components.capture_draw import CaptureDraw
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.laser_draw import LaserDraw
from data.states.game.components.father import DragAndDrop
from data.helpers.bitboard_helpers import bitboard_to_coords
from data.helpers.board_helpers import screen_pos_to_coords
from data.states.game.widget_dict import GAME_WIDGETS
from data.components.custom_event import CustomEvent
from data.components.widget_group import WidgetGroup
from data.utils.event_types import GameEventType
from data.managers.window import window
from data.managers.audio import audio
from data.utils.assets import SFX

class GameView:
    def __init__(self, model):
        self._model = model
        self._hide_pieces = False
        self._selected_coords = None
        self._event_to_func_map = {
            GameEventType.UPDATE_PIECES: self.handle_update_pieces,
            GameEventType.SET_LASER: self.handle_set_laser,
            GameEventType.PAUSE_CLICK: self.handle_pause,
        }

        # Register model event handling with process_model_event()
        self._model.register_listener(self.process_model_event, 'game')

        # Initialise WidgetGroup with map of widgets
        self._widget_group = WidgetGroup(GAME_WIDGETS)
        self._widget_group.handle_resize(window.size)
        self.initialise_widgets()

        self._laser_draw = LaserDraw(self.board_position, self.board_size)
        self._overlay_draw = OverlayDraw(self.board_position, self.board_size)
        self._drag_and_drop = DragAndDrop(self.board_position, self.board_size)
        self._capture_draw = CaptureDraw(self.board_position, self.board_size)
        self._piece_group = PieceGroup()
        self.handle_update_pieces()

        self.set_status_text(StatusText.PLAYER_MOVE)

    @property
    def board_position(self):
        return GAME_WIDGETS['chessboard'].position

    @property
    def board_size(self):
        return GAME_WIDGETS['chessboard'].size

    @property
    def square_size(self):
        return self.board_size[0] / 10

    def initialise_widgets(self):
        """
        Run methods on widgets stored in GAME_WIDGETS dictionary to reset them.
        """
        GAME_WIDGETS['move_list'].reset_move_list()
        GAME_WIDGETS['move_list'].kill()
        GAME_WIDGETS['help'].kill()
        GAME_WIDGETS['tutorial'].kill()

        GAME_WIDGETS['scroll_area'].set_image()

        GAME_WIDGETS['chessboard'].refresh_board()

        GAME_WIDGETS['blue_piece_display'].reset_piece_list()
        GAME_WIDGETS['red_piece_display'].reset_piece_list()

    def set_status_text(self, status):
        """
        Sets text on status text widget.

        Args:
            status (StatusText): The game stage for which text should be displayed for.
        """
        match status:
            case StatusText.PLAYER_MOVE:
                GAME_WIDGETS['status_text'].set_text(f"{self._model.states['ACTIVE_COLOUR'].name}'s turn to move")
            case StatusText.CPU_MOVE:
                GAME_WIDGETS['status_text'].set_text("CPU thinking...") # CPU calculating a crazy move...
            case StatusText.WIN:
                if self._model.states['WINNER'] == Miscellaneous.DRAW:
                    GAME_WIDGETS['status_text'].set_text("Game is a draw! Boring...")
                else:
                    GAME_WIDGETS['status_text'].set_text(f"{self._model.states['WINNER'].name} won!")
            case StatusText.DRAW:
                GAME_WIDGETS['status_text'].set_text("Game is a draw! Boring...")

    def handle_resize(self):
        """
        Handles resizing of the window.
        """
        self._overlay_draw.handle_resize(self.board_position, self.board_size)
        self._capture_draw.handle_resize(self.board_position, self.board_size)
        self._piece_group.handle_resize(self.board_position, self.board_size)
        self._laser_draw.handle_resize(self.board_position, self.board_size)
        self._laser_draw.handle_resize(self.board_position, self.board_size)
        self._widget_group.handle_resize(window.size)

        if self._laser_draw.firing:
            self.update_laser_mask()

    def handle_update_pieces(self, event=None):
        """
        Callback function to update pieces after move.

        Args:
            event (GameEventType, optional): If updating pieces after player move, event contains move information. Defaults to None.
            toggle_timers (bool, optional): Toggle timers on and off for new active colour. Defaults to True.
        """
        piece_list = self._model.get_piece_list()
        self._piece_group.initialise_pieces(piece_list, self.board_position, self.board_size)

        if event:
            GAME_WIDGETS['move_list'].append_to_move_list(event.move_notation)
            GAME_WIDGETS['scroll_area'].set_image()
            audio.play_sfx(SFX['piece_move'])

        # If active colour is starting colour, as player always moves first
        if ['b', 'r'][self._model.states['ACTIVE_COLOUR']] == self._model.states['START_FEN_STRING'][-1]:
            self.set_status_text(StatusText.PLAYER_MOVE)
        else:
            self.set_status_text(StatusText.CPU_MOVE)

        if self._model.states['TIME_ENABLED']:
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'], True)
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'].get_flipped_colour(), False)

        if self._model.states['WINNER'] is not None:
            self.handle_game_end()

    def handle_game_end(self, play_sfx=True):
        self.toggle_timer(self._model.states['ACTIVE_COLOUR'], False)
        self.toggle_timer(self._model.states['ACTIVE_COLOUR'].get_flipped_colour(), False)

        if self._model.states['WINNER'] == Miscellaneous.DRAW:
            self.set_status_text(StatusText.DRAW)
        else:
            self.set_status_text(StatusText.WIN)

        if play_sfx:
            audio.play_sfx(SFX['sphinx_destroy_1'])
            audio.play_sfx(SFX['sphinx_destroy_2'])
            audio.play_sfx(SFX['sphinx_destroy_3'])

    def handle_set_laser(self, event):
        """
        Callback function to draw laser after move.

        Args:
            event (GameEventType): Contains laser trajectory information.
        """
        laser_result = event.laser_result

        # If laser has hit a piece
        if laser_result.hit_square_bitboard:
            coords_to_remove = bitboard_to_coords(laser_result.hit_square_bitboard)
            self._piece_group.remove_piece(coords_to_remove)

            if laser_result.piece_colour == Colour.BLUE:
                GAME_WIDGETS['red_piece_display'].add_piece(laser_result.piece_hit)
            elif laser_result.piece_colour == Colour.RED:
                GAME_WIDGETS['blue_piece_display'].add_piece(laser_result.piece_hit)

            # Draw piece capture GFX
            self._capture_draw.add_capture(
                laser_result.piece_hit,
                laser_result.piece_colour,
                laser_result.piece_rotation,
                coords_to_remove,
                laser_result.laser_path[0][0],
                self._model.states['ACTIVE_COLOUR']
            )

        self._laser_draw.add_laser(laser_result, self._model.states['ACTIVE_COLOUR'])
        self.update_laser_mask()

    def handle_pause(self, event=None):
        """
        Callback function for pausing timer.

        Args:
            event (None): Event argument not used.
        """
        is_active = not(self._model.states['PAUSED'])
        self.toggle_timer(self._model.states['ACTIVE_COLOUR'], is_active)

    def initialise_timers(self):
        """
        Initialises both timers with the correct amount of time and starts the timer for the active colour.
        """
        if self._model.states['TIME_ENABLED']:
            GAME_WIDGETS['blue_timer'].set_time(self._model.states['TIME'] * 60 * 1000)
            GAME_WIDGETS['red_timer'].set_time(self._model.states['TIME'] * 60 * 1000)
        else:
            GAME_WIDGETS['blue_timer'].kill()
            GAME_WIDGETS['red_timer'].kill()

        self.toggle_timer(self._model.states['ACTIVE_COLOUR'], True)

    def toggle_timer(self, colour, is_active):
        """
        Stops or resumes timer.

        Args:
            colour (Colour): Timer to toggle.
            is_active (bool): Whether to pause or resume timer.
        """
        if colour == Colour.BLUE:
            GAME_WIDGETS['blue_timer'].set_active(is_active)
        elif colour == Colour.RED:
            GAME_WIDGETS['red_timer'].set_active(is_active)

    def update_laser_mask(self):
        """
        Uses pygame.mask to create a mask for the pieces.
        Used for occluding the ray shader.
        """
        temp_surface = pygame.Surface(window.size, pygame.SRCALPHA)
        self._piece_group.draw(temp_surface)
        mask = pygame.mask.from_surface(temp_surface, threshold=127)
        mask_surface = mask.to_surface(unsetcolor=(0, 0, 0, 255), setcolor=(255, 0, 0, 255))

        window.set_apply_arguments(ShaderType.RAYS, occlusion=mask_surface)

    def draw(self):
        """
        Draws GUI and pieces onto the screen.
        """
        self._widget_group.update()
        self._capture_draw.update()

        self._widget_group.draw()
        self._overlay_draw.draw(window.screen)

        if self._hide_pieces is False:
            self._piece_group.draw(window.screen)

        self._laser_draw.draw(window.screen)
        self._drag_and_drop.draw(window.screen)
        self._capture_draw.draw(window.screen)

    def process_model_event(self, event):
        """
        Registered listener function for handling GameModel events.
        Each event is mapped to a callback function, and the appropiate one is run.

        Args:
            event (GameEventType): Game event to process.

        Raises:
            KeyError: If an unrecgonised event type is passed as the argument.
        """
        try:
            self._event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Game View (GameView.process_model_event):', event.type)

    def set_overlay_coords(self, available_coords_list, selected_coord):
        """
        Set board coordinates for potential moves overlay.

        Args:
            available_coords_list (list[tuple[int, int]], ...): Array of coordinates
            selected_coord (list[int, int]): Coordinates of selected piece.
        """
        self._selected_coords = selected_coord
        self._overlay_draw.set_selected_coords(selected_coord)
        self._overlay_draw.set_available_coords(available_coords_list)

    def get_selected_coords(self):
        return self._selected_coords

    def set_dragged_piece(self, piece, colour, rotation):
        """
        Passes information of the dragged piece to the dragging drawing class.

        Args:
            piece (Piece): Piece type of dragged piece.
            colour (Colour): Colour of dragged piece.
            rotation (Rotation): Rotation of dragged piece.
        """
        self._drag_and_drop.set_dragged_piece(piece, colour, rotation)

    def remove_dragged_piece(self):
        """
        Stops drawing dragged piece when user lets go of piece.
        """
        self._drag_and_drop.remove_dragged_piece()

    def convert_mouse_pos(self, event):
        """
        Passes information of what mouse cursor is interacting with to a GameController object.

        Args:
            event (pygame.Event): Mouse event to process.

        Returns:
            CustomEvent | None: Contains information what mouse is doing.
        """
        clicked_coords = screen_pos_to_coords(event.pos, self.board_position, self.board_size)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if clicked_coords:
                return CustomEvent.create_event(GameEventType.BOARD_CLICK, coords=clicked_coords)

            else:
                return None

        elif event.type == pygame.MOUSEBUTTONUP:
            if self._drag_and_drop.dragged_sprite:
                piece, colour, rotation = self._drag_and_drop.get_dragged_info()
                piece_dragged = self._drag_and_drop.remove_dragged_piece()
                return CustomEvent.create_event(GameEventType.PIECE_DROP, coords=clicked_coords, piece=piece, colour=colour, rotation=rotation, remove_overlay=piece_dragged)

    def add_help_screen(self):
        """
        Draw help overlay when player clicks on the help button.
        """
        self._widget_group.add(GAME_WIDGETS['help'])
        self._widget_group.handle_resize(window.size)

    def add_tutorial_screen(self):
        """
        Draw tutorial overlay when player clicks on the tutorial button.
        """
        self._widget_group.add(GAME_WIDGETS['tutorial'])
        self._widget_group.handle_resize(window.size)
        self._hide_pieces = True

    def remove_help_screen(self):
        GAME_WIDGETS['help'].kill()

    def remove_tutorial_screen(self):
        GAME_WIDGETS['tutorial'].kill()
        self._hide_pieces = False

    def process_widget_event(self, event):
        """
        Passes Pygame event to WidgetGroup to allow individual widgets to process events.

        Args:
            event (pygame.Event): Event to process.

        Returns:
            CustomEvent | None: A widget event.
        """
        return self._widget_group.process_event(event)