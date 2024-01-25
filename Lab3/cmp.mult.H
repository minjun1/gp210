No input header 

Su2sep:   bob@kana   Wed Nov  1 16:39:18 2000
		sets next: in="/net/kana/scr4/antoine/gulf.shots.H@"
		hff="gulf.shots.H@@"
		same_record_number=1
	n1=2404  o1=4e-06  d1=0.004  label1="none"  unit1="none"
		gff="-1"
		esize=4
		data_format="xdr_float"
		same_record_number=1
	 	n2=180180 o2=1 d2=1 label2="trace number"
	n1=2404  o1=4e-06  d1=0.004  label1="none"  unit1="none"
		gff="-1"
		esize=4


Headermath:   antoine@kana   Fri Nov  3 12:42:24 2000
		sets next: in="/net/kana/antoine/gulf.3d.math.H@"
		eqn1="sx"
		eqn2="gx"
		eqn3="-offset"
		eqn4="0.5*(gx+sx)"
		eqn5="-offset/2."
		hff="gulf.3d.math.H@@"
		sets next: in="/net/kana/scr4/antoine/gulf.shots.H@"
		data_format="xdr_float"



Sort3d:   antoine@kana   Fri Nov  3 15:04:25 2000
		sets next: in="/net/kana/antoine/gulf.sort.H@"
		Read  from param: #max_memory=10
		Read  from param: #synch=0
		Read  from param: #compress_tr=1
		Read  from param: #grid_fold=0
		Read  from param: #nkeys=2
		Read  from param: #verb=1
		Read  from param: #debug=1
		Read  from param: #just_grid=0
		Read  from param: #preserve_nd=0
		Read  from param: #plane="none"
		hff="gulf.sort.H@@"
		gff="gulf.sort.H@@@@"
		sets next: in="/net/kana/scr4/antoine/gulf.shots.H@"
		same_record_number=0
	n3=1 n4=1 n5=1 n6=1 n7=1 n8=1
		data_format="xdr_float"



Infill3d:   antoine@kana   Fri Nov  3 15:04:42 2000
		sets next: in="/net/kana/scr4/antoine/gulf.shots2.H@"
		Read  from param: #maxsize=10
		Read  from param: #verb=0
	n2=180  o2=330  d2=87.5  label2="offset_x"  unit2="unit2"
	n3=1000  o3=0  d3=87.5  label3="s_x"  unit3="unit3"
		gff="-1"
		hff="-1"
	n1=2404  o1=4e-06  d1=0.004  label1="none"  unit1=""
		hff="-1"
		gff="-1"
		esize=4
		data_format="xdr_float"



Window:   antoine@kana   Fri Nov 10 11:32:52 2000
		sepstr_ready_out() : sets next in="stdin"
		In:	float	Fortran (2404,180,1000,1)	C [1][1000][180][2404]
		Out:	float	Fortran (1500,180,1000,1)	C [1][1000][180][1500]
	 From History:
		 n4=1 n3=1000 n2=180 n1=2404 esize=4
	 From Par:
		 n1=1500  #f1=0  #j1=1  #min1=0.000004  #max1=5.996
		 n2=180  #f2=0  #j2=1  #min2=330.000000  #max2=15992.5
		 n3=1000  #f3=0  #j3=1  #min3=0.000000  #max3=87412.5
		 n4=1  #f4=0  #j4=1  #min4=0  #max4=0
	 Make header useful for further processing:
		 n1=1500 	 n2=180 	 n3=1000 	 n4=1
		 o1=0.000004 	 o2=330.000000 	 o3=0.000000 	 o4=0.000000
		 d1=0.004 	 d2=87.5 	 d3=87.5 	 d4=1
		 label1="none" 	 label2="offset_x" 	 label3="s_x" 	 label4=""
		data_format="xdr_float"


Reverse:   antoine@kana   Fri Nov 10 11:32:52 2000
		sepstr_ready_out() : sets next in="stdin"
	Reverse: reversing over n2.
		o2=-15992.5
		d2=87.5
		data_format="xdr_float"


Mute:   antoine@kana   Fri Nov 10 11:35:08 2000
		sepstr_ready_out() : sets next in="stdin"
		Read  from param: #vmute=5000
		Read  from param: #tmute=1.6
		Read  from param: #tramp=0.25
		Read  from param: #tpow=0
		Read  from param: #xpow=0
		Read  from param: #trcbal=0
		Read  from param: #weight=0
		Read  from param: #taper=0
		Read  from param: #eramp=0.25
		Read  from param: #emute=6
		vmute=5000
		tmute=1.6
		tramp=0.25
		tpow=0
		xpow=0
		trcbal=0
		weight=0
		taper=0
		n2=180
		n3=1001
		data_format="xdr_float"


Tpow:   antoine@kana   Fri Nov 10 11:35:08 2000
		sepstr_ready_out() : sets next in="stdin"
		n1=1500
		n2=180
		n3=1001
		d1=0.004
		o1=4e-06
		d2=87.5
		o2=-15992.5
		Given-tpow= applied_tpow=0.5
		For plotting: tpow=0
		data_format="xdr_float"


Pad:   antoine@kana   Fri Nov 10 11:46:32 2000
		sepstr_ready_out() : sets next in="stdin"
		n1=3000
		n2=180
		n3=1001
		esize=4
		data_format="xdr_float"


/net/kana/james/bin/SGI64/Transf:   antoine@kana   Fri Nov 10 11:46:33 2000
		sets next: in="/net/kana/antoine/shotfrq.H@"
		From par: dim = dim=3
		From par: esize_out = esize=8
		From par: ny_block_inp = ny_block_inp=100
		From par: f_min = f_min=5
		From par: f_max = f_max=80
		nx_out = n1=180
		ny_out = n2=1001
		nf_out = n3=901
		nhx_out = n4=1
		nhy_out = n5=1
		x0_out = o1=-15992.5
		y0_out = o2=0
		f0_out = o3=4.91667
		hx0_out = o4=0
		hy0_out = o5=0
		dx_out = d1=87.5
		dy_out = d2=87.5
		df_out = d3=0.0833333
		dhx_out = d4=1
		dhy_out = d5=1
		data_format="xdr_float"


Transp:   antoine@kana   Thu Jan 17 19:08:11 2002
		sepstr_ready_out() : sets next in="stdin"
Transposing plane 2 and 3 
Using 250 megabytes 
		junkME=0
	n2=901  o2=4.91667  d2=0.0833333   label2="s_x"   unit2="unit3"	n3=1001  o3=0  d3=87.5   label3="offset_x"   unit3="unit2"		gff="-1"
		hff="-1"
	n1=180  o1=-15992.5  d1=87.5   label1="none"		hff="-1"
		gff="-1"
		esize=8
		data_format="xdr_float"


Transp:   antoine@kana   Thu Jan 17 19:08:39 2002
		sepstr_ready_out() : sets next in="stdin"
Transposing plane 1 and 2 
Using 150 megabytes 
		junkME=0
	n2=180  o2=-15992.5  d2=87.5   label2="none"	n3=1001  o3=0  d3=87.5   label3="offset_x"   unit3="unit2"		gff="-1"
		hff="-1"
	n1=901  o1=4.91667  d1=0.0833333   label1="s_x"   unit1="unit3"		hff="-1"
		gff="-1"
		esize=8
		data_format="xdr_float"


Src/Transfinv.x:   antoine@kana   Thu Jan 17 19:08:55 2002
		sets next: in="/net/kana/scr3/antoine/junk.H@"
		n1=2048
		esize=4
		o1=0
		d1=0.00585938
		data_format="xdr_float"



Interp:   antoine@kana   Thu Jan 17 19:29:14 2002
		sepstr_ready_out() : sets next in="stdin"
	sinc interpolation with 10 points
	n1=1500 o1=0.000004 d1=0.004000
		data_format="xdr_float"


Reverse:   antoine@kana   Thu Jan 17 19:29:14 2002
		sepstr_ready_out() : sets next in="stdin"
	Reverse: reversing over n2.
		o2=330
		d2=87.5
		data_format="xdr_float"


Tpow:   antoine@kana   Thu Jan 17 19:48:13 2002
		sets next: in="/net/kana/scr3/antoine/datashot.HH@"
		n1=1500
		n2=180
		n3=1001
		d1=0.004
		o1=4e-06
		d2=87.5
		o2=330
		Given-tpow= applied_tpow=-0.5
		For plotting: tpow=0
		data_format="xdr_float"



Window:   antoine@koko   Fri Mar 15 12:03:44 2002
		sepstr_ready_out() : sets next in="stdin"
		In:	float	Fortran (1500,180,1001,1)	C [1][1001][180][1500]
		Out:	float	Fortran (1250,175,1,1)	C [1][1][175][1250]
	 From History:
		 n4=1 n3=1001 n2=180 n1=1500 esize=4
	 From Par:
		 n1=1250  #f1=250  #j1=1  #min1=1.000004  #max1=5.996
		 n2=175  #f2=5  #j2=1  #min2=767.500000  #max2=15992.5
		 n3=1  #f3=500  #j3=1  #min3=43750.000000  #max3=43750
		 n4=1  #f4=0  #j4=1  #min4=0  #max4=0
	 Make header useful for further processing:
		 n1=1250 	 n2=175 	 n3=1 	 n4=1
		 o1=1.000004 	 o2=767.500000 	 o3=43750.000000 	 o4=0.000000
		 d1=0.004 	 d2=87.5 	 d3=87.5 	 d4=1
		 label1="s_x" 	 label2="none" 	 label3="offset_x" 	 label4=""
		data_format="xdr_float"



Window3d:   stuart@storm.stanford.edu   Thu Oct 17 17:15:52 2019
		sets next: in="/net/storm/scr1/stuart/cmp.mult.H@"
#Window #f1=0  #j1=1 #n1=1250
#Window #f2=0  #j2=1 #n2=175
#Window #f3=0  #j3=1 #n3=1
		junkME=0
	n2=175  o2=767.500000  d2=87.500000   label2="none"   unit2="unit3"
	n3=1  o3=43750.000000  d3=87.500000   label3="offset_x"   unit3="unit2"
		gff="-1"
		hff="-1"
hff=-1 gff=-1  n4=1  n5=1  n6=1  n7=1  n8=1  n9=1 
	n1=1250  o1=1.000004  d1=0.004000   label1="s_x"   unit1="unit3"
		hff="-1"
		gff="-1"
		esize=4
		data_format="xdr_float"

label1=sec label2=offset(m) o2=0.234 d2=0.02667
label2='offset (km)'
label1='tau (sec)'
