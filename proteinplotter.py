import pandas as pd
import numpy as np
from bokeh.io import curdoc, show, reset_output
from bokeh.models import ColumnDataSource, Grid, Line, LinearAxis, Plot, LabelSet, LinearColorMapper, Range1d
#from bokeh.io.export import get_screen
from bokeh.plotting import figure
from bokeh.layouts import column


def plotprotein(sequence, other_binding, dna_binding, metal_binding, active, variant_location):
    sequence = [i for i in sequence[0]]
    sequence += [''] * (3000 - len(sequence))
    print(sequence)
    if variant_location > 50:
        start_seq = variant_location - 50
    else:
        start_seq = 0
    if variant_location + 50 < len(sequence):
        end_seq = variant_location + 50
    else:
        end_seq = 3000
    x_values = range(0, 3000)
        #x_values = range(starting_value, value)
    source1 = ColumnDataSource(dict(x=x_values[start_seq:end_seq], y=other_binding[start_seq:end_seq],
                                    names=sequence[start_seq:end_seq]))
    source2 = ColumnDataSource(dict(x=x_values[start_seq:end_seq], y=dna_binding[start_seq:end_seq],
                                    names=sequence[start_seq:end_seq]))
    source3 = ColumnDataSource(dict(x=x_values[start_seq:end_seq], y=metal_binding[start_seq:end_seq],
                                    names=sequence[start_seq:end_seq]))
    source4 = ColumnDataSource(dict(x=x_values[start_seq:end_seq], y=active[start_seq:end_seq],
                                    names=sequence[start_seq:end_seq]))
    glyph1 = Line(x="x", y="y", line_color="red", line_width=3, line_alpha=0.6)
    glyph2 = Line(x="x", y="y", line_color="blue", line_width=3, line_alpha=0.6)
    glyph3 = Line(x="x", y="y", line_color="green", line_width=3, line_alpha=0.6)
    glyph4 = Line(x="x", y="y", line_color="orange", line_width=3, line_alpha=0.6)
    plot = Plot(
        title=None, plot_height=150, plot_width=1000,
        min_border=0, toolbar_location=None)
    plot.add_glyph(source1, glyph1)
    plot.add_glyph(source2, glyph2)
    plot.add_glyph(source3, glyph3)
    plot.add_glyph(source4, glyph4)
    xaxis = LinearAxis()
        #YOUR_FONT_SIZE = 10
    labels = LabelSet(x='x', y=1, text='names', level='glyph',
                        x_offset=-1, y_offset=5, source=source1,
                        render_mode='canvas', text_font_size='5pt')
    plot.add_layout(labels)
    yaxis = LinearAxis()
    plot.add_layout(yaxis, 'left')
    plot.yaxis.bounds = (0, 1)
    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.y_range = Range1d(-0.1, 1.5)
    show(plot)

#input_data = ['AYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATGAYTGYGGATG']
#values = np.random.rand(3000,)
#print(values)
#plotprotein(input_data, values, values, values, values)


