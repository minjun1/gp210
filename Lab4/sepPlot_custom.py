import numpy as np
# import SepVector
# import Hypercube
from sep_python.sep_vector import FloatVector,get_sep_vector
from sep_python.hypercube import Hypercube, Axis
import sep_python.modes
io=sep_python.modes.default_io 
# import pySepVector
import numpy
from ipywidgets import widgets, interactive
import matplotlib.animation as animation


class Position:
    """Keep track of the position in the hypercube"""

    def __init__(self, **kw):
        """Initialize position object
                hyper=hyper
                """
        self.beg = [0] * 8
        self.end = [1] * 8
        self.pos = [0] * 8
        self.o = [0.] * 8
        self.d = [1.] * 8
        self.n = [1] * 8
        if "hyper" in kw:
            self.hyper = kw["hyper"]
            if not isinstance(self.hyper, Hypercube.hypercube):
                raise Exception("hyper muse be type Hypercube.hypercube")
        else:
            raise Exception("Did not find anyway to initialize position")
        self.ndim = len(self.hyper.axes)
        for i in range(self.ndim):
            self.end[i] = self.hyper.axes[i].n
            self.pos[i] = int(self.end[i] / 2)
            self.o[i] = self.hyper.axes[i].o
            self.d[i] = self.hyper.axes[i].d
            self.n[i] = self.hyper.axes[i].n

    def updateSampling(self, iax, origin, sampling):
        """Update sampling"""
        self.o[iax] = origin
        self.d[iax] = sampling

    def positionString(self):
        """Return position string"""
        str = ""
        for i in range(2, self.ndim):
            str += "pos%d=%f " % (i + 1, self.o[i] + self.d[i] * self.pos[i])
        return str


class Orient(Position):
    """Order in which to display the data"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.reverse = [False] * 8
        self.order = range(8)

    def getMinMax(self, iax, rev):
        """getMinMax - get limits of an axis"""
        lower = self.beg[iax] * self.d[iax] + self.o[iax]
        upper = self.end[iax] * self.d[iax] + self.o[iax]
        if not rev:
            return lower, upper
        else:
            return upper, lower


class Dataset:

    def __init__(self, **kw):
        """Initialize a dataset object
           vector=vector (expecting a sepVector"""
        if "vector" in kw:
            self.data = kw["vector"]
            # if not isinstance(self.data, SepVector.vector):
            #     raise Exception("vector muse be type SepVector.vector")
        # else:
        #     raise Exception("Did not find anyway to initialize dataset object")
        self.hyper = self.data.getHyper()

    def getHyper(self):
        """Return hypercube"""
        return self.hyper

    def getVec(self):
        """REturn vector"""
        return self.data

    def getSlice(self, orient, iax1, iax2, rev1=True, rev2=False):
        """Return slice of dataset
                orient - Orrientation
                iax1 - Fast axis for plotting
                iax2 - Slower axis for plotting
                rev1 - Whether or not reverse first axis
                rev2 - Whether or not reverse second axis"""
        return Sepvector.getSepVector(
            vector=self.data, iax1=iax1, iax2=iax2, rev1=rev1, rev2=rev2, beg=orient.beg, end=orient.end)


class Option:

    def __init__(self, param, doc, default, values=None):
        """	param   - Name of parameter
                default - Default value for parameter
                doc 	- Documentation for parameter
                values=None - Possible values for parameter"""
        self.param = param
        self.doc = doc
        self.values = values
        self.val = default

    def setValue(self, val):
        """Set the value of the parameter"""
        if self.values:
            if not val in self.values:
                raise Exception(
                    "Unacceptable value:%s ppossible values=%s" %
                    (val, ",".join(
                        self.values)))
        self.val = val

    def cycleParam(self):
        """Cycle value of parameter"""
        if self.values:
            for i in len(self.values):
                if self.values[i] == self.val:
                    if i + 1 == len(self.values):
                        i = 0
                    else:
                        i = i + 1
                self.val = self.values[i]
        return self.val

    def getParam(self):
        """Returm current parameter"""
        return self.val

    def document(self):
        """Print documentation for option"""
        if not self.values:
            print("%s [%s] - %s" % (self.param, self.val, self.doc))
        else:
            print("%s [%s] -%s\n\t Possible values=%s" %
                  (self.param, self.val, self.doc, ",".join(self.values)))


class Options:
    """Class for options"""

    def __init__(self):
        self.opts = {}

    def addParam(self, param, default, doc, values=None):
        """	param   - Name of parameter
                default - Default value for parameter
                doc 	- Documentation for parameter
                values=None - Possible values for parameter"""
        self.opts[param] = Option(param, default, doc, values)

    def updateValues(self, vs):
        """Update values
            vs - dictionary containing list of values"""
        for k, v in vs.items():
            if k in self.opts.keys():
                self.opts[k].setValue(v)

    def document(self):
        """Print documentation"""
        for s, v in self.opts.items():
            v.document()

    def cycleParam(self, par):
        """Cycle parameter"""
        if not par in self.opts:
            raise Exception("Param-%s does not exist" % (par))
        self.opts[par].cycleParam()

    def getParam(self, par):
        """Return parameter"""
        if not par in self.opts:
            return False
            #raise Exception("Param-%s does not exist" % par)
        return self.opts[par].getParam()

    def setValue(self, par, val):
        """Set a value"""
        if not par in self.opts:
            raise Exception("Param-%s does not exist" % par)
        return self.opts[par].setValue(val)


class sepPlot:
    """Generic plot class that will setup good defaults"""

    def __init__(self, plt, data, kw):
        """Initialize sePlot
            plt - matplotlib.plot object
            data - sepVector object
            kw   - optional arguments"""
        self.data = Dataset(vector=data)
        self.hyper=data.get_hyper()
        self.options = self.setDefaults()
        self.plt = plt
        self.move = 1
        self.orient = Orient(hyper=self.data.get_hyper())

    def setDefaults(self):
        """Set defaults"""
        o = Options()
        o.addParam("title", "Title for plot", "")
        o.addParam("label2", "Label for second axis", None)
        for i in range(len(self.data.get_hyper().axes)):
            o.addParam(
                "label%d" %
                (i + 1), "Label for %d axis" %
                (i + 1), self.data.get_hyper().axes[i].label)
            o.addParam(
                "o%d" %
                (i + 1), "origin for %d axis" %
                (i + 1), self.data.get_hyper().axes[i].o)
            o.addParam(
                "d%d" %
                (i + 1), "sampling for %d axis" %
                (i + 1), self.data.get_hyper().axes[i].d)
            o.addParam(
                "min%d" %
                (i + 1), "Miimum for %d axis" %
                (i + 1), self.data.get_hyper().axes[i].o)
            o.addParam(
                "max%d" %
                (i +
                 1),
                "Maximum for %d axis" %
                (i +
                 1),
                self.data.get_hyper().axes[i].o +
                self.data.get_hyper().axes[i].d *
                self.data.get_hyper().axes[i].n)
        o.addParam("titleFontSize", "Font size for title", 18)
        o.addParam("labelFontSize", "Font size for label", 14)
        o.addParam("figsize", "Size of figure to plot", None)
        o.addParam(
            "transp",
            "Whether or not transpose the first and second axis",
            True)
        o.addParam("reversex", "Whether or not to reverse the x axis", False)
        o.addParam("reversey", "Whether or not to reverse the y axis", False)
        return o

    def reverseOption(self, revs):
        """Set the reverse for an axis"""
        ic = 0
        for r in revs:
            if r:
                ic += 1
        if ic % 2 == 1:
            return True
        else:
            return False

    def selfDoc(self):
        """Print self documentation"""
        self.options.document()

    def redoSampling(self):
        """Reset sampling of hypercube"""
        for i in len(self.hyper.axes):
            self.orient.updateSampling(
                i,
                self.getParam(
                    "o%d" % (i + 1)),
                self.getParam(
                    "d%d" % (i + 1)))

    def getCurrentSlice(self):
        """Return the current slice given the position"""
        ns = self.data.getVec().getHyper().getNs()

        if len(ns) < 3:
            return self.data.getVec()
        else:
            if ns[1] == 1:
                if isinstance(self.data.getVec(), SepVector.floatVector):
                    return SepVector.floatVector(fromCpp=pySepVector.float1DReg(self.data.getVec().cppMode,
                                                                                0, False,
                                                                                self.orient.pos, self.orient.beg, self.orient.end))
                elif isinstance(self.data.getVec(), SepVector.doubleVector):
                    return SepVector.doubleVector(fromCpp=pySepVector.double1DReg(self.data.getVec().cppMode,
                                                                                  0, False,
                                                                                  self.orient.pos, self.orient.beg, self.orient.end))
                elif isinstance(self.data.getVec(), SepVector.intVector):
                    return SepVector.intVector(fromCpp=pySepVector.int1DReg(self.data.getVec().cppMode,
                                                                            0, False,
                                                                            self.orient.pos, self.orient.beg, self.orient.end))
                elif isinstance(self.data.getVec(), SepVector.byteVector):
                    return SepVector.byteVector(fromCpp=pySepVector.byte1DReg(self.data.getVec().cppMode,
                                                                              0, False,
                                                                              self.orient.pos, self.orient.beg, self.orient.end))
                elif isinstance(self.data.getVec(), SepVector.complexVector):
                    return SepVector.complexVector(fromCpp=pySepVector.complex1DReg(self.data.getVec().cppMode,
                                                                                    0, False,
                                                                                    self.orient.pos, self.orient.beg, self.orient.end))
                else:
                    raise Exception("Unknown type ", type(self.data))
            else:
                if isinstance(self.data.getVec(), SepVector.floatVector):
                    x = SepVector.floatVector(fromCpp=pySepVector.float2DReg(self.data.getVec().cppMode,
                                                                             0, False, 1, False,
                                                                             self.orient.pos, self.orient.beg, self.orient.end))
                    return x
                elif isinstance(self.data.getVec(), SepVector.doubleVector):
                    return SepVector.doubleVector(fromCpp=pySepVector.double2DReg(self.data.getVec().cppMode,
                                                                                  0, False, 1, False,
                                                                                  self.orient.pos, self.orient.beg, self.orient.end))
                elif isinstance(self.data.getVec(), SepVector.intVector):
                    return SepVector.intVector(fromCpp=pySepVector.int2DReg(self.data.getVec().cppMode,
                                                                            0, False, 1, False,
                                                                            self.orient.pos, self.orient.beg, self.orient.end))
                elif isinstance(self.data.getVec(), SepVector.byteVector):
                    return SepVector.byteVector(fromCpp=pySepVector.byte2DReg(self.data.getVec().cppMode,
                                                                              0, False, 1, False,
                                                                              self.orient.pos, self.orient.beg, self.orient.end))
                elif isinstance(self.data.getVec(), SepVector.complexVector):
                    return SepVector.complexVector(fromCpp=pySepVector.complex2DReg(self.data.getVec().cppMode,
                                                                                    0, False, 1, False,
                                                                                    self.orient.pos, self.orient.beg, self.orient.end))
                else:
                    raise Exception("Unknown type ", type(self.data))

    def sweepNext(self, move=1):
        """Update position in a sweep"""

        for imove in range(move):
            found = False
            i = 0
            while not found and i < len(self.sweepRotate):
                idim = self.sweepRotate[i]
                if self.sweepDir == 1:
                    if self.orient.pos[idim] + 1 == self.orient.end[idim]:
                        self.orient.pos[idim] = self.orient.beg[idim]
                        i = i + 1
                    else:
                        self.orient.pos[idim] += 1
                        found = True
                else:
                    if self.orient.pos[idim] == self.orient.beg[idim]:
                        self.orient.pos[idim] = self.orient.end[idim] - 1
                        i = i + 1
                    else:
                        self.orient.pos[idim] -= 1
                        found = True
            if not found:
                for i in range(len(self.sweepRotate)):
                    idim = self.sweepRotate[i]
                    if self.sweepDir == 1:
                        self.orient.pos[idim] = self.orient.beg[idim]
                    else:
                        self.orient.pos[idim] = self.orient.end[idim] - 1

    def initializeSweep(self, dim=None):
        """Initialize a sweep through the dataset"""
        if dim:
            self.sweepDim = dim
        self.sweepRotate = []
        self.sweepDir = 1
        self.sweepOn = True
        self.sweepTime = 200
        for i in range(self.sweepDim, 8):
            if self.orient.n[i] > 1:
                self.sweepRotate.append(i)
                self.orient.pos[i] = self.orient.beg[i]
        if len(self.sweepRotate) == 0:
            return False
        else:
            return True

    def getParam(self, par):
        """Get parameter"""
        return self.options.getParam(par)

    def setValue(self, par, val):
        """Set parameter"""
        self.options.setValue(par, val)

    def getAxisLimits(self, ax1, rev1, ax2, rev2):
        """Get axis limits
                ax1  - Fast axis (Up-Down)
                rev1 - Reverse axis 1
                ax2  - Slower axis (Left-Right)
                rev2 - Reverse axis 2"""
        a1L, a1H = self.orient.getMinMax(ax1, rev1)
        a2L, a2H = self.orient.getMinMax(ax2, rev2)
        return [a1L, a1H, a2H, a2L]


class plot2D(sepPlot):

    def __init__(self, plt, data, **kw):
        super().__init__(plt, data, kw)

    def setDefaults(self):
        """Set defaults for all 2-D fields
          label2,o2,d2 - From axis 2"""
        o = super().setDefaults()
        o.addParam("scalebar", "Whether or not to draw a scalebar", False)
        o.addParam("scalebarOrientation", "Location of the scalebar",
                   "vertical", ["vertical", "horizontal"])
        o.addParam("scalebarLabel", "Label for the  scalebar", None)
        return o

    def transformSlice(self, currentSlice):
        """Transform slice"""
        if self.getParam("transp"):
            self.revX = self.reverseOption(
                [self.getParam("reversex"), self.orient.reverse[1]])
            self.revY = self.reverseOption(
                [self.getParam("reversey"), self.orient.reverse[0]])
            vec = SepVector.getSepVector(vector=currentSlice, iax1=1, iax2=0, rev1=self.revX,
                                         rev2=self.revY, ipos=self.orient.pos, beg=self.orient.beg, end=self.orient.end)
            self.iax1 = 1
            self.iax2 = 0
            self.labelY = self.getParam("label1")
            self.labelX = self.getParam("label2")
        else:
            self.revX = self.reverseOption(
                [self.getParam("reversex"), self.orient.reverse[0]])
            self.revY = self.reverseOption(
                [self.getParam("reversey"), self.orient.reverse[1]])
            vec = SepVector.getSepVector(vector=currentSlice, iax1=0, iax2=1, rev1=self.revX,
                                         rev2=self.revY, ipos=self.orient.pos, beg=self.orient.beg, end=self.orient.end)
            self.labelX = self.getParam("label1")
            self.labelY = self.getParam("label2")
            self.iax1 = 0
            self.iax2 = 1
        return vec

    def nextSlice(self, frame=None):
        """Update the move with the next slice"""

        self.sweepNext(self.move)

        vec = self.transformSlice(
            self.getCurrentSlice())
        self.ax.set_title(
            self.orient.positionString(),
            fontsize=self.getParam("titleFontSize"))
        self.image.set_array(vec.getNdArray())
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def keyRelease(self, event):
        self.move = 1
        self.animate.event_source.stop()

        if event.key == "r":
            self.startAnimation()

        elif event.key == "s":
            self.sweepTime = min(2000, int(self.sweepTime * 1.5))

            self.startAnimation()
        elif event.key == "f":
            self.sweepTime = max(50, int(self.sweepTime / 1.5))

            self.startAnimation()
        if event.key == "n":
            self.sweepDir = 1
            self.nextSlice()
        elif event.key == "m":
            self.sweepDir = -1
            self.nextSlice()
        elif event.key == "0":
            self.initializeSweep()
            self.move = 0
            self.nextSlice()
        elif event.key == "1":
            self.move = 1
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "2":
            self.move = 2
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "3":
            self.move = 3
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "4":
            self.move = 4
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "5":
            self.move = 5
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "6":
            self.move = 6
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "7":
            self.move = 7
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "8":
            self.move = 8
            self.initializeSweep()
            self.nextSlice()
        elif event.key == "9":
            self.initializeSweep()
            self.move = 9
            self.nextSlice()
        self.figure.canvas.draw()

    def connect(self):
        """Connect keyboard and mouse controls"""
        self.bpress = self.figure.canvas.mpl_connect(
            "key_release_event", self.keyRelease)

    def startAnimation(self):
        self.move = 1
        self.animate = animation.FuncAnimation(
            self.figure, self.nextSlice, interval=self.sweepTime)

    def animate(self):
        """Animate display"""

        movie = self.initializeSweep(2)

        self.output(movie)

        self.connect()
        if movie:
            self.startAnimation()
        self.figure.show()

    def getColormap(self):
        """Get the colormap to use"""
        col = self.getParam("color")
        cmap = self.getParam("cmap")
        if not cmap:
            cmap = self.cmaps[col]
        return cmap


class Grey(plot2D):

    def __init__(self, plt, data, **kw):
        """Plot a varialbe density plot
                plt - matplotlib.plt
                data - sepVector
                kw   - addtional options

                Use selfDoc for options available"""

        super().__init__(plt, data, **kw)
        self.cmaps = {
            "I": "gray",
            "j": "gist_rainbow",
            "J": "rainbow",
            "F": "seismic"}
        self.first = True
        if kw:
            self.options.updateValues(kw)

        if "animate" in kw:
            self.animate()

    def setDefaults(self):
        o = super().setDefaults()
        o.addParam("bpclip", "Begining clip pct", 1.)
        o.addParam("epclip", "End clip pct", 99.)
        o.addParam("color", "Colormaps", "I", ["I", "j", "J", "F"])
        o.addParam("cmap", "Specify matplotlib colormap", None)
        o.addParam(
            "gainpanel",
            "Gainpanel (e-every panel, a- all, ith-base clip on pct)",
            "e")
        o.addParam("bclip", "Begining clip", None)
        o.addParam("eclip", "Enging clip", None)
        o.addParam("aspect", "Aspect ratio for the plot", "auto")
        return o

    def getClips(self):
        """Return the clip values"""
        gp = self.getParam("gainpanel")
        if gp[0:0] == "e":
            pass
        elif self.first:
            self.first = False
            if not self.getParam("bclip"):
                self.setValue(
                    "bclip", self.data.getVec().cent(
                        self.getParam("bpclip")))
            if not self.getParam("eclip"):
                self.setValue(
                    "eclip", self.data.getVec().cent(
                        self.getParam("epclip")))

    def transformSlice(self, currentSlice):
        """Transform slice"""
        vec = super().transformSlice(currentSlice)
        self.getClips()
        vec.clip(self.getParam("bclip"), self.getParam("eclip"))
        return vec

    def output(self, animated=False):
        """Output a static 2-D plot"""

        m = self.getCurrentSlice()
        vec = self.transformSlice(m)

        if self.getParam("figsize"):
            self.figure, self.ax = self.plt.subplots(
                figsize=self.getParam("figsize"))
        else:
            self.figure, self.ax = self.plt.subplots()

        self.image = self.ax.imshow(vec.getNdArray(), cmap=self.getColormap(),
                                    extent=self.getAxisLimits(
            self.iax1, self.revX, self.iax2, self.revY),
            aspect=self.getParam("aspect"), animated=animated)

        if self.getParam("title"):
            self.titleObj = self.ax.set_title(
                self.getParam("title"),
                fontsize=self.getParam("titleFontSize"))
        self.ax.set_xlabel(
            self.labelX,
            fontsize=self.getParam("labelFontSize"))
        self.ax.set_ylabel(
            self.labelY,
            fontsize=self.getParam("labelFontSize"))
        if self.getParam("scalebar"):
            CBI = self.plt.colorbar(self.image,
                                    orientation=self.getParam("scalebarOrientation"))
            if self.getParam("scalebarLabel"):
                CBI.set_label(self.getParam("scalebarLabel"))
        self.plt.ion()
        self.plt.show()
        self.plt.pause(0.01)
        # self.plt.show()
        #raise Exception("faile 2")


class Contour(plot2D):

    def __init__(self, plt, data, **kw):
        """Plot a varialbe density plot
                plt - matplotlib.plt
                data - sepVector
                kw   - addtional options

                Use selfDoc for options available"""
        super().__init__(plt, data, **kw)
        if kw:
            self.options.updateValues(kw)

    def setDefaults(self):
        """Set defaults for Contour"""
        o = super().setDefaults()
        o.addParam("levels", "Specify the contour values (int array)", None)
        o.addParam("labelContour", "Label the contours", False)
        o.addParam("contourFontSize", "Fontsize for labeling contours", 10)
        o.addParam("contourFontSize", "Fontsize for labeling contours", 10)
        return o

    def output(self, animated=False, **kw):

        vec, labelX, labelY, iax1, iax2 = self.transformSlice(
            self.getCurrentSlice())

        if self.getParam("figsize"):
            self.figure = self.plt.figure(figsize=self.getParam("figsize"))
        else:
            self.figure = self.plt.figure()

        if self.getParam("levels"):
            self.image = self.plt.contour(vec.getNdArray(), extent=self.getAxisLimits(iax1, revX, iax2, revY),
                                          levels=self.getParam("levels"), animated=animated)
        else:
            self.image = self.plt.contour(vec.getNdArray(), extent=self.getAxisLimits(iax1, revX, iax2, revY),
                                          animated=animated)
        if self.getParam("title"):
            self.plt.title(
                self.getParam("title"),
                fontsize=self.getParam("titleFontSize"))
        if self.getParam("labelContour"):
            self.plt.clabel(
                self.image,
                inline=1,
                fontsize=self.getParam("contourFontSize"))
        self.plt.xlabel(labelX, fontsize=self.getParam("labelFontSize"))
        self.plt.ylabel(labelY, fontsize=self.getParam("labelFontSize"))
        if self.getParam("scalebar"):
            CBI = self.plt.colorbar(
                orientation=self.getParam("scalebarOrientation"))
            if self.getParam("scalebarLabel"):
                CBI.set_label(self.getParam("scalebarLabel"))
    #    self.plt.show()


class plot1D(sepPlot):

    def __init__(self, plt, data, **kw):
        super().__init__(plt, data, kw)

    def setDefaults(self):
        """Set defaults """
        o = super().setDefaults()
        return o

    def getDomainRange(self, current):
        """Get domain"""
        domains = []
        ranges = []
        v = current.getVec()
        vnd = v.getNdArray()
        ndim = current.getHyper().getNdim()
        if ndim == 1:
            if isinstance(v, pySepVector.complex1DReg):
                domains.append(vnd[:].real)
                ranges.append(vnd[:].imag)
            else:
                domains.append(np.arange(self.getParam("o1"),
                                         self.getParam("o1") + self.getParam("d1") * self.orient.n[0], self.getParam("d1")))
                ranges.append(vnd[:])
        elif ndim == 2:
            if isintance(v, pySepVector.complex2DReg):
                for i in range(self.getParam("n2")):
                    domains.append(vnd[i][:].real)
                    ranges.append(vnd[i][:].imag)
            else:
                for i in range(self.getParam("n2")):
                    domains.append(np.arange(self.getParam("o1"),
                                             self.getParam("o1") + self.getParam("d1") * self.orient.n[0], self.getParam("d1")))
                    ranges.append(vnd[i][:])
        else:
            raise Exception("Can only 1 and 2-D")
        return domains, ranges

    def getXY(self):
        currentSlice = self.getCurrentSlice()
        domains, ranges = self.getDomainRange(currentSlice)
        if not self.getParam("transp"):
            return ranges, domains, self.getParam(
                "label2"), self.getParam("label1")
        else:
            return domains, ranges, self.getParam(
                "label1"), self.getParam("label2")


class Dots(plot1D):

    def __init__(self, plt, data, **kw):
        """Plot a varialbe density plot
                plt - matplotlib.plt
                data - sepVector
                kw   - addtional options

                Use selfDoc for options available"""
        super().__init__(plt, data, **kw)

    def setDefaults(self):
        """Set defaults """
        o = super().setDefaults()
        o.addParam(
            "lineColor", "List of line colors", [
                "black", "green", "blue", "red", "yellow", "cyan"])
        o.addParam("lineWidth", "List of line widths", 1)
        return o

    def output(self, animated=False):
        """Output 2-D figure"""
        if not isinstance(self.getParam("lineColor"), list):
            raise Exception("Expecting lineColor to be a list")

        if self.getParam("figsize"):
            self.plt.figure(figsize=self.getParam("figsize"))

        xs, ys, labelX, labelY = self.getXY()
        self.plt.figure(figsize=self.getParam("figsize"))

        for i in range(len(xs)):
            markerLines, stemLines, baseLine = self.plt.stem(
                xs[i], ys[i], animated=animated)
            j = i % len(self.getParam("lineColor"))
            c = self.getParam("lineColor")[j]
            self.plt.setp(
                stemLines, color=c, linewidth=int(
                    self.getParam("lineWidth")))
            z = self.plt.setp(markerLines, "markerfacecolor", c)
        self.plt.xlabel(labelX, fontsize=self.getParam("labelFontSize"))
        self.plt.ylabel(labelY, fontsize=self.getParam("labelFontSize"))
        if self.getParam("title"):
            self.plt.title(
                self.getParam("title"),
                fontsize=self.getParam("titleFontSize"))


class Graph(plot1D):

    def __init__(self, plt, data, **kw):
        """Plot a varialbe density plot
                plt - matplotlib.plt
                data - sepVector
                kw   - addtional options

                Use selfDoc for options available"""
        super().__init__(plt, data, **kw)

    def setDefaults(self):
        """Set defaults """
        o = super().setDefaults()
        o.addParam("styles", "Line styles lookup matplotlib",
                   ["k-", "r-", "g-", "b-", "c-", "m-", "y-"])
        o.addParam("minX", "Minimum value for x", False)
        o.addParam("maxX", "Maximum value for x", False)
        o.addParam("minY", "Minimum value for y", False)
        o.addParam("maxY", "Maximum value for y", False)
        return o

    def output(self, animated=False):
        """Output 2-D figure"""
        if not isinstance(self.getParam("styles"), list):
            raise Exception("Expecting styles to be a list")

        if self.getParam("figsize"):
            self.plt.figure(figsize=self.getParam("figsize"))

        xs, ys, labelX, labelY = self.getXY()
        out = []
        for i in range(len(xs)):
            out.append(xs[i])
            out.append(ys[i])
            j = i % len(self.getParam("styles"))
            out.append(self.getParam("styles")[j])
        self.plt.plot(*out, animated=animated)
        self.plt.xlabel(labelX, fontsize=self.getParam("labelFontSize"))
        self.plt.ylabel(labelY, fontsize=self.getParam("labelFontSize"))
        axes = self.plt.gca()
        xmin, xmax = self.plt.xlim()
        ymin, ymax = self.plt.ylim()
        if self.getParam("minX"):
            xmin = self.getParam("minX")
        if self.getParam("minY"):
            ymin = self.getParam("minY")
        if self.getParam("maxX"):
            xmax = self.getParam("maxX")
        if self.getParam("maxY"):
            ymax = self.getParam("maxY")
        axes.set_xlim([xmin, xmax])
        axes.set_ylim([ymin, ymax])
        if self.getParam("reversex"):
            plt.gca().invert_xaxis()
        if self.getParam("reversey"):
            plt.gca().invert_yaxis()
        if self.getParam("title"):
            self.plt.title(
                self.getParam("title"),
                fontsize=self.getParam("titleFontSize"))

