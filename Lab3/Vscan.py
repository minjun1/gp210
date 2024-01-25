import numpy as np

class Vscan:

    """docstring for Vscan."""

    def __init__(self, model, data):
        ax1 = data.getHyper().getAxis(1)
        tmax = ax1.o + (ax1.n - 1) * ax1.d
        self.tmin = ax1.o
        self.tmax = ax1.n
        self.dt = ax1.d
        ax2 = data.getHyper().getAxis(2)
        offmax = ax2.o + (ax2.n - 1) * ax2.d
        ax3 = model.getHyper().getAxis(2)
        vmax = ax3.o + (ax3.n - 1) * ax3.d

        self.t0 = np.linspace(ax1.o,tmax,ax1.n)
        self.h = np.linspace(ax2.o,offmax,ax2.n)
        self.v = np.linspace(ax3.o,vmax,ax3.n)


    def itime(self,t0,h,v):
        return int((np.sqrt(t0*t0 + h*h / (v*v)) - self.tmin) / self.dt)

    def forward(self, add, model, data):
        if (not add): data.scale(0)
        modNd = model.getNdArray()
        datNd = data.getNdArray()
        for iv in range(modNd.shape[0]):
            for ih in range(datNd.shape[0]):
                for it in range(modNd.shape[1]):
                    itt = self.itime(self.t0[it],self.h[ih],self.v[iv])
                    if itt < self.tmax: datNd[ih,itt] += modNd[iv,it]

    def adjoint(self, add, model, data):
        if (not add): model.scale(0)
        modNd = model.getNdArray()
        datNd = data.getNdArray()
        for iv in range(modNd.shape[0]):
            for ih in range(datNd.shape[0]):
                for it in range(modNd.shape[1]):
                    itt = self.itime(self.t0[it],self.h[ih],self.v[iv])
                    if itt < self.tmax: modNd[iv,it] += datNd[ih,itt]


class NMO:
    """docstring for NMO."""

    def __init__(self, model, data, vpick):

        ax1 = data.getHyper().getAxis(1)
        tmax = ax1.o + (ax1.n - 1) * ax1.d
        self.tmin = ax1.o
        self.tmax = ax1.n
        self.dt = ax1.d
        ax2 = data.getHyper().getAxis(2)
        offmax = ax2.o + (ax2.n - 1) * ax2.d

        self.t0 = np.linspace(ax1.o,tmax,ax1.n)
        self.h = np.linspace(ax2.o,offmax,ax2.n)

        self.update_vel(vpick)

    def itime(self,t0,h,v):
        return int((np.sqrt(t0*t0 + h*h / (v*v)) - self.tmin) / self.dt)

    def update_vel(self,vpick):
        self.v = np.interp(self.t0,vpick[1],vpick[0],left=vpick[0,0],right=vpick[0,-1])

    # nmo spread
    def forward(self, add, model, data):
        if (not add): data.scale(0)
        modNd = model.getNdArray()
        datNd = data.getNdArray()
        for ih in range(datNd.shape[0]):
            for it in range(datNd.shape[1]):
                itt = self.itime(self.t0[it],self.h[ih],self.v[it])
                if itt < self.tmax: datNd[ih,itt] += modNd[ih,it]

    # nmo stack
    def adjoint(self, add, model, data):
        if (not add): model.scale(0)
        modNd = model.getNdArray()
        datNd = data.getNdArray()
        for ih in range(datNd.shape[0]):
            for it in range(datNd.shape[1]):
                itt = self.itime(self.t0[it],self.h[ih],self.v[it])
                if itt < self.tmax: modNd[ih,it] += datNd[ih,itt]
