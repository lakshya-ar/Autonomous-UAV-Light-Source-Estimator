from sympy import symbols, solve
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, PointDrawTool, Slider, Select, Button, Div
from bokeh.layouts import column, row

I1 = int(input("Enter the first Intensity (I1): "))
x1, y1, z1 = map(int, input("Enter initial Mic 1 coordinates (x1 y1 z1): ").split())

I2 = int(input("Enter the second Intensity (I2): "))
x2, y2, z2 = map(int, input("Enterinitial Mic 2 coordinates (x2 y2 z2): ").split())

I3 = int(input("Enter the third Intensity (I3): "))
x3, y3, z3 = map(int, input("Enter initial Mic 3 coordinates (x3 y3 z3): ").split())

I4 = int(input("Enter the fourth Intensity (I4): "))
x4, y4, z4 = map(int, input("Enter initial Mic 4 coordinates (x4 y4 z4): ").split())


# initial mic positions and labels
xs = [x1, x2, x3, x4]   # x coords
ys = [y1, y2, y3, y4]   # y coords
zs = [z1, z2, z3, z4]   # z coords
labels = ['Mic0', 'Mic1', 'Mic2', 'Mic3']

source = ColumnDataSource(data=dict(x=xs, y=ys, label=labels))

p = figure(title="Mic positions — drag points to move", x_range=(-100, 100), y_range=(-100, 100),
           tools="pan,wheel_zoom,reset", width=600, height=600)
r = p.circle('x', 'y', size=14, source=source)

# show labels
p.text('x', 'y', text='label', source=source, x_offset=8, y_offset=8)

# make points draggable
draw_tool = PointDrawTool(renderers=[r], add=False)  # add=False prevents adding new points
p.add_tools(draw_tool)
p.toolbar.active_drag = draw_tool

# Widget: select which mic to edit via sliders
mic_select = Select(title="Select mic to edit", value="0", options=[str(i) for i in range(len(xs))])

# Sliders to edit coordinates of the selected mic
x_slider = Slider(start=-100, end=100, step=0.5, title="X coordinate", value=xs[0])
y_slider = Slider(start=-100, end=100, step=0.5, title="Y coordinate", value=ys[0])

info = Div(text="You can drag points on the plot OR pick a mic and move it using the sliders. "
                "Dragging updates the source directly; the sliders update the selected mic.",
           width=600)

# Result Div for speaker positions
result_div = Div(text="<b>x_speaker:</b> - &nbsp;&nbsp; <b>y_speaker:</b> - &nbsp;&nbsp; <b>z_speaker:</b>", width=900)

# Calculate button
calc_button = Button(label="Calculate positions (x, y, z)", button_type="primary", width=300)

# When selecting a mic, update the slider positions
def select_changed(attr, old, new):
    idx = int(new)
    x_slider.value = source.data['x'][idx]
    y_slider.value = source.data['y'][idx]

mic_select.on_change('value', select_changed)

# When sliders change, write values into the selected mic coords
def update_x(attr, old, new):
    idx = int(mic_select.value)
    d = dict(source.data)
    xs = list(d['x'])
    xs[idx] = new
    d['x'] = xs
    source.data = d

def update_y(attr, old, new):
    idx = int(mic_select.value)
    d = dict(source.data)
    ys = list(d['y'])
    ys[idx] = new
    d['y'] = ys
    source.data = d

x_slider.on_change('value', update_x)
y_slider.on_change('value', update_y)

# Keep sliders in sync if user drags a point: update sliders when source changes
def source_changed(attr, old, new):
    # pick currently selected mic and update sliders to reflect its current position
    idx = int(mic_select.value)
    # guard against index errors if source mutated
    if 0 <= idx < len(source.data['x']):
        x_slider.value = source.data['x'][idx]
        y_slider.value = source.data['y'][idx]

source.on_change('data', source_changed)

# Calculate locations
def calculate_location():
    d = source.data
    xs_list = d.get('x', [])
    ys_list = d.get('y', [])
    zs_list = zs 
    
    n = len(xs_list)
    if n == 0:
        result_div.text = "<b style='color:orange'>No mic positions available.</b>"
        return

    a, b, c = symbols('a b c')

    # Equations
    eq1 = I1*((a - xs_list[0])**2 + (b - ys_list[0])**2 + (c - zs_list[0])**2) - I2*((a - xs_list[1])**2 + (b - ys_list[1])**2 + (c - zs_list[1])**2)
    eq2 = I2*((a - xs_list[1])**2 + (b - ys_list[1])**2 + (c - zs_list[1])**2) - I3*((a - xs_list[2])**2 + (b - ys_list[2])**2 + (c - zs_list[2])**2)
    eq3 = I3*((a - xs_list[2])**2 + (b - ys_list[2])**2 + (c - zs_list[2])**2) - I4*((a - xs_list[3])**2 + (b - ys_list[3])**2 + (c - zs_list[3])**2)

    speaker_position = solve((eq1, eq2, eq3), (a, b, c), dict=True)

    if not speaker_position:
        result_div.text = "<b style='color:red'>No solution found!</b>"
        return

    output_text = "<b>Calculation Results:</b><br>"
    
    for i, sol in enumerate(speaker_position):
        try:
            
            val_a = sol.get(a, 0.0)
            val_b = sol.get(b, 0.0)
            val_c = sol.get(c, 0.0)

            sx = float(val_a)
            sy = float(val_b)
            sz = float(val_c)
            
            output_text += f"<b>Sol {i+1}:</b> X: {sx:.4f}, Y: {sy:.4f}, Z: {sz:.4f}<br>"

        except TypeError:
            output_text += f"Sol {i+1}: <span style='color:red'>Complex (Physically Impossible Inputs)</span><br>"

    result_div.text = output_text

def calc_clicked():
    calculate_location()

calc_button.on_click(calc_clicked)

# Layout
controls = column(mic_select, x_slider, y_slider, calc_button, result_div, width=320)
layout = column(info, row(p, controls))
curdoc().add_root(layout)
curdoc().title = "Mic Position Editor"