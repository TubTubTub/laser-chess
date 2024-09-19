from data.constants import EventType

class GameEvent():
    def __init__(self, event_type, **kwargs):
        self.__dict__.update(kwargs)
        self.event_type = event_type

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
            case _:
                raise ValueError('Invalid event type (GameEvent.create_event)')