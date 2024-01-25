import SepVector
import Hypercube
import numpy as np
import genericIO
import math

#################################################################
# The code for Normal Moveout. No need to edit this cell. Just run it.
#################################################################
def adjnull(adj, add, model_sepVec, data_sepVec):
    if(add==0):
        if(adj): 
            model_sepVec.set(0.)
        else:    
            data_sepVec.set(0.)
            
def NMO(adj,add,model_sepVec,data_sepVec,vel_sepVec):
    """
    Function to perform forward or adjoint Normal Moveout (NMO) on a 2d cmp gather
            adj                       - boolean; Flag to perform forward or adjoint
            add                       - boolean; Flag to add to model/data space or zero it 
            model_sepVec              - sepVector; 2d model space. CMP gather 
            model_sepVec              - sepVector; 2d data space. NMOed CMP gather 
            vel_sepVec                - sepVector; 1d RMS velocity profile
    """
    n_off = model_sepVec.getHyper().getAxis(2).n
    d_off = model_sepVec.getHyper().getAxis(2).d
    o_off = model_sepVec.getHyper().getAxis(2).o
    n_tau = model_sepVec.getHyper().getAxis(1).n
    d_tau = model_sepVec.getHyper().getAxis(1).d
    o_tau = model_sepVec.getHyper().getAxis(1).o 
    d_t = data_sepVec.getHyper().getAxis(1).d
    o_t = data_sepVec.getHyper().getAxis(1).o
    
    adjnull(adj, add, model_sepVec, data_sepVec)
    
    for i_off in np.arange(n_off):
        off = o_off + d_off * i_off
        for i_tau in np.arange(n_tau):
            tau = o_tau + d_tau * i_tau
            xs = off/vel_sepVec.getNdArray()[i_tau]
            tt = math.sqrt(tau*tau + xs*xs)
            i_tt = int(0.5 + (tt-o_t)/d_t) 
            if(i_tt < n_tau):
                if(adj==0):
                    data_sepVec.getNdArray()[i_off,i_tt] += model_sepVec.getNdArray()[i_off,i_tau]
                else:
                    model_sepVec.getNdArray()[i_off,i_tau] += data_sepVec.getNdArray()[i_off,i_tt]
