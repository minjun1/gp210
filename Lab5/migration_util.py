import math 
from sep_python.sep_vector import FloatVector,get_sep_vector
from sep_python.hypercube import Hypercube, Axis
import numpy as np
import math
import cmath
from IPython.display import clear_output
import sep_python.modes
io=sep_python.modes.default_io  #Get default IO that expects SEPlib datasets and uses sepVectors


def is_finite_after_operation(arr, operation_desc):
    """
    Check if the array has only finite values after a specific operation.
    If not, print a warning with the operation description.
    """
    if not np.all(np.isfinite(arr)):
        print(f"Warning: Non-finite values detected after {operation_desc}")

def ft1axis(sign, adj, complex_sepVec):
    """
    Add checks for NaN or Inf values after FFT operations.
    """
    complex_ndArray = complex_sepVec.get_nd_array()
    n1 = complex_sepVec.get_hyper().get_axis(1).n
    if adj == 0:
        complex_ndArray[:] = np.fft.fft(complex_ndArray, axis=1)
        is_finite_after_operation(complex_ndArray, "FFT along fast axis")
        complex_ndArray[:] = np.fft.fftshift(complex_ndArray, axes=1)
    else:
        complex_ndArray[:] = np.fft.ifftshift(complex_ndArray, axes=1)
        complex_ndArray[:] = np.fft.ifft(complex_ndArray, axis=1)
        is_finite_after_operation(complex_ndArray, "IFFT along fast axis")
    complex_ndArray[:] = complex_ndArray * sign / math.sqrt(n1)
    is_finite_after_operation(complex_ndArray, "Normalization after FFT/IFFT along fast axis")

def ft2axis(sign, adj, complex_sepVec):
    """
    Add checks for NaN or Inf values after FFT operations.
    """
    complex_ndArray = complex_sepVec.get_nd_array()
    n2 = complex_sepVec.get_hyper().get_axis(2).n
    if adj == 0:
        complex_ndArray[:] = np.fft.fft(complex_ndArray, axis=0)
        is_finite_after_operation(complex_ndArray, "FFT along slow axis")
        complex_ndArray[:] = np.fft.fftshift(complex_ndArray, axes=0)
    else:
        complex_ndArray[:] = np.fft.ifftshift(complex_ndArray, axes=0)
        complex_ndArray[:] = np.fft.ifft(complex_ndArray, axis=0)
        is_finite_after_operation(complex_ndArray, "IFFT along slow axis")
    complex_ndArray[:] = complex_ndArray * sign / math.sqrt(n2)
    is_finite_after_operation(complex_ndArray, "Normalization after FFT/IFFT along slow axis")


def phaseshift_vofz_migration(adj,add,model_sepVec,data_sepVec,vel_sepVec):
    """
    Function to perform pahse shift migration or modeling.
            adj              - boolean; Flag to perform forward or adjoint
            model_sepVec     - sepVector; model space 
            data_sepVec     - sepVector; data space 
    """
    if add == 0:
        if adj: 
            model_sepVec.zero()
        else:    
            data_sepVec.zero()
            
    #set variables
    nz = model_sepVec.get_hyper().get_axis(1).n
    oz = model_sepVec.get_hyper().get_axis(1).o
    dz = model_sepVec.get_hyper().get_axis(1).d
    nx = model_sepVec.get_hyper().get_axis(2).n
    ox = model_sepVec.get_hyper().get_axis(2).o
    dx = model_sepVec.get_hyper().get_axis(2).d
    nt = data_sepVec.get_hyper().get_axis(1).n
    ot = data_sepVec.get_hyper().get_axis(1).o
    dt = data_sepVec.get_hyper().get_axis(1).d
    
    nw = nt
    ow = -math.pi/dt
    dw = 2*math.pi/(nt*dt)
    nkx = nx
    okx = -math.pi/dx
    dkx = 2*math.pi/(nx*dx)
    qi = .5/(nt*dt)
        
    #make complex copy of data_sepVec and model_sepVec
    modelComplex_sepVec=get_sep_vector(model_sepVec.get_hyper(),data_format ="complex128")
    dataComplex_sepVec=get_sep_vector(data_sepVec.get_hyper(),data_format ="complex128")
    
    if adj:
        dataComplex_sepVec.get_nd_array()[:].real = data_sepVec.get_nd_array()
        ft1axis(1,0,dataComplex_sepVec) 
        ft2axis(-1,0,dataComplex_sepVec) 
        
        for ikx in np.arange(nkx):
            clear_output()
            print(ikx/nkx*100,'% finished')
            kx = okx + ikx*dkx
            for iw in np.arange(int(nt/2)):
                w = ow + iw*dw
                cup = dataComplex_sepVec.get_nd_array()[ikx,iw]
                for iz in np.arange(nz):
                    modelComplex_sepVec.get_nd_array()[ikx,iz] = modelComplex_sepVec.get_nd_array()[ikx,iz] + cup
                    cup = cup*np.conj(cmath.exp(-dt*cmath.sqrt(complex(qi,w)**2 + kx*kx/4*vel_sepVec.get_nd_array()[0,iz]**2)))
        ft2axis(-1,1,modelComplex_sepVec) 
        model_sepVec.get_nd_array()[:] = model_sepVec.get_nd_array() + modelComplex_sepVec.get_nd_array().real/nt
    else:
        modelComplex_sepVec.get_nd_array()[:].real = model_sepVec.get_nd_array()
        ft2axis(-1,0,modelComplex_sepVec)
        
        for ikx in np.arange(nkx):
            clear_output()
            print(ikx/nkx*100,'% finished')
            kx = okx + ikx*dkx
            for iw in np.arange(nt/2):
                w = ow + iw*dw
                dataComplex_sepVec.get_nd_array()[ikx,iw] = modelComplex_sepVec.get_nd_array()[ikx,nz-1]
                for iz in np.arange(nz-1,-1,-1):
                    dataComplex_sepVec.get_nd_array()[ikx,iw] = dataComplex_sepVec.get_nd_array()[ikx,iw]*np.conj(cmath.exp(-dt*cmath.sqrt(complex(qi,w)**2 + kx*kx/4*vel_sepVec.get_nd_array()[0,iz]**2))) + modelComplex_sepVec.get_nd_array()[ikx,iz]
        ft1axis(1,1,dataComplex_sepVec) 
        ft2axis(-1,1,dataComplex_sepVec) 
        data_sepVec.get_nd_array()[:] = data_sepVec.get_nd_array() + dataComplex_sepVec.get_nd_array().real


def kirchfast(adj,add,model_sepVec,data_sepVec,vrms_sepVec,amax):
    """
    Function to apply poststack kirchoff migration.
            adj             - boolean; apply forward or adjoint
            add             - boolean; add to input or zer onput 
            model_sepVec    - sepVector; migration output
            data_sepVector  - sepVector; modeling output
            vrms_sepVec     - sepVector; 1d vrms profile
            amax            - float; max angle of energy propagation
    """
    nt = model_sepVec.get_hyper().get_axis(1).n
    ot = model_sepVec.get_hyper().get_axis(1).o
    dt = model_sepVec.get_hyper().get_axis(1).d
    nx = model_sepVec.get_hyper().get_axis(2).n
    ox = model_sepVec.get_hyper().get_axis(2).o
    dx = model_sepVec.get_hyper().get_axis(2).d
    
    vrms_ndArray = vrms_sepVec.get_nd_array()
    data_ndArray = data_sepVec.get_nd_array()
    model_ndArray = model_sepVec.get_nd_array()
    
    if add == 0:
        if adj: 
            model_sepVec.set(0.)
        else:    
            data_sepVec.set(0.)
    amaxRAD = amax/180*math.pi
    for ih in np.arange(int(-nx/2),int(nx/2)):
        clear_output()
        print((ih+int(nx/2))/nx*100,'% finished')
        h = dx * ih # h = offset
        for iz in np.arange(1,nt):
            z = ot + dt * (iz) # z = travel-time depth
            t = math.sqrt( z**2 + (2*h/vrms_ndArray[0,iz])**2 )
            it = int(0.5 + (t - ot) / dt)
            if(it >= nt) :
                  continue
            amp = (z / t) * math.sqrt( nt*dt / t )
            xstart = 1-ih
            xstart = max( 1, xstart)
            xend = nx-ih
            xend = min( nx, xend)
            
            tap=1 #taper value... maybe should depend on amax?
            ataper=10
            ataperRAD=ataper/180*math.pi
            if( amaxRAD-ataperRAD >= math.acos(z/t)):
                tap = 1.0;
            elif ( amaxRAD < math.acos(z/t)):
                tap = 0.0
            else:
                tap = 0.5 * math.pi * (amaxRAD-math.acos(z/t))/(amaxRAD-ataperRAD)**2
            if adj ==0:
                for ix in np.arange(xstart, xend):
                    data_ndArray[ix+ih,it] += model_ndArray[ix,iz]*amp*tap
            else:
                for ix in np.arange(xstart, xend):
                    model_ndArray[ix,iz] += data_ndArray[ix+ih,it]*amp*tap