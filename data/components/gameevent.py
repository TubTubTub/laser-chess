from data.constants import EventType

class GameEvent():
    def __init__(self):
        pass

    @classmethod
    def create_event(event_cls, event_type, **kwargs):
        match event_type:
            case EventType.BOARD_CLICK:
                if 'square_index' not in kwargs:
                    raise ValueError('Square index required for BOARD_CLICK event (GameEvent.create_event)')
                
                return event_cls(event_type, square_index=kwargs.get('square_index'))
            
            case EventType.PIECE_CLICK:
                raise NotImplementedError
            case EventType.WIDGET_CLICK:
                raise NotImplementedError
            case _:
                raise ValueError('Invalid event type (GameEvent.create_event)')