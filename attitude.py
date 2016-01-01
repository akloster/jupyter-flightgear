import bokeh
import math
from bokeh.plotting import *
from bokeh_update import replace_bokeh_data_source


class AttitudeIndicator(object):
    def __init__(self, width=400, height=400):
        patch_source = ColumnDataSource(dict(x=[], y=[]))

        line_source = ColumnDataSource(dict(x=[], y=[], width=[]))

        self.patch_source = patch_source
        self.line_source = line_source

        plot = figure(title = "Attitude Indicator ", x_range=(-1, 1),
            y_range=(-1,1), tools=[], plot_width=400, plot_height=400)

        # Styling
        plot.xaxis.visible = False
        plot.yaxis.visible = False

        # Artificial Horizon
        plot.patches(xs="x", ys="y", color=["blue", "darkorange"], source=patch_source)

        # Horizontal white lines
        plot.multi_line(xs="x", ys="y", color="white", line_width="width", source=line_source)

        # Center cross
        b = 0.1
        plot.multi_line(xs=[[-b,b],[0,0]], ys=[[0,0],[b,-b]], color="white", line_width=1)

        self.plot = plot
        self.update(0,0, send=False)

    def update(self, pitch, roll, send=True):
        # No, I didn't get the trigonometry right on the first try...
        # Todo: Numpify

        # Artificial Horizon
        right_y = -pitch / 90 - math.tan(-roll / 180*math.pi)
        left_y = -pitch / 90 + math.tan(-roll / 180*math.pi)
        self.patch_source.data["x"] = [[-1, 1, 1, -1], [-1, 1, 1, -1]]
        self.patch_source.data["y"] = [[1, 1, right_y, left_y], [left_y, right_y, -1,-1]]       

        xs = []
        ys = []
        widths = []

        rot = lambda x,y,sin_a,cos_a: (x*cos_a-y*sin_a, y*cos_a+x*sin_a)

        sin_a = math.sin(roll / 180*math.pi)
        cos_a = math.cos(roll / 180*math.pi)

        # White Lines
        x1,y1 = rot(-3, -pitch/90, sin_a, cos_a)
        x2,y2 = rot(3, -pitch/90, sin_a, cos_a)
        xs.append([x1,x2])
        ys.append([y1,y2])
        widths.append(5)

        for i in range(0,4):
            x1,y1 = rot(-0.5,(i+1)*20 / 90 - pitch/90, sin_a, cos_a)
            x2,y2 = rot(0.5,(i+1)*20 / 90 -pitch/90, sin_a, cos_a)
            xs.append([x1,x2])
            ys.append([y1,y2])
            widths.append(2)

            x1,y1 = rot(-0.5,-(i+1)*20 / 90 - pitch/90, sin_a, cos_a)
            x2,y2 = rot(0.5,-(i+1)*20 / 90 - pitch/90, sin_a, cos_a)
            xs.append([x1,x2])
            ys.append([y1,y2])
            widths.append(2)

        self.line_source.data["x"]=xs
        self.line_source.data["y"]=ys
        self.line_source.data["width"]=widths
        replace_bokeh_data_source(self.line_source)
        replace_bokeh_data_source(self.patch_source)
