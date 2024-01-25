import Picking
import Grey
import Vscan
import SepVector
import Hypercube
import numpy as np

class Vpick:

    def __init__(self,plt,data,vmin=1.5,vmax=4,dv=0.1,**kw):
        self.panels = []
        fig, axes = plt.subplots(1,2)
        self.buttons = Picking.Buttons(axes[1])
        self.buttons.show()

        vels = self.create_vels(data,vmin,vmax,dv)
        nmo_data = data.clone()
        vscan = Vscan.Vscan(vels,data)
        vscan.adjoint(False,vels,data)
        vels = self.envelope(vels)

        # original data
        self.panels.append(Grey.Grey(plt,data,axis=axes[0],title='CMP gather',**kw))
        # nmo-ed data
        # self.panels.append(Grey.Grey(plt,nmo_data,axis=axes[1],title='NMO-corrected',**kw))
        # vscan
        self.panels.append(Grey.Grey(plt,vels,axis=axes[1],cmap='rainbow',title='Velocity scan',**kw))

    def create_vels(self,data,vmin,vmax,dv):
        nv = int((vmax-vmin)/dv)
        vels = SepVector.getSepVector(Hypercube.hypercube(ns=[data.getHyper().getAxis(1).n,nv],
                                                    ds=[data.getHyper().getAxis(1).d,dv],
                                                    os=[data.getHyper().getAxis(1).o,vmin],
                                                    labels=['','Velocity(km/s)']))
        return vels

    def envelope(self,data):
        array = data.getNdArray()
        fft = np.fft.fft(array,norm='ortho')
        fft[:,0] = 1
        fft[:,1:fft.shape[1]//2] *= 2
        fft[:,fft.shape[1]//2] = 1
        array[:] = np.abs(np.fft.ifft(fft,norm='ortho'))
        return data

    def output(self):
        for panel in self.panels:
            panel.output()
