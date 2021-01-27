import pandas as pd
import numpy as np
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, Line, LinearAxis, Plot, LabelSet, LinearColorMapper, Range1d
from bokeh.io.export import get_screenshot_as_png



def plotprotein(sequence, other_binding, dna_binding, metal_binding, active):
    x_values = range(0, len(other_binding))
    source1 = ColumnDataSource(dict(x=x_values, y=other_binding, names=[i for i in sequence[0]]))
    source2 = ColumnDataSource(dict(x=x_values, y=dna_binding, names=[i for i in sequence[0]]))
    source3 = ColumnDataSource(dict(x=x_values, y=metal_binding, names=[i for i in sequence[0]]))
    source4 = ColumnDataSource(dict(x=x_values, y=active, names=[i for i in sequence[0]]))
    glyph1 = Line(x="x", y="y", line_color="red", line_width=3, line_alpha=0.6)
    glyph2 = Line(x="x", y="y", line_color="blue", line_width=3, line_alpha=0.6)
    glyph3 = Line(x="x", y="y", line_color="green", line_width=3, line_alpha=0.6)
    glyph4 = Line(x="x", y="y", line_color="orange", line_width=3, line_alpha=0.6)
    plot = Plot(
        title=None, plot_height=150,
        min_border=0, toolbar_location=None)
    plot.add_glyph(source1, glyph1)
    plot.add_glyph(source2, glyph2)
    plot.add_glyph(source3, glyph3)
    plot.add_glyph(source4, glyph4)
    xaxis = LinearAxis()

    labels = LabelSet(x='x', y=1, text='names', level='glyph',
                      x_offset=-1, y_offset=5, source=source1, render_mode='canvas')
    plot.add_layout(labels)
    yaxis = LinearAxis()
    plot.add_layout(yaxis, 'left')
    plot.yaxis.bounds = (0, 1)
    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.y_range = Range1d(-0.1, 1.5)
    curdoc().add_root(plot)
    image = get_screenshot_as_png(plot, height=150)

    return image


input_data = ['AYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATG']
values = np.array((0, 0, 0, 0, 0.1, 0.3, 0.4, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1, 0.2, 0.3, 0.1, 0.1, 0.31, 0.5, 0.6,
                         0.7, 0.3, 0.1, 0.2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                         0))

show(plotprotein(input_data, values, values, values, values))


