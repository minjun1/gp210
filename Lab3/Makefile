### Makefile for GP210 Homework 3
SEPINC=/opt/SEP/SEP7.0/include
include $(SEPINC)/SEP.top

SRCDIR = ./Src
OBJDIR = ./Obj
MODDIR = ./Mod
BINDIR = ./Bin
RESDIR = ./Fig
DATDIR = /net/server2/book/bei/Data

S = ${SRCDIR}
O = ${OBJDIR}
M = ${MODDIR}
B = ${BINDIR}
R = ${RESDIR}
D = ${DATDIR}

UF90LIBS = ${GEELIB}
UF90FLAGS = -C -module ${M}

################################################################################

cmp.H:
	Window3d < ${D}/midpts.HH n3=1 > $@

cmp.mult.H:
	Window3d < ${D}/gomdata.H > $@
	echo "label1=sec label2=offset(m) o2=0.234 d2=0.02667" >> $@

# For the interactive steps


#vrms0.H Nmo0.H: cmp.H ${B}/Vrms1.x
#	${SPCUBE} cmp.H nmo=1 v0=1.4 dv=0.02 nv=60 nviews=3
#	${B}/Vrms1.x < cmp.H > vrms0.H
#	Graph < vrms0.H transp=1 yreverse=1 label2="NMO velocity(km/s)" title=" " | Tube &
#	Vconvert intype=2 outtype=1 invelopt=1 inpar=1 < vrms0.H > vint0.H
#	NMO velfile=vrms0.H < cmp.H > Nmo0.H
#	make ${R}/vel0.v
#	make ${R}/nmo0.v
#	Grey < Nmo0.H | Tube &

v_pick: cmp.HH 
	./Sep_cube cmp.HH nmo=1 v0=1.4 dv=0.02 nv=60 nviews=3

v_pick_mult: cmp.mult.HH
	./Sep_cube cmp.mult.HH nmo=1 v0=1.4 dv=0.02 nv=60 nviews=3

################################################################################

# Figures

labels  = title=" " label1="time (s)" 
range   = min2=1.300 max2=3.500
intplot = wantaxis=0 wantframe=0 dash=1 plotcol=5

graph = Graph ${labels} >/dev/null ${range} yreverse=1 transp=y label2="velocity (km/s)"
grey  = Grey ${labels} >/dev/null label2="offset (km)" 
greyWindow  = Grey ${labels} >/dev/null label2="offset (km)" 
wiggle = Wiggle ${labels} >/dev/null label2="offset (km)" transp=1 yreverse=1

${R}/v1.v:
	Spike n1=100 n2=100 | Scale rscale=0. | $(graph) out=${R}/pp.v
	vppen < ${R}/pp.v vpstyle=n xscale=0.5 txscale=1.3 tyscale=1.3 > $@
	cp ${R}/v1.v ${R}/vel.0.v
	cp ${R}/v1.v ${R}/vel.1.v
	cp ${R}/v1.v ${R}/vel.2.v
	cp ${R}/v1.v ${R}/vel.3.v
	rm -f ${R}/pp.v

${R}/cmpWiggle.v: cmp.H
	$(wiggle) out=${R}/pp.v < cmp.H 
	vppen < ${R}/pp.v vpstyle=n xscale=0.5 txscale=1.3 tyscale=1.3 > $@
	rm -f ${R}/pp.v

${R}/cmpWindow.v: cmp.H
	Window  < cmp.H n1=300 f1=699 | $(greyWindow) out=${R}/pp.v 
	vppen < ${R}/pp.v vpstyle=n xscale=0.5 txscale=1.3 tyscale=1.3 > $@
	rm -f ${R}/pp.v

${R}/cmp.v: cmp.H
	$(grey) out=${R}/pp.v < cmp.H 
	vppen < ${R}/pp.v vpstyle=n xscale=0.5 txscale=1.3 tyscale=1.3 > $@
	rm -f ${R}/pp.v

${R}/cmp.mult.v: cmp.mult.H
	$(grey) out=${R}/pp.v < cmp.mult.H 
	vppen < ${R}/pp.v vpstyle=n xscale=0.5 txscale=1.3 tyscale=1.3 > $@
	rm -f ${R}/pp.v

${R}/vel%.v: Nmo%.H
	$(graph) < vrms$*.H out=${R}/rms$*.v 	
	$(graph) dash=3 < vint$*.H out=${R}/int$*.v 
	vp_Overlay ${R}/rms$*.v ${R}/int$*.v > $@

${R}/nmo%.v: Nmo%.H
	$(grey) out=${R}/pp.v < Nmo$*.H 
	vppen < ${R}/pp.v vpstyle=n xscale=0.5 txscale=1.3 tyscale=1.3 > $@
	rm -f ${R}/pp.v

#${R}/comp.vel.v: ${R}/vel.1.v ${R}/vel.2.v
#	vp_SideBySideAniso ${R}/vel.1.v ${R}/vel.2.v > $@

#${R}/comp.nmo.v: ${R}/nmo.1.v ${R}/nmo.2.v
#	vp_SideBySideAniso ${R}/nmo.1.v ${R}/nmo.2.v > $@

################################################################################

# clean and Burn

clean: jclean

burn: clean
	rm -f ${B}/*
	rm -f ${O}/*
	rm -f ${M}/*
	rm -f ${R}/*.pdf
	rm -f ${R}/*.ps
	rm -f ${R}/*.v*

################################################################################

default: ${R}/cmp.pdf ${R}/cmp.mult.pdf ${R}/vel0.pdf ${R}/vel1.pdf ${R}/vel2.pdf ${R}/vel3.pdf ${R}/nmo0.pdf ${R}/nmo1.pdf ${R}/nmo2.pdf ${R}/nmo3.pdf

include ${SEPINC}/SEP.bottom
