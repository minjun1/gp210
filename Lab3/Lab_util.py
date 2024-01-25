import SepVector
import Hypercube
import numpy as np
import genericIO

def vel_txt2sep(filename,cmp_sepVec):
	vrms=[]
	vint=[]
	tau_vrms=[]
	tau_vint=[]
	with open(filename) as fp:
	    line = fp.readline().split()
	    while line:
	        if(line[0]=='red'):
	            tau_vrms.append(float(line[1]))
	            vrms.append(float(line[6]))
	        if(line[0]=='blue'):
	            tau_vint.append(float(line[1]))
	            vint.append(float(line[6]))
	        line = fp.readline().split()
	n_tau = cmp_sepVec.getHyper().getAxis(1).n
	o_tau = cmp_sepVec.getHyper().getAxis(1).o
	d_tau = cmp_sepVec.getHyper().getAxis(1).d
	tau_full = np.arange(o_tau,o_tau+n_tau*d_tau,d_tau)
	
	vrms_full = np.interp(tau_full, tau_vrms, vrms)
	vint_full = np.interp(tau_full, tau_vint, vint)
	tau_Axis=Hypercube.axis(n=n_tau,o=o_tau,d=d_tau,label='tau (sec)')
	vel_hyper=Hypercube.hypercube(axes=[tau_Axis])
	vel_combined_hyper=Hypercube.hypercube(axes=[tau_Axis,Hypercube.axis(n=2,o=0,d=1,label='vel type')])
	vrms_sepVec=SepVector.getSepVector(vel_hyper)
	vint_sepVec=SepVector.getSepVector(vel_hyper)
	vel_combined_sepVec=SepVector.getSepVector(vel_combined_hyper)
	
	vrms_sepVec.getNdArray()[:] = vrms_full
	vint_sepVec.getNdArray()[:] = vint_full
	vel_combined_sepVec.getNdArray()[:] = [vrms_full,vint_full]
	return vrms_sepVec, vint_sepVec, vel_combined_sepVec
