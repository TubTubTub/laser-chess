from data.constants import GameEventType, MenuEventType, SettingsEventType

required_args = {
    GameEventType.BOARD_CLICK: ['coords'],
    GameEventType.REMOVE_PIECE: ['coords_to_remove'],
    GameEventType.ROTATE_PIECE: ['rotation_direction'],
    GameEventType.SET_LASER: ['laser_path', 'active_colour'],
    SettingsEventType.COLOUR_CLICK: ['colour'],
    SettingsEventType.COLOUR_SLIDER_SLIDE: ['colour'],
    SettingsEventType.COLOUR_PICKER_CLICK: ['colour', 'colour_type'],
    SettingsEventType.COLOUR_BUTTON_CLICK: ['colour_type']
}

class CustomEvent():
    def __init__(self, type, **kwargs):
        self.__dict__.update(kwargs)
        self.type = type

    @classmethod
    def create_event(event_cls, event_type, **kwargs):
        if event_type in required_args:

            for required_arg in required_args[event_type]:
                if required_arg not in kwargs:
                    raise ValueError(f"Argument '{required_arg}' required for {event_type.name} event (GameEvent.create_event)")
            
            return event_cls(event_type, **kwargs)

        else:
            return event_cls(event_type)