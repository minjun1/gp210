import sepPlot_custom
# import SepVector
import sep_python.sep_vector as SepVector
import numpy
import matplotlib.animation as animation
from IPython.display import HTML
import Picking


class Grey(sepPlot_custom.sepPlot):
	def __init__(self,plt,data,axis=None,**kw):
		self.kw=kw
		self.hyper=data.get_hyper()
		super().__init__(plt,data,kw)
		self.cmaps={"I":"gray","j":"gist_rainbow","J":"rainbow","F":"seismic"}
		self.plt = plt
		if axis:
			self.axis = axis
			self.figure = plt.gcf()
		else:
			self.figure, self.axis = plt.subplots()

		if "picking" in kw and kw["picking"]:
			self.buttons = Picking.Buttons(self.axis)
			self.buttons.show()

		self.array=data.getNdArray()


	def setDefaults(self):
		o = super().setDefaults()
		o.addParam("bpclip", "bottom clip",1.)
		o.addParam("epclip", "end clip",99.)
		o.addParam("color", "color scheme","I")
		o.addParam("fontsize", "axis font size",14)
		o.addParam("cmap", "cmap","gray")
		o.addParam("transp", "transpose axis","y")
		o.addParam("yreverse", "reverse y axis","n")
		o.addParam("xreverse", "reverse x axis","n")
		o.addParam("gainpanel", "what gain to apply","e")
		if 'cmap' in self.kw: o.addParam("cmap", "cmap",self.kw.get('cmap'))
		#if 'label1' in self.kw: o.addParam("label1", "axis 1 label",self.kw.get('label1'))
		#else: o.addParam("label1", "axis 1 label","")
		#if 'label2' in self.kw: o.addParam("label2", "axis 1 label",self.kw.get('label2'))
		#else: o.addParam("label2", "axis 1 label","")
		if 'aspect' in self.kw: o.addParam("aspect", "aspect ratio",self.kw.get('aspect'))
		else: o.addParam("aspect", "aspect ratio","auto")
		if 'title' in self.kw: o.addParam("title", "title ratio",self.kw.get('title'))
		else: o.addParam("title", "title ratio","")
		if 'figsize' in self.kw: o.addParam("figsize", "figure size in inches",self.kw.get('figsize'))
		else: o.addParam("figsize", "figure size in inches",(7,9))
		return o

	def getClips(self):
		self.bp=self.getParam("bpclip")
		self.ep=self.getParam("epclip")
		gp=self.getParam("gainpanel")
		gain=True;
		self.dims=numpy.shape(self.array)
		self.gainPanel=False
		if gp[0]=="e":
			self.gainPanel=False
			b_val=None
			e_val=None
		elif gp[0]=="a":
			b_val,e_val=numpy.percentile(self.array,[self.bp,self.ep])
		else:
			try:
				self.gainPanel=int(gp)
			except valueError:
				self.gainPanel=0
			if len(dims) ==2:
				b_val,e_val=numpy.percentile(self.array,[self.bp,self.ep])
			elif len(dims) ==3:
				b_val,e_val=numpy.percentile(self.array[self.gainPanel,:,:],[self.bp,self.ep])
			elif len(dims)==4:
				b_val,e_val=numpy.percentile(self.array[0,self.gainPanel,:,:],[self.bp,self.ep])
		return b_val,e_val
	def pclipToClip(self,b_val,e_val):
		bclip=self.getParam("bclip")
		eclip=self.getParam("eclip")
		if not bclip:
			bclip=b_val
		if not eclip:
			eclip=e_val
		return bclip,eclip
	def getColormap(self):
		col=self.getParam("color")
		cmap=self.getParam("cmap")
		if not cmap:
			cmap=self.cmaps[col]
		return cmap
	def orrientArray(self,mat):
		o1=self.getParam("o1")
		d1=self.getParam("d1")
		o2=self.getParam("o2")
		d2=self.getParam("d2")
		n1=self.hyper.axes[0].n
		n2=self.hyper.axes[1].n

		if "y"==self.getParam("transp"):
			mat=mat.transpose()
			self.axis.set_xlabel(self.getParam("label2"))
			self.axis.set_ylabel(self.getParam("label1"))
			self.a_x=[o2,d2*n2+o2]
			self.a_y=[d1*n1+o1,o1]
		else:
			self.axis.set_xlabel(self.getParam("label1"))
			self.axis.set_ylabel(self.getParam("label2"))
			self.a_y=[o2,d2*n2+o2]
			self.a_x=[d1*n1+o1,o1]
		if "y"==self.getParam("yreverse"):
			mat=mat[::-1,:]
			self.a_y=[self.a_y[1],self.a_y[0]]
		if "y"==self.getParam("xreverse"):
			mat=mat[:,::-1]
			self.a_x=[self.a_x[1],self.a_x[0]]
		return mat
	def getAxisLimits(self):
		self.extents=[self.a_x[0],self.a_x[1],self.a_y[0],self.a_y[1]]
		return self.extents




	def output(self):
		b_val,e_val=self.getClips()
		if len(self.dims)==2 or b_val:
			b_val,e_val=numpy.percentile(self.array,[self.bp,self.ep])
			bclip,eclip=self.pclipToClip(b_val,e_val)

		if len(self.dims)==2:
			fig=self.figure.set_size_inches(self.getParam("figsize"))
			mat=numpy.clip(self.array,bclip,eclip)
			mat=self.orrientArray(mat)
			self.axis.imshow(mat,cmap=self.getColormap(),extent=self.getAxisLimits(),aspect=self.getParam("aspect"))
			self.axis.set_title(self.getParam("title"))
		else:
			ims=[]
			fig=self.figure.set_size_inches(self.getParam("figsize"))
			if len(self.dims)==3:
				for i3 in range(self.dims[0]):
					if not self.gainPanel:
						b_val,e_val=numpy.percentile(self.array[i3,:,:],[self.bp,self.ep])
						bclip,eclip=self.pclipToClip(b_val,e_val)
					mat=numpy.clip(self.array[i3,:,:],bclip,eclip)
					mat=self.orrientArray(mat)
#					im=self.plt.imshow(mat,animated=True)
					im=self.axis.imshow(mat,cmap=self.getColormap(),animated=True,
								extent=self.getAxisLimits(),aspect=self.getParam("aspect"),zorder=1)
					self.axis.set_title(self.getParam("title"))
					ims.append([im])
				#self.plt.show()
			if len(self.dims)==4:
				for i4 in range(self.dims[0]):
					for i3 in range(self.dims[1]):
						if not self.gainPanel:
							b_val,e_val=numpy.percentile(self.array[i4,i3,:,:],[self.bp,self.ep])
							bclip,eclip=self.pclipToClip(b_val,e_val)
						mat=numpy.clip(self.array[i4,i3,:,:],bclip,eclip)
						mat=self.orrientArray(mat)
						ims.append(self.plt.imshow(mat,cmap=self.getColormap(),animated=True,
								extent=self.getAxisLimits(),aspect=self.getParam("aspect"),zorder=1))
			ani = animation.ArtistAnimation(fig, ims, interval=500
					, blit=True,repeat=True,
                                repeat_delay=0)
			self.plt.close()
			HTML(ani.to_jshtml())
			return ani


class Graph(sepPlot_custom.sepPlot):
	def __init__(self,plt,data,**kw):
		"""Initiatlize Graph object
		   plt  -   matplotlib plt object
		   data -   data (must be inherited SepVector.vector)
		   kw   -   Optional arguments
		"""
		self.kw=kw
		super().__init__(plt,data,kw)
		self.plt=plt
		self.checkLogic()
		self.data=data
	def setDefaults(self):
		o = super().setDefaults()
		o.addParam("title", "graph title ","")
		if 'label1' in self.kw: o.addParam("label1", "axis 1 label",self.kw.get('label1'))
		else: o.addParam("label1", "axis 1 label","")
		if 'label2' in self.kw: o.addParam("label2", "axis 1 label",self.kw.get('label2'))
		else: o.addParam("label2", "axis 1 label","")
		if 'legend' in self.kw: o.addParam("legend", "legend",self.kw.get('legend'))
		else: o.addParam("legend", "legend","")
		o.addParam("o1", "axis 1 origin",self.hyper.axes[0].o)
		o.addParam("d1", "axis 1 discretization ",self.hyper.axes[0].d)
		o.addParam("bpclip", "bottom clip",1.)
		o.addParam("epclip", "end clip",99.)
		o.addParam("Color", "color scheme","I")
		o.addParam("fontsize", "axis font size",14)
		o.addParam("cmap", "cmap","gray")
		if 'grid' in self.kw: o.addParam("grid", "grid on",self.kw.get('grid'))
		else: o.addParam("grid", "grid on","n")
		if 'transp' in self.kw: o.addParam("transp", "transpose axis",self.kw.get('transp'))
		else: o.addParam("transp", "transpose axis","y")
		if 'yreverse' in self.kw: o.addParam("yreverse", "reverse y axis",self.kw.get('yreverse'))
		else: o.addParam("yreverse", "reverse y axis","n")
		if 'xreverse' in self.kw: o.addParam("xreverse", "reverse y axis",self.kw.get('xreverse'))
		else: o.addParam("xreverse", "reverse x axis","n")
		o.addParam("gainpanel", "what gain to apply","e")
		if 'aspect' in self.kw: o.addParam("aspect", "aspect ratio",self.kw.get('aspect'))
		else: o.addParam("aspect", "aspect ratio","auto")
		if 'title' in self.kw: o.addParam("title", "title ratio",self.kw.get('title'))
		else: o.addParam("title", "title ratio","")
		if 'figsize' in self.kw: o.addParam("figsize", "figure size in inches",self.kw.get('figsize'))
		else: o.addParam("figsize", "figure size in inches",(7,9))
		o.addParam("styles", " styles",["k-","r-","g-","b-","c-","m-","y-"])
		return o
	def checkLogic(self):
		"""Check to make sure we have data that we can plot.
		   For now it must be 1 or 2-D array"""

		n3=1
		for i in range(2,len(self.hyper.axes)):
			n3=n3*self.hyper.axes[i]
		if n3>1:
			raise Exception("For now graph can only plot 1- and 2-D arrays")
	def getDomains(self):
		"""Get domains that we need to plot"""
		domains=[]
		if isinstance(self.data,SepVector.ComplexVector):
			for i2 in range(self.hyper.axes[0].n):
				domains.append(self.data.getNdArray()[i2,:].real)
		else:
			for i2 in range(self.hyper.axes[0].n):
				domains.append(numpy.arange(self.getParam("o1"),self.getParam("o1")+self.getParam("d1")*self.hyper.axes[0].n,self.getParam("d1")))
		return domains

	def getRanges(self):
		"""Get ranges that we need to plot"""
		rangeA=[]
		if isinstance(self.data,SepVector.ComplexVector):
			if self.hyper.getNdim() == 2:
				for i2 in range(self.hyper.axes[1].n):
					rangeA.append(self.data.getNdArray()[:,i2].imag)
			else: rangeA.append(self.data.getNdArray()[:].imag)
		else:
			if self.hyper.getNdim() == 2:
				for i2 in range(self.hyper.axes[1].n):
					rangeA.append(self.data.getNdArray()[i2,:])
			else: rangeA.append(self.data.getNdArray()[:])

		return rangeA
	def orientArray(self,xin,yin):
		"""Orient plot depending on options given"""
		if "y"==self.getParam("transp"):
			self.plt.xlabel(self.getParam("label2"))
			self.plt.ylabel(self.getParam("label1"))
			yout=xin
			xout=yin
		else:
			self.plt.xlabel(self.getParam("label1"))
			self.plt.ylabel(self.getParam("label2"))
			xout=xin
			yout=yin
		xmin=1e31
		xmax=-1e31
		ymin=1e31
		ymax=-1e31
		for i in range(len(xout)):
			xmin=min(xout[i].min(),xmin)
			xmax=max(xout[i].max(),xmax)
			ymin=min(yout[i].min(),ymin)
			ymax=max(yout[i].max(),ymax)

		a_x=[xmin,xmax]
		a_y=[ymin,ymax]
		if "y"==self.getParam("yreverse"):
			yout=numpy.flip(yout)
			#self.a_y=[self.a_y[1],self.a_y[0]]
		if "y"==self.getParam("xreverse"):
			xout=numpy.flip(xout)
			#self.a_x=[self.a_x[1],self.a_x[0]]
		return xout,yout
	def getRotatedParms(self, i, field):
		fields = self.getParam(field)
		if not isinstance(fields, list):
			raise Exception("Expecting %s to be a list" % field)
		mod = i % len(fields)
		return fields[mod]
	def output(self):
		"""Output a graph"""
		domains=self.getDomains()
		rangeA=self.getRanges()
		xout,yout=self.orientArray(domains,rangeA)
		out=[]
		for i in range(len(xout)):
			out.append(xout[i])
			out.append(yout[i])
			out.append(self.getRotatedParms(i,"styles"))
		fig = self.plt.figure(figsize=self.getParam("figsize"))
		self.plt.rcParams["figure.figsize"] = self.getParam("figsize")
		self.plt.plot(*out)
		if(self.getParam("grid")=='y'): self.plt.grid(True)
		self.plt.xlabel(self.getParam("label2"))
		self.plt.ylabel(self.getParam("label1"))
		self.plt.title(self.getParam("title"))
		self.plt.legend(self.getParam("legend"),loc='upper right')
