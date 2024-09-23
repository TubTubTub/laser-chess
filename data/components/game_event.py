from data.constants import EventType

class GameEvent():
    def __init__(self, type, **kwargs):
        self.__dict__.update(kwargs)
        self.type = type

    @classmethod
    def create_event(event_cls, event_type, **kwargs):
        match event_type:
            case EventType.BOARD_CLICK:
                coords = kwargs.get('coords')
                if coords is None:
                    raise ValueError("Argument 'coords' required for BOARD_CLICK event (GameEvent.create_event)")
                
                return event_cls(event_type, coords=coords)

            case EventType.WIDGET_CLICK:
                return event_cls(event_type)
                
            case EventType.EMPTY_CLICK:
                return event_cls(event_type)
            
            case EventType.UPDATE_PIECES:
                return event_cls(event_type)
            
            case EventType.REMOVE_PIECE:
                coords_to_remove = kwargs.get('coords_to_remove')
                if coords_to_remove is None:
                    raise ValueError("Argument 'coords_to_remove' required for REMOVE_PIECE event (GameEvent.create_event)")
                
                return event_cls(event_type, coords_to_remove=coords_to_remove)
            
            case EventType.ROTATE_PIECE:
                rotation_direction = kwargs.get('rotation_direction')
                if rotation_direction is None:
                    raise ValueError("Argument 'rotation_direction' required for REMOVE_PIECE event (GameEvent.create_event)")

                return event_cls(event_type, rotation_direction=rotation_direction)

            case EventType.SET_LASER:
                laser_path = kwargs.get('laser_path')
                active_colour = kwargs.get('active_colour')
                if (laser_path is None) or (active_colour is None):
                    raise ValueError("Argument 'laser_path' required for REMOVE_PIECE event (GameEvent.create_event)")
                
                return event_cls(event_type, laser_path=laser_path, active_colour=active_colour)
            
            case _:
                raise ValueError('Invalid event type (GameEvent.create_event)')