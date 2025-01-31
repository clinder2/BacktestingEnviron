import datetime
import queue

from abc import ABCMeta, abstractmethod

from Event import fillEvent, OrderEvent

class ExecutionHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError("error")
    
class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self, events):
        self.events = events
    
    def execute_order(self, event):
        if event.type == 'ORDER':
            fill_event = fillEvent(datetime.datetime.now(), event.symbol, 'ARCA', event.quantity, event.direction, None)
            self.events.put(fill_event)