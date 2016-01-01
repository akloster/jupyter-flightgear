import bokeh
from bokeh.plotting import *
from bokeh_update import replace_bokeh_data_source
import pandas as pd

def timedelta_to_seconds(ts):
    """ Convert the TimedeltaIndex of a pandas.Series into a numpy
        array of seconds. """
    seconds = ts.index.values.astype(float)
    seconds -= seconds[-1]
    seconds /= 1e9
    return seconds

class TimeSeriesDemo(object):
    """ Demonstrate realtime plotting of time series data. """
    def __init__(self):
        self.minutes_back = 5

        # airspeed vs groundspeed plot
        self.airspeed_source = ColumnDataSource(dict(time=[], airspeed=[]))
        self.groundspeed_source = ColumnDataSource(dict(time=[], groundspeed=[]))
        self.ag_plot = figure(title="Airspeed/Groundspeed",
                      plot_width=600,
                      plot_height=200,
                      x_range=(-self.minutes_back*60,0),
                      y_range =(0,150),
                      tools=[])

        self.ag_plot.line(x="time", y="airspeed", source=self.airspeed_source, color="red",
                          legend="airspeed(kt)")
        self.ag_plot.line(x="time", y="groundspeed", source=self.groundspeed_source, color="blue",
                          legend="groundspeed(kt)")
        self.ag_plot.legend.orientation ="top_left"


        # Altitude above ground in feet
        self.altitude_source = ColumnDataSource(dict(time=[], altitude=[]))

        self.altitude_plot = figure(title= "Altitude",
                      plot_width=600,
                      plot_height=200,
                      x_range=(-self.minutes_back*60,0),
                      y_range =(0,4000),
                      tools=[])

        self.altitude_plot.line(x="time", y="altitude",
                      source=self.altitude_source,
                      color="black",
                      legend="altitude above ground(ft)")
        self.altitude_plot.legend.orientation ="top_left"

    def update(self, airspeed, groundspeed, altitude, transmit=True):
        ts_airspeed = airspeed.get_timeseries()
        ts_groundspeed = groundspeed.get_timeseries()


        minute_delta = pd.Timedelta("1 minute")
        b = ts_airspeed.index[-1]
        a = b - self.minutes_back*minute_delta

        ts_airspeed = ts_airspeed[a:b]
        ts_groundspeed = ts_groundspeed[a:b]


        self.airspeed_source.data["time"] = timedelta_to_seconds(ts_airspeed)
        self.airspeed_source.data["airspeed"] = ts_airspeed.values

        self.groundspeed_source.data["time"] =  timedelta_to_seconds(ts_groundspeed)
        self.groundspeed_source.data["groundspeed"] = ts_groundspeed.values

        ts_altitude = altitude.get_timeseries()[a:b]
        self.altitude_source.data['time'] = timedelta_to_seconds(ts_altitude)
        self.altitude_source.data['altitude'] = ts_altitude.values
        if transmit:
            replace_bokeh_data_source(self.airspeed_source)
            replace_bokeh_data_source(self.groundspeed_source)
            replace_bokeh_data_source(self.altitude_source)

class TimeSeriesDemo(object):
    def __init__(self):
        self.minutes_back = 5
        self.airspeed_source = ColumnDataSource(dict(time=[], airspeed=[]))
        self.groundspeed_source = ColumnDataSource(dict(time=[], groundspeed=[]))
        self.ag_plot = figure(title="Airspeed/Groundspeed",
                      plot_width=600,
                      plot_height=200,
                      x_range=(-self.minutes_back*60,0),
                      y_range =(0,150),
                      tools=[])
        
        self.ag_plot.line(x="time", y="airspeed", source=self.airspeed_source, color="red",
                          legend="airspeed")
        self.ag_plot.line(x="time", y="groundspeed", source=self.groundspeed_source, color="blue",
                          legend="groundspeed")
        self.ag_plot.legend.orientation ="top_left"
        self.altitude_source = ColumnDataSource(dict(time=[], altitude=[]))
        
        self.altitude_plot = figure(title= "Altitude",
                      plot_width=600,
                      plot_height=200,
                      x_range=(-self.minutes_back*60,0),
                      y_range =(0,4000),
                      tools=[])

        self.altitude_plot.line(x="time", y="altitude", source=self.altitude_source, color="black", legend="altitude above ground")        
        self.altitude_plot.legend.orientation ="top_left"
    def update(self, airspeed, groundspeed, altitude, transmit=True):
        ts_airspeed = airspeed.get_timeseries()
        ts_groundspeed = groundspeed.get_timeseries()

        minute_delta = pd.Timedelta("1 minute")
        b = ts_airspeed.index[-1]
        a = b - self.minutes_back*minute_delta

        ts_airspeed = ts_airspeed[a:b]
        ts_groundspeed = ts_groundspeed[a:b]


        self.airspeed_source.data["time"] = timedelta_to_seconds(ts_airspeed)
        self.airspeed_source.data["airspeed"] = ts_airspeed.values

        self.groundspeed_source.data["time"] =  timedelta_to_seconds(ts_groundspeed)
        self.groundspeed_source.data["groundspeed"] = ts_groundspeed.values

        ts_altitude = altitude.get_timeseries()[a:b]
        self.altitude_source.data['time'] = timedelta_to_seconds(ts_altitude)
        self.altitude_source.data['altitude'] = ts_altitude.values
        if transmit:
            replace_bokeh_data_source(self.airspeed_source)
            replace_bokeh_data_source(self.groundspeed_source)
            replace_bokeh_data_source(self.altitude_source)
