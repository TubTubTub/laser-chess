from data.constants import EventType

class GameEvent():
    def __init__(self, type, **kwargs):
        self.__dict__.update(kwargs)
        self.type = type

    @classmethod
    def create_event(event_cls, event_type, **kwargs):
        match event_type:
            case EventType.BOARD_CLICK:
                if 'coords' not in kwargs:
                    raise ValueError("Argument 'coords' required for BOARD_CLICK event (GameEvent.create_event)")
                
                return event_cls(event_type, coords=kwargs.get('coords'))

            case EventType.WIDGET_CLICK:
                raise NotImplementedError
                
            case EventType.EMPTY_CLICK:
                return event_cls(event_type)
            
            case EventType.UPDATE_PIECES:
                return event_cls(event_type)
            
            case EventType.REMOVE_PIECE:
                if 'coords_to_remove' not in kwargs:
                    raise ValueError("Argument 'coords_to_remove' required for REMOVE_PIECE event (GameEvent.create_event)")
                
                return event_cls(event_type, coords_to_remove=kwargs.get('coords_to_remove'))
            
            case _:
                raise ValueError('Invalid event type (GameEvent.create_event)')