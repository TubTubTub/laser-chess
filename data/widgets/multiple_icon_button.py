import pygame
from data.constants import WidgetState, LOCKED_BLUE_BUTTON_COLOURS, LOCKED_RED_BUTTON_COLOURS, RED_BUTTON_COLOURS, BLUE_BUTTON_COLOURS
from data.components.custom_event import CustomEvent
from data.widgets.bases.circular import _Circular
from data.widgets.icon_button import IconButton
from data.widgets.bases.box import _Box

class MultipleIconButton(_Circular, IconButton):
	def __init__(self, icons_dict, **kwargs):
		_Circular.__init__(self, items_dict=icons_dict)
		IconButton.__init__(self, icon=self.current_item, **kwargs)

		self._fill_colour_copy = self._fill_colour
		
		self._locked = None
	
	def set_locked(self, is_locked):
		self._locked = is_locked
		if self._locked:
			r, g, b, a  = pygame.Color(self._fill_colour_copy).rgba
			if self._box_colours_dict == BLUE_BUTTON_COLOURS:
				_Box.__init__(self, box_colours=LOCKED_BLUE_BUTTON_COLOURS)
			elif self._box_colours_dict == RED_BUTTON_COLOURS:
				_Box.__init__(self, box_colours=LOCKED_RED_BUTTON_COLOURS)
			else:
				self.initialise_new_colours((max(r + 50, 0), max(g + 50, 0), max(b + 50, 0), a))
		else:
			if self._box_colours_dict == LOCKED_BLUE_BUTTON_COLOURS:
				_Box.__init__(self, box_colours=BLUE_BUTTON_COLOURS)
			elif self._box_colours_dict == LOCKED_RED_BUTTON_COLOURS:
				_Box.__init__(self, box_colours=RED_BUTTON_COLOURS)
			else:
				self.initialise_new_colours(self._fill_colour_copy)

		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.set_state_colour(WidgetState.HOVER)
		else:
			self.set_state_colour(WidgetState.BASE)
	
	def set_next_icon(self):
		super().set_next_item()
		self._icon = self.current_item
		self.set_image()
		
	def process_event(self, event):
		widget_event = super().process_event(event)

		if widget_event:
			return CustomEvent(**vars(widget_event), data=self.current_key)