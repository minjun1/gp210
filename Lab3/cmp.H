Merge: Copy of header file /r5/jon/classdata/WG.HH:

Merge: Copy of header file WG1500.H:

Merge: Copy of header file evenp.H:



sycube:   jblack@hanauma   Fri Jun 26 13:31:24 1992
		input() :    in ="stdin"
		output() : sets next in="/scr/jblack/junk1.H@"
		data_format="xdr_float"
	esize=4 n1=1525 n2=48 n3=100
	o1=0.000000 o2=1.000000 o3=1500.000000
	d1=0.004000 d2=1.000000 d3=1.000000
	label1=time label2=cdpt label3=cdp



Window:   jblack@hanauma   Fri Jun 26 13:35:08 1992
#	input history file /home/taal/r5/jon/basdata/junk1.H
		input() :    in ="/scr/jblack/junk1.H@"
		output() : sets next in="/scr/jblack/even.H@"
		data_format="xdr_float"
		In:	float	Fortran (1525,48,100,1)	C [1][100][48][1525]
		Out:	float	Fortran (1000,24,50,1)	C [1][50][24][1000]
	 From History:
		 n4=1 n3=100 n2=48 n1=1525 esize=4
	 From Par:
		 n1=1000  #f1=0  #j1=1  #min1=0  #max1=3.996
		 n2=24  #f2=1  #j2=2  #min2=2  #max2=48
		 n3=50  #f3=0  #j3=2  #min3=1500  #max3=1598
		 n4=1  #f4=0  #j4=1  #min4=0  #max4=0
	 Make header useful for further processing:
		 n1=1000 	 n2=24 	 n3=50 	 n4=1
		 o1=0 	 o2=2 	 o3=1500 	 o4=0
		 d1=0.004 	 d2=2 	 d3=2 	 d4=1
		 label1="time" 	 label2="cdpt" 	 label3="cdp" 	 label4=""



Pad:   jblack@hanauma   Fri Jun 26 13:35:45 1992
#	input history file /home/taal/r5/jon/basdata/even.H
		input() :    in ="/scr/jblack/even.H@"
		output() : sets next in="/scr/jblack/evenp.H@"
		data_format="xdr_float"
		n1=1000
		n2=24
		n3=50
		esize=4



Merge: Input header list:
	<evenp.H   in=/scr/jblack/evenp.H@
	<oddp.H   in=/scr/jblack/oddp.H@
	esize=4 n1=1000 n2=48 n3=50
	o1=0.000000 o2=2.000000 o3=1500.000000
	d1=0.004000 d2=2.000000 d3=2.000000
	axis=2


Merge:   jblack@hanauma   Fri Jun 26 13:37:58 1992
		output() : sets next in="/scr/jblack/merge.H@"
		data_format="xdr_float"

n2=24
n3=100
d2=1 d3=1


Reverse:   jblack@hanauma   Fri Jun 26 13:38:52 1992
#	input history file /home/taal/r5/jon/basdata/all1.H
		input() :    in ="/scr/jblack/merge.H@"
		output() : sets next in="/scr/jblack/all.H@"
		data_format="xdr_float"
	Reverse: reversing over n2.
		o2=25
		d2=-1

d2=1 o2=0


Mv:   jblack@hanauma   Fri Jun 26 17:39:00 1992
#	input history file /home/taal/r5/jon/basdata/all.H
		input() :    in ="/scr/jblack/all.H@"
		output() : sets next in="./WG1500.H@"
		data_format="xdr_float"



Merge: Input header list:
	<WG1500.H   in=./WG1500.H@
	<WG1600.H   in=./WG1600.H@
	<WG1700.H   in=./WG1700.H@
	<WG1800.H   in=./WG1800.H@
	esize=4 n1=1000 n2=24 n3=400
	o1=0.000000 o2=0.000000 o3=1500.000000
	d1=0.004000 d2=1.000000 d3=1.000000
	axis=3


Merge:   jblack@hanauma   Fri Jun 26 21:08:40 1992
		output() : sets next in="./WG.H@"
		data_format="xdr_float"

d2=.440 d3=.110 o2=1.085 o1=0 o3=0

vi:	jon
		in="$CLASSDATA/WG.HH@"
		CLASSDATA=/r5/jon/classdata

vi: jon guess at units
	d1=0.004000
	label1=sec

	d2=.12		# guess based on water velocity
	o2=.36		# assume a three trace lead in
	label2=km,guess

	label3=midpoint

vi: jim based on segy header information
	d2=.134          # equals 440 feet @ 0.0003048 km/ft
	o2=.264          # for the first midpoint in the dataset
			 #o2=.331 for the second midpoint in the dataset
	label2=offset(km)
	d3=.0335         # equals 110 feet
	label3=midpoint(km)

vi jon
	CDPtype=2



Merge: Input header list:
	</r5/jon/classdata/WG.HH   in=$CLASSDATA/WG.HH@
	<cdp35.HH   in=./cdp35.HH@
	<cdp1935.HH   in=./cdp1935.HH@
	<cdp1936.HH   in=./cdp1936.HH@
	<cdp2000.HH   in=./cdp2000.HH@
	<cdp2200.HH   in=./cdp2200.HH@
	esize=4 n1=1000 n2=24 n3=912
	o1=0.000000 o2=0.264000 o3=0.000000
	d1=0.004000 d2=0.134000 d3=0.033500
	axis=3


Merge:   jblack@hanauma   Sat Jul 11 12:38:44 1992
		output() : sets next in="./WG2.HH@"
		data_format="xdr_float"

vi:	in=$CLASSDATA/WG2.HH@


Window:   jon@taal   Thu Jul 16 11:27:23 1992
		input() :    in ="$CLASSDATA/WG2.HH@"
		output() : sets next in="stdout"
		data_format="xdr_float"
		In:	float	Fortran (1000,24,912,1)	C [1][912][24][1000]
		Out:	float	Fortran (1000,24,300,1)	C [1][300][24][1000]
	 From History:
		 n4=1 n3=912 n2=24 n1=1000 esize=4
	 From Par:
		 n1=1000  #f1=0  #j1=1  #min1=0  #max1=3.996
		 n2=24  #f2=0  #j2=1  #min2=0.264  #max2=3.346
		 n3=300  #f3=210  #j3=1  #min3=7.035  #max3=17.0515
		 n4=1  #f4=0  #j4=1  #min4=0  #max4=0
	 Make header useful for further processing:
		 n1=1000 	 n2=24 	 n3=300 	 n4=1
		 o1=0 	 o2=0.264 	 o3=7.035 	 o4=0
		 d1=0.004 	 d2=0.134 	 d3=0.0335 	 d4=1
		 label1="sec" 	 label2="offset(km)" 	 label3="midpoint(km)" 	 label4=""


Demean.x:   jon@taal   Thu Jul 16 11:27:23 1992
		From par: rho = rho=0.8
		output() : sets next in="$CLASSDATA/midpts.HH@"
		output(): current environment CLASSDATA="/r5/jon/classdata"
		data_format="xdr_float"



Transp:   jblack@taal   Sun Jul 26 07:55:05 1992
		input() :    in ="$CLASSDATA/midpts.HH@"
		output() : sets next in="/r5/jon/bei-old/classdata/coffs.HH@"
		output(): current environment CLASSDATA="/r5/jon/bei-old/classdata"
		data_format="xdr_float"
#	Creating work file /scr/jblack/Transpa00775
# Transp: input n1=1000  n2=24  n3=300 esize=4
#		o2=0.264000 o3=7.035000
#		d2=0.134000 d3=0.033500
#		label2="offset(km)" label3="midpoint(km)"
Transp: output n1=1000  n2=300  n3=24 esize=4
		o2=7.035000 o3=0.264000
		d2=0.033500 d3=0.134000
		label2="midpoint(km)" label3="offset(km)"



Cp:   jon@oas   Wed Jun 14 14:28:30 1995
		sepstr_ready_out() : sets next in="stdin"
#	output tag is "out" 
		data_format="xdr_float"



Cp:   jon@oas   Wed Jun 14 14:32:54 1995
		sets next: in="/scr21/jon/junk.H@"
#	output tag is "out" 
		data_format="xdr_float"



Transp:   jon@oas   Wed Jun 14 14:33:46 1995
		sepstr_ready_out() : sets next in="stdin"
#	Creating work file /scr21/jon/Transpa12118
# Transp: input n1=1000  n2=300  n3=24 esize=4
#		o2=7.035000 o3=0.264000
#		d2=0.033500 d3=0.134000
#		label2="midpoint(km)" label3="offset(km)"
Transp: output n1=1000  n2=24  n3=300 esize=4
		o2=0.264000 o3=7.035000
		d2=0.134000 d3=0.033500
		label2="offset(km)" label3="midpoint(km)"
#	output tag is "out" 
		data_format="xdr_float"



Smooth:   biondo@oas   Fri May 24 19:05:55 1996
		sepstr_ready_out() : sets next in="stdin"
		From par: rect3 = rect3=1
		From par: rect1 = rect1=2
		From par: rect2 = rect2=1
		From par: tridiag = tridiag=0
		From par: scaleup = scaleup=0
		From par: diff1 = diff1=0
		From par: diff2 = diff2=0
		From par: agc = agc=0
		From par: absval = absval=0
		From par: sum3 = sum3=0
	Data smoothed with triangle().
		Data smoothed with: rect1=2
		Data smoothed with: rect2=1
		Data smoothed with: rect3=1
#	output tag is "out" 
		data_format="xdr_float"


Window:   biondo@oas   Fri May 24 19:05:56 1996
		sepstr_ready_out() : sets next in="stdin"
		In:	float	Fortran (1000,24,300,1)	C [1][300][24][1000]
		Out:	float	Fortran (1000,24,250,1)	C [1][250][24][1000]
	 From History:
		 n4=1 n3=300 n2=24 n1=1000 esize=4
	 From Par:
		 n1=1000  #f1=0  #j1=1  #min1=0  #max1=3.996
		 n2=24  #f2=0  #j2=1  #min2=0.264  #max2=3.346
		 n3=250  #f3=20  #j3=1  #min3=7.705  #max3=16.0465
		 n4=1  #f4=0  #j4=1  #min4=0  #max4=0
	 Make header useful for further processing:
		 n1=1000 	 n2=24 	 n3=250 	 n4=1
		 o1=0 	 o2=0.264 	 o3=7.705 	 o4=0
		 d1=0.004 	 d2=0.134 	 d3=0.0335 	 d4=1
		 label1="sec" 	 label2="offset(km)" 	 label3="midpoint(km)" 	 label4=""
#	output tag is "out" 
		data_format="xdr_float"


Demean.x:   biondo@oas   Fri May 24 19:05:56 1996
		sepstr_ready_out() : sets next in="stdin"
		From par: rho = rho=0.8
#	output tag is "out" 
		data_format="xdr_float"



Window3d:   stuart@storm.stanford.edu   Thu Oct 17 08:35:04 2019
		sets next: in="/net/storm/scr1/stuart/cmp.H@"
#Window #f1=0  #j1=1 #n1=1000
#Window #f2=0  #j2=1 #n2=24
#Window #f3=0  #j3=1 #n3=1
		junkME=0
	n2=24  o2=0.264000  d2=0.134000   label2="offset(km)"   unit2="Undefined"
	n3=1  o3=7.705000  d3=0.033500   label3="midpoint(km)"   unit3="Undefined"
		gff="-1"
		hff="-1"
hff=-1 gff=-1  n4=1  n5=1  n6=1  n7=1  n8=1  n9=1 
	n1=1000  o1=0.000000  d1=0.004000   label1="sec"   unit1="Undefined"
		hff="-1"
		gff="-1"
		esize=4
		data_format="xdr_float"

