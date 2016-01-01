from ipywidgets.widgets import HTML, Button
from tornado.ioloop import IOLoop
from IPython import display
import time
from traitlets import Bool

class LoopDecorator(object):
    """ Runs the wrapped function in a certain interval until the user presses
        the stop button. """
    def __init__(self, button, interval=1.0):
        self.button = button
        self.interval = interval
        
    def __call__(self, func):
        display.display(self.button)
        self.last_time = None
        self.wrapped = func
        self.iterate()
        return None
    
    def iterate(self):
        if self.button.clicked:
            return
        loop = IOLoop.current()
        t = time.time()
        self.wrapped()
        wait = self.interval
        wait = min(self.interval - time.time()+t , wait)
        wait = max(0.01, wait)
        wait = min(self.interval, wait)
        loop.call_later(wait, self.iterate)


class StopButton(Button):
    """ A modified Button which as a "clicked" Attribute. """
    clicked = Bool(False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked = False
        self.on_click(self._on_click)
    def _on_click(self, *args, **kwargs):
        self.disabled = True
        self.clicked = True

    def loop(self, interval=1.0):
        """ Returns a loop decorator with this button. """
        decorator = LoopDecorator(self, interval)
        return decorator


