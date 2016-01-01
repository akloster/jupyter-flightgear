import numpy as np
import pandas as pd
import tornado
from tornado.websocket import websocket_connect
from tornado.httpclient import HTTPRequest
import json
import sys

def message(**kwargs):
    return json.dumps(kwargs)


class FlightGearProperty(object):
    """ Manages a property transmitted from FlightGear. """

    def __init__(self, node):
        self.node = node
        self.values = []
        self.indices = []

    def get_timeseries(self, tail_n=-1):
        """ Convert the captured values into a pandas.Series with a
            TimeDeltaIndex.
        """
        tail_n = min(len(self.values), 0)

        if tail_n>0:
            return pd.Series(self.values[:-tail_n], index=pd.to_timedelta(self.indices[:-tail_n], unit="s"))
        else:
            return pd.Series(self.values, index=pd.to_timedelta(self.indices, unit="s"))

    def update(self, data):
        """ Update the property with data from a websocket message. """
        v = data['value']
        data_type = data['type']
        if data_type == "double":
            v = float(v)
        elif data_type == "int":
            v = int(v)
        t = data["ts"]
        self.values.append(v)
        self.indices.append(float(t))


class FlightGearConnection(object):
    def __init__(self, host="localhost", port=9015):
        """ When FlightGear is run with the --httpd=PORT option, it serves a
            Webapplication, and also a Websocket URL to get, set and listen to
            all properties inside the Simulation.

            The FlightGearConnection handles the lifetime of such a connection.

            The IPython Kernel uses Tornado to run asynchronously, which allows
            us to communicate with websockets very nicely.
            """
        self.connected = False
        self.host = host
        self.port = port
        self.properties = {}

    def connect(self):
        self.connected = False
        request = HTTPRequest("ws://%s:%i/PropertyListener" % (self.host, self.port))
        self.future = websocket_connect(request, on_message_callback=self.on_message)
        self.future.add_done_callback(self.on_connected)

    def on_message(self, msg):
        if msg is None:
            return
        data = json.loads(msg)
        node = data['path']
        try:
            self.properties[node].update(data)
        except KeyError:
            # This should not happen
            print("%s not found" % node)

    def on_connected(self, *args, **kwargs):
        sys.stdout.flush()
        self.connected = True
        self.websocket = self.future.result()

        for node, prop in self.properties.items():
            self._add_listener(prop)

    def close(self):
        self.connected = False
        self.websocket.close()

    def _add_listener(self, prop):
        if self.connected:
            self.websocket.write_message(message(command="get", node=prop.node))
            self.websocket.write_message(message(command="addListener", node=prop.node))

    def listen(self, node):
        prop = FlightGearProperty(node)

        self.properties[node] = prop
        self._add_listener(prop)
        return prop
