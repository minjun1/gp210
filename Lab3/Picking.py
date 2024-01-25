import ipywidgets as widgets
import numpy as np
import matplotlib.colors as mcolors

class LineBuilder:
    def __init__(self, axis, color='b'):
        self.ax = axis
        self.line, = self.ax.plot([],[],marker='x')
        self.set_color(color)
        self.xs = list(self.line.get_xdata())
        self.ys = list(self.line.get_ydata())
        self.connect()

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        if event.button == 1:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.refresh()

    def get_color(self):
        return self.color

    def set_color(self,color):
        self.line.set_color(color)
        self.color = mcolors.to_hex(color)

    def refresh(self):
        # self.plt.draw()
        self.line.figure.canvas.draw()

    def remove(self):
        self.disconnect()
        del self.xs, self.ys
        self.ax.lines.remove(self.line)
        self.refresh()

    def get_data(self):
        return self.line.get_data()

    def disconnect(self):
        self.line.figure.canvas.mpl_disconnect(self.cid)
        self.refresh()

    def connect(self):
        self.refresh()
        self.cid = self.line.figure.canvas.mpl_connect('button_press_event', self)


class Buttons:
    def __init__(self, axis):
        self.picking = widgets.ToggleButton(description='Picking')
        self.plus = widgets.Button(description='+',disabled=True,layout=widgets.Layout(width='30px',height='30px'))
        self.minus = widgets.Button(description='-',disabled=True,layout=widgets.Layout(width='30px',height='30px'))
        self.dropdown = widgets.Dropdown(
            options=[('', 0)],
            value=0,
            description='Events:',
            disabled = True,
        )
        self.color = widgets.ColorPicker(
            concise=True,
            value='blue',
            disabled=True
        )
        self.filename = widgets.Text(
            value='pick.npz',
            placeholder='Type something',
            description='Filename:',
            disabled=True
        )
        self.save_as = widgets.Button(description='Save',disabled=True,layout=widgets.Layout(width='60px',height='30px'))

        self.picking.observe(self.start_pick)

        self.box = widgets.HBox([self.picking, self.dropdown,
                                self.plus, self.minus, self.color, self.filename, self.save_as])

        self.lines = {}
        self.connected = False
        self.axis = axis

    def start_pick(self,change):
        self.plus.on_click(self.add_pick)
        self.minus.on_click(self.remove_pick)
        self.dropdown.observe(self.choose_pick,names='value')
        self.color.observe(self.choose_color, names='value')
        self.save_as.on_click(self.save_pick)

        if self.picking.value == True:
            self.dropdown.disabled = False
            self.plus.disabled = False
            self.minus.disabled = False
            self.color.disabled = False
            self.filename.disabled = False
            self.save_as.disabled = False
        else:
            self.dropdown.disabled = True
            self.plus.disabled = True
            self.minus.disabled = True
            self.color.disabled = True
            self.filename.disabled = True
            self.save_as.disabled = True

    def add_pick(self,change):
        if len(self.dropdown.options) == 1: self.plus.count = 0
        self.plus.count += 1
        name = 'Pick %s' % self.plus.count
        self.lines[name] = LineBuilder(self.axis)

        self.dropdown.options += ((name, self.plus.count),)
        self.dropdown.value = self.plus.count
        self.minus.disabled = False

    def remove_pick(self,change):
        if self.plus.count != 0:
            if self.dropdown.value != 0:
                l = list(self.dropdown.options)
                name = "Pick %s" % self.dropdown.value
                l.remove((name, self.dropdown.value))
                self.dropdown.options = tuple(l)
                self.lines[name].remove()
        else:
            self.minus.disabled = True

    def choose_pick(self, change):
        if change.new:
            if  len(self.dropdown.options) > 2:
                self.lines[self.connected].disconnect()
            name = "Pick %s" % change.new
            self.lines[name].connect()
            self.connected = name
            self.color.value = self.lines[name].get_color()

    def save_pick(self,change):
        files = {}
        opts = list(self.dropdown.options)
        for i in range(1,len(opts)):
            name = opts[i][0]
            files[name] = self.lines[name].get_data()
        np.savez(self.filename.value, **files)

    def choose_color(self,change):
        if self.dropdown.value > 0:
            name = "Pick %s" % self.dropdown.value
            self.lines[name].set_color(change.new)

    def show(self):
        display(self.box)
