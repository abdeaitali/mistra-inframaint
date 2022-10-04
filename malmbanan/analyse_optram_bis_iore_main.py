# -----------------------------------------------------------------
#                                                   Initiate
#                                                   ---------------

# Import packages
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import os
from scipy import signal
from functions_v2 import *
import xlrd 

# Paths
home = os.getcwd()
O2_path = os.path.abspath(os.path.join(os.path.dirname(home),'DATA/section111/OPTRAM'))
O1_path = os.path.abspath(os.path.join(os.path.dirname(home),'DATA/section111/OPTRAM/alignment'))
B_path = os.path.abspath(os.path.join(os.path.dirname(home),'DATA/section111/BIS'))
S_path = os.path.abspath(os.path.join(os.path.dirname(home),'DATA/section111/SHAPE'))
IORE_path = os.path.abspath(os.path.join(os.path.dirname(home),'DATA/section111/LOCO'))


# File names
B_filename = ['tamping_and_grinding.xlsx']
B_columns = np.array([[2,3,4,7,8,9]])
O1_filename = ['cirkulärkurva.xlsx','lutning.xlsx','raklinje.xlsx','räl.xlsx','rälsförhöjning.xlsx','rälssmörjningsapparat.xlsx',
                'spårväxel.xlsx','sth.xlsx','vertikalkurva.xlsx','övergångskurva.xlsx']
O1_filename = ['cirkulärkurva.xlsx','raklinje.xlsx','rälsförhöjning.xlsx',
                'sth.xlsx','räl.xlsx','övergångskurva.xlsx']
O3_filename = 'curves_SPL_1909250857A_111_E_1417_874_20210223_1107.xlsx'
O1_columns = np.array([[1,2,8,12,14],[1,2,8,12],[1,2,8,12,15,16],[1,2,8,13,14,15,16],[1,2,8,12,15,17,22],[1,2,8,12,15,16]])
O2_filename = ['RPM_1409121027A_111_E_1417_876_20210223_1105.csv', #'RPM_1409121027A_111_E_1417_876_20210223_1106.csv',
                'RPM_1507270844A_111_E_1417_875_20210223_1106.csv','RPM_1608100911A_111_E_1417_874_20210223_1107.csv', #'RPM_1709160759A_111_E_1417_875_20210223_1108.csv',
                'RPM_1809231019A_111_E_1417_874_20210223_1109.csv','RPM_1909250857A_111_E_1417_875_20210223_1110.csv',
                'Rälslitage segment mätdata111.csv','SPL_1909250857A_111_E_1417_874_20210223_1107.csv','VIH_20200430_111_20210223_1103.csv',
                'VIH_20200501_111_20210223_1103.csv','VIV_20200430_111_20210223_1103.csv','VIV_20200501_111_20210223_1103.csv']
O2_columns = ['SAMPLE_NUMBER','CORRIDOR_CODE','SURVEY_OFFSET','CORRIDOR_OFFSET','MARKER','MARKER_OFFSET','TRACK','Samverkan rfh sidoläge (mm)','Kvalitetsklass (n/a)','Stationsområde (n/a)',\
    'Spårvidd (mm)','Kurvatur (1/m)','Rälsförhöjning (mm)','GPS-koordinater SWEREF 99 N (m)','GPS-koordinater SWEREF 99 E (m)','Std rälsförhöjning (mm)','Spårviddsändring 10m (mm)','Spårvidd 100m medel (mm)',\
        'Rälsförhöjningens ojämnhet (mm)']
O2_columns_rpm = ['SAMPLE_NUMBER','CORRIDOR_CODE','SURVEY_OFFSET','CORRIDOR_OFFSET','MARKER','MARKER_OFFSET','TRACK','Sidoslitage_V (mm)','Höjdslitage_V (mm)','Summeratslitage_V (mm)','Sidoslitage_H (mm)','Höjdslitage_H (mm)','Summeratslitage_H (mm)']
O2_columns_seg = ['Startläge','Slutläge','Radie i cirkulärdel','Räl inläggningsår H','Räl inläggningsår V']
S_filename = ['circle_section111_coordinates_v2.xlsx']
S_columns = np.array([[15,16,17,18,1]])
IORE_filename = 'Data7eApril.xlsx'
IORE_columns = ['veh_nbr','id_code','pa1','pr1','pv1','time_t','lat','lon','dir','speed']


# -----------------------------------------------------------------
#                                                   Load data
#                                                   ---------------

val_, label = open_xls(O1_path,O1_filename,O1_columns)
val_s, label_s = open_xls(S_path,S_filename,S_columns)
val_b, label_b = open_xls(B_path,B_filename,B_columns)
#val_o = open_csv(O2_path,O2_filename[10],O2_columns,'spl')
#np.save('optram_spl.npy', val_o)
val_o = np.load('optram_spl.npy',allow_pickle=True)

#val_rpm = np.zeros(5,dtype=object)
#for i in range(0,len(val_rpm)):
#    val_rpm[i] = open_csv(O2_path,O2_filename[i],O2_columns_rpm,'rpm')
#    print(i)
#np.save('optram_rpm.npy', val_rpm)
val_rpm = np.load('optram_rpm.npy',allow_pickle=True)
val_year_rpm = [2014,2015,2016,2018,2019]
##val_year_rpm = [2014,2014,2015,2016,2017,2018,2019,2020]

# IORE-data
#val_iore,label_iore = open_iore_v2(IORE_path,IORE_filename,IORE_columns)
#np.savez('iore_data_v2',a=val_iore,b=label_iore)
data = np.load('iore_data_v3.npz',allow_pickle=True)
val_iore = data['a']
label_iore = data['b']

# Load segment data
val_seg_ = open_csv(O2_path,O2_filename[5],O2_columns_seg,'seg')

# Load coordinates of curves
filename = os.path.join(O2_path,O3_filename)
wb = xlrd.open_workbook(filename) 
sheet = wb.sheet_by_index(0)
rows = sheet.nrows
cols = sheet.ncols
R_coord = np.zeros((rows-1,cols))
for i in range(1,rows):
    for j in range(0,cols):
        R_coord[i-1,j] = sheet.cell_value(i,j)

# Sort
ind_ = val_seg_[:,0]
ind = ind_.argsort()
val_seg = val_seg_[ind,:]
n,ind=np.unique(val_seg[:,0],return_index=True)
val_seg_unique = np.zeros((len(ind),len(val_seg[0,:])))
for i in range(0,len(ind)):
    #print(i)
    if i<len(ind)-1:
        year_h=np.max(val_seg[np.arange(ind[i],ind[i+1]),3])
        year_v=np.max(val_seg[np.arange(ind[i],ind[i+1]),4])
    else:
        year_h=np.max(val_seg[np.arange(ind[i],len(val_seg[:,0])),3])
        year_v=np.max(val_seg[np.arange(ind[i],len(val_seg[:,0])),4])
    
    val_seg_unique[i,:] = val_seg[ind[i],:]
    val_seg_unique[i,3] = year_v #same order as in the RPM-measurement
    val_seg_unique[i,4] = year_h

# -----------------------------------------------------------------
#                                                   Analysis
#                                                   ---------------

# Separate in different tracks
ind_track = [3,3,3,6,3,3]
ind_trackb = [0]
val_0,val_1,val_2,val_3 = sort_tracks(val_,ind_track)
valb_0,valb_1,valb_2,valb_3 = sort_tracks(val_b,ind_trackb)

# Collect data
d_min = 1*pow(10,7)
d_max = 0
for i in range(0,len(O1_filename)):

    # Curves
    if O1_filename[i] == 'cirkulärkurva.xlsx':
        R_func_0,mes,mes_label = analyse_curve(val_0[i],val_0[2],val_0[3],val_0[4],val_s[0])
        R_func_1,mes,mes_label = analyse_curve(val_1[i],val_1[2],val_1[3],val_1[4],val_s[0])
        R_func_2,mes,mes_label = analyse_curve(val_2[i],val_2[2],val_2[3],val_2[4],val_s[0])
        R_func_3,mes,mes_label = analyse_curve(val_3[i],val_3[2],val_3[3],val_3[4],val_s[0])

        # Add rail grinding
      #  maint,gauge = analyse_maint(R_func_0,valb_0,val_o)

# --------- Find curves based on Optram-data ---------
R_lim = 3000 #only account for curves with radius below this radius [m]

#x_iore = map_iore(val_iore,val_o)
O_func = analyse_optram_spl(val_o,R_func_0,R_func_1,R_func_2,R_func_3,R_lim,R_coord,val_iore,val_seg_unique)
maint,damage = analyse_maint_opt(O_func,val_b,val_rpm)
id_vehicle = [9174000010251,9174000010581,9174000012721,9174000012561]
iore = analyse_iore(O_func,val_iore,val_o,id_vehicle)

# Total length
L = d_max-d_min

# Categorize curves
R_cat_100 = np.arange(100,3000,100)
nr_cat_100,L_cat_100,cat_ryear_100,cat_veq_100,cat_prof_100,cat_maint_100,cat_gauge_100,cat_H_100,cat_i_100 = cat_curve_opt(O_func,maint,R_cat_100,damage)

R_cat_3 = [600,3000]
nr_cat_3,L_cat_3,cat_ryear_3,cat_veq_3,cat_prof_3,cat_maint_3,cat_gauge_3,cat_H_3,cat_i_3 = cat_curve_opt(O_func,maint,R_cat_3,damage)

""" # Create mapping between track segments and iore-data
d = np.zeros((len(val_iore[:,1]),1))
map_R_iore = np.empty(len(R_func_0[:,1]),dtype=object)
dist_lim = 100
for i in range(0,len(R_func_0[:,1])):
    x0,y0 = centre(R_func_0[i,7],R_func_0[i,8],R_func_0[i,9],R_func_0[i,10],R_func_0[i,0])
    r0 = np.array([x0,y0])
    R = abs(R_func_0[i,0]) #radius
    v0 = np.array([R_func_0[i,7],R_func_0[i,8]])
    v1 = np.array([R_func_0[i,9],R_func_0[i,10]])
    ind=[]
    count = 0

    if i==168:
        debug=1

    for j in range(0,len(val_iore[:,1])):
        v_iore = val_iore[j,[0,1]]
        r = np.linalg.norm(val_iore[j,[0,1]]-r0)
        v = [np.linalg.norm(v_iore-v0),np.linalg.norm(v1-v0)]
        if r<(R+20) and r>(R-20): 
            if v[0]<v[1]:
                if count==0:
                    ind = j
                    count = count+1
                else:
                    ind = np.append(ind,j)

    map_R_iore[i] = ind
    ind = [] """
    


#print(nr_cat,L_cat)
#print(R_func,nr_cat,L_cat)

# -----------------------------------------------------------------
#                                                   Figure
#                                                   ---------------

# Sort curve categories
#cat_year_sort_3,cat_year_label_3,cat_veq_sort_3,cat_veq_label_3,cat_prof_sort_3,cat_prof_label_3,cat_maint_sort_3,cat_maint_label_3,cat_gauge_sort_3,cat_gauge_label_3=sort_R_cat(cat_ryear_3,cat_veq_3,cat_prof_3,cat_maint_3,cat_gauge_3,nr_cat_3)
cat_year_sort_100,cat_year_label_100,cat_veq_sort_100,cat_veq_label_100,cat_prof_sort_100,cat_prof_label_100,cat_maint_sort_100,cat_maint_label_100,cat_gauge_sort_100,cat_gauge_label_100,cat_H_sort_100,cat_H_label_100=sort_R_cat(cat_ryear_100,cat_veq_100,cat_prof_100,cat_maint_100,cat_gauge_100,nr_cat_100,cat_H_100)


# ------------ Individual curves --------------

# Number of curves in 100 m curve radius categories
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
plt.bar(R_cat_100, nr_cat_100[0:-1], width = 90,color = 'b')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Number of curves [-]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
plt.ylim((0,65))
#plt.savefig('nr_cat_100_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()


# Length of curves in 100 m curve radius categories
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
plt.bar(R_cat_100, L_cat_100[0:-1]/1000, width = 90,color = 'b')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Length of curves [km]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
#plt.savefig('L_cat_100_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()


# Stacked year
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
ax.bar(R_cat_100, cat_year_sort_100[:,0], width = 90,color = 'b', label = 'Before year 2005')
ax.bar(R_cat_100, cat_year_sort_100[:,1], bottom = cat_year_sort_100[:,0],width = 90,color = 'r', label = 'Between 2005-2010')
ax.bar(R_cat_100, cat_year_sort_100[:,2], bottom = cat_year_sort_100[:,0]+cat_year_sort_100[:,1],width = 90,color = 'g', label = 'Between 2010-2015')
ax.bar(R_cat_100, cat_year_sort_100[:,3], bottom = cat_year_sort_100[:,0]+cat_year_sort_100[:,1]+cat_year_sort_100[:,2],width = 90,color = 'm', label = 'After 2015')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Number of curves [-]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
plt.ylim((0,65))
ax.legend(fontsize=22)
#plt.savefig('year_cat_100_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Stacked veq
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
ax.bar(R_cat_100, cat_veq_sort_100[:,0], width = 90,color = 'b', label = r'$\itv_{\rmSTH} - \itv_{\rmeq}<$' r'$20 \ $' r'$\rm{km/h}$')
ax.bar(R_cat_100, cat_veq_sort_100[:,1], bottom = cat_veq_sort_100[:,0],width = 90,color = 'r', label = r'$20 \ \rm{km/h}$' r'$\leq$' r'$\itv_{\rmSTH} - \itv_{\rmeq}$' r'$<$' r'$35 \ \rm{km/h}$')
ax.bar(R_cat_100, cat_veq_sort_100[:,2], bottom = cat_veq_sort_100[:,0]+cat_veq_sort_100[:,1],width = 90,color = 'g', label = r'$35 \ \rm{km/h}$' r'$\leq$' r'$\itv_{\rmSTH} - \itv_{\rmeq}$' r'$<$' r'$50 \ \rm{km/h}$')
ax.bar(R_cat_100, cat_veq_sort_100[:,3], bottom = cat_veq_sort_100[:,0]+cat_veq_sort_100[:,1]+cat_veq_sort_100[:,2],width = 90,color = 'm', label = r'$\itv_{\rmSTH} - \itv_{\rmeq}>$' r'$50 \ $' r'$\rm{km/h}$')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Number of curves [-]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
plt.ylim((0,65))
ax.legend(fontsize=22)
#plt.savefig('veq_cat_100_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Stacked prof
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
ax.bar(R_cat_100, cat_prof_sort_100[:,0], width = 90,color = 'b', label = 'MB6')
ax.bar(R_cat_100, cat_prof_sort_100[:,1], bottom = cat_prof_sort_100[:,0],width = 90,color = 'r', label = '60E1')
#ax.bar(R_cat_100, cat_prof_sort_100[:,2], bottom = cat_prof_sort_100[:,0]+cat_prof_sort_100[:,1],width = 90,color = 'g', label = 'BV')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Number of curves [-]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
plt.ylim((0,65))
ax.legend(fontsize=22)
#plt.savefig('prof_cat_100_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()


# Stacked grinding
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
ax.bar(R_cat_100, cat_maint_sort_100[:,0], width = 90,color = 'b', label = 'Average grinding interval ' r'$\leq$' ' 1 year')
ax.bar(R_cat_100, cat_maint_sort_100[:,1], bottom = cat_maint_sort_100[:,0],width = 90,color = 'r', label = 'Average grinding interval between 1 - 2 years')
ax.bar(R_cat_100, cat_maint_sort_100[:,2], bottom = cat_maint_sort_100[:,0]+cat_maint_sort_100[:,1],width = 90,color = 'g', label = 'Average grinding interval between 2 - 3 years')
ax.bar(R_cat_100, cat_maint_sort_100[:,3], bottom = cat_maint_sort_100[:,0]+cat_maint_sort_100[:,1]+cat_maint_sort_100[:,2],width = 90,color = 'm', label = 'Average grinding interval > 3 years')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Number of curves [-]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
plt.ylim((0,65))
ax.legend(fontsize=22)
#plt.savefig('maint_cat_100_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Stacked gauge
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
ax.bar(R_cat_100, cat_gauge_sort_100[:,0], width = 90,color = 'b', label = 'Average gauge widening ' r'$\leq$' ' 5 mm')
ax.bar(R_cat_100, cat_gauge_sort_100[:,1], bottom = cat_gauge_sort_100[:,0],width = 90,color = 'r', label = 'Average gauge widening between 5 - 10 mm')
ax.bar(R_cat_100, cat_gauge_sort_100[:,2], bottom = cat_gauge_sort_100[:,0]+cat_gauge_sort_100[:,1],width = 90,color = 'g', label = 'Average gauge widening between 10 - 15 mm')
ax.bar(R_cat_100, cat_gauge_sort_100[:,3], bottom = cat_gauge_sort_100[:,0]+cat_gauge_sort_100[:,1]+cat_gauge_sort_100[:,2],width = 90,color = 'm', label = 'Average gauge widening > 15 mm')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Number of curves [-]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
plt.ylim((0,65))
ax.legend(fontsize=22)
#plt.savefig('gauge_cat_100_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Stacked H-damage
plt.figure(1,figsize=(14,6)) #passage 1
ax = plt.axes()
ax.bar(R_cat_100, cat_H_sort_100[:,0], width = 90,color = 'b', label = r'$\Delta\itH$' ' less than 0.33 mm/year')
ax.bar(R_cat_100, cat_H_sort_100[:,1], bottom = cat_H_sort_100[:,0],width = 90,color = 'r', label = r'$\Delta\itH$' ' between 0.33 - 0.66 mm/year')
ax.bar(R_cat_100, cat_H_sort_100[:,2], bottom = cat_H_sort_100[:,0]+cat_H_sort_100[:,1],width = 90,color = 'g', label =  r'$\Delta\itH$' ' between 0.66 - 1 mm/year')
ax.bar(R_cat_100, cat_H_sort_100[:,3], bottom = cat_H_sort_100[:,0]+cat_H_sort_100[:,1]+cat_H_sort_100[:,2],width = 90,color = 'm', label = r'$\Delta\itH$' ' larger than 1 mm/year')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel('Number of curves [-]',fontsize=24,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
plt.xlim((100,3000))
plt.ylim((0,65))
ax.legend(fontsize=22)
plt.savefig('H_cat_100_fig.svg',bbox_inches='tight')
#plt.close()
plt.show()



"""
# ------------ 3 categories --------------

# Number of curves in 3 categories
plt.figure(1,figsize=(6,6))
ax = plt.axes()
plt.bar(np.arange(0,3,1), nr_cat_3, width = 0.8,color = 'b')
plt.xticks(np.arange(0,3,1)-1/2, [0,600,3000])
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('Number of curves [-]',fontsize=20,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=20,labelpad=10)
plt.xlim((-0.5,1.7))
plt.ylim((0,125))
#plt.savefig('nr_cat_3_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Length of curves in 3 categories
plt.figure(1,figsize=(6,6)) #passage 1
ax = plt.axes()
plt.bar(np.arange(0,3,1), L_cat_3/1000, width = 0.8,color = 'b')
plt.xticks(np.arange(0,3,1)-1/2, [0,600,3000])
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('Length of curves [km]',fontsize=20,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=20,labelpad=10)
plt.xlim((-0.5,1.7))
#plt.ylim((0,125))
#plt.savefig('L_cat_3_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Stacked year
plt.figure(1,figsize=(6,6))
ax = plt.axes()
ax.bar(np.arange(0,2,1), cat_year_sort_3[:,0], width = 0.8,color = 'b', label = 'Before year 2005')
ax.bar(np.arange(0,2,1), cat_year_sort_3[:,1], bottom = cat_year_sort_3[:,0],width = 0.8,color = 'r', label = 'Between 2005-2010')
ax.bar(np.arange(0,2,1), cat_year_sort_3[:,2], bottom = cat_year_sort_3[:,0]+cat_year_sort_3[:,1],width = 0.8,color = 'g', label = 'Between 2010-2015')
ax.bar(np.arange(0,2,1), cat_year_sort_3[:,3], bottom = cat_year_sort_3[:,0]+cat_year_sort_3[:,1]+cat_year_sort_3[:,2],width = 0.8,color = 'm', label = 'After 2015')
plt.xticks(np.arange(0,3,1)-1/2, [0,600,3000])
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('Number of curves [-]',fontsize=20,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=20,labelpad=10)
plt.xlim((-0.5,1.7))
plt.ylim((0,125))
ax.legend(fontsize=18,loc='upper center',bbox_to_anchor=(1.8, 0.7))
#plt.savefig('year_cat_3_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Stacked grinding
plt.figure(1,figsize=(6,6))
ax = plt.axes()
ax.bar(np.arange(0,2,1), cat_maint_sort_3[:,0], width = 0.8,color = 'b', label = 'Average grinding interval ' r'$\leq$' ' 1 year')
ax.bar(np.arange(0,2,1), cat_maint_sort_3[:,1], bottom = cat_maint_sort_3[:,0],width = 0.8,color = 'r', label = 'Average grinding interval between 1 - 2 years')
ax.bar(np.arange(0,2,1), cat_maint_sort_3[:,2], bottom = cat_maint_sort_3[:,0]+cat_maint_sort_3[:,1],width = 0.8,color = 'g', label = 'Average grinding interval between 2 - 3 years')
ax.bar(np.arange(0,2,1), cat_maint_sort_3[:,3], bottom = cat_maint_sort_3[:,0]+cat_maint_sort_3[:,1]+cat_maint_sort_3[:,2],width = 0.8,color = 'm', label = 'Average grinding interval > 3 years')
plt.xticks(np.arange(0,3,1)-1/2, [0,600,3000])
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('Number of curves [-]',fontsize=20,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=20,labelpad=10)
plt.xlim((-0.5,1.7))
plt.ylim((0,125))
ax.legend(fontsize=18,loc='upper center',bbox_to_anchor=(1.8, 0.7))
#plt.savefig('maint_cat_3_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()

# Stacked gauge
plt.figure(1,figsize=(6,6))
ax = plt.axes()
ax.bar(np.arange(0,2,1), cat_gauge_sort_3[:,0], width = 0.8,color = 'b', label = 'Average gauge widening ' r'$\leq$' ' 5 mm')
ax.bar(np.arange(0,2,1), cat_gauge_sort_3[:,1], bottom = cat_gauge_sort_3[:,0],width = 0.8,color = 'r', label = 'Average gauge widening between 5 - 10 mm')
ax.bar(np.arange(0,2,1), cat_gauge_sort_3[:,2], bottom = cat_gauge_sort_3[:,0]+cat_gauge_sort_3[:,1],width = 0.8,color = 'g', label = 'Average gauge widening between 10 - 15 mm')
ax.bar(np.arange(0,2,1), cat_gauge_sort_3[:,3], bottom = cat_gauge_sort_3[:,0]+cat_gauge_sort_3[:,1]+cat_gauge_sort_3[:,2],width = 0.8,color = 'm', label = 'Average gauge widening > 15 mm')
plt.xticks(np.arange(0,3,1)-1/2, [0,600,3000])
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('Number of curves [-]',fontsize=20,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=20,labelpad=10)
plt.xlim((-0.5,1.7))
plt.ylim((0,125))
ax.legend(fontsize=18,loc='upper center',bbox_to_anchor=(1.8, 0.7))
#plt.savefig('gauge_cat_3_fig.svg',bbox_inches='tight')
plt.close()
#plt.show()












# Length of curves in 100 m curve radius categories
plt.figure(1,figsize=(6,6)) #passage 1
ax = plt.axes()
plt.bar(R_cat_100, L_cat_100[0:-1]/1000, width = 90,color = 'b')
plt.xticks(np.arange(100,3100,100)-100/2, np.arange(100,3100,100),rotation=45) #('','','','',500,'','','','',1000,'','','','',1500,'','','','',2000,'','','','',2500,'','','','',3000)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('Length of curves [km]',fontsize=20,labelpad=10)
plt.xlabel('Curve radius [m]',fontsize=20,labelpad=10)
plt.xlim((100,3000))
plt.show()


ax.pcolor(Freq[ind_freq[0],:],Time[ind_freq[0],:], 10*np.log10(np.divide(LdB[ind_freq[0],:],pow(a_ref,2))), vmin=v_a_min,vmax=v_a_max,cmap='viridis',edgecolors='face')
ax.set_xticks(np.log10(f_ticks))
x_labels = ax.get_xticklabels()
for i in range(len(x_labels)):
    if i>0:
        x_labels[i] = int(f_ticks[i])
    else:
        x_labels[i] = f_ticks[i]
ax.set_xticklabels(x_labels)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylabel('Time [s]',fontsize=20)
plt.xlabel('Frequency [Hz]',fontsize=20)
plt.xticks(rotation=90)
ax.invert_xaxis()
plt.ylim((0.1,5.2))
#ax.set_yticks([0,1,2,3,4,5,6,7,8,9,10,11])
#plt.savefig('acc_spec_X50_Torp_201113_sim.jpg',bbox_inches='tight')


# -----------------------------------------------------------------
#                                                   Figure to locate curves
#                                                   ---------------

ind_R = 9
ind_x = 2

x_min = 120000
x_max = 130000

ind = np.intersect1d(np.where(val_o[:,ind_x]>x_min),np.where(val_o[:,ind_x]<x_max))
plt.figure(1,figsize=(10,5))
ax = plt.gca()
plt.plot(val_o[ind,ind_x],val_o[ind,ind_R],linewidth=2)
plt.xlabel('Track following coordinate [m]',fontsize=20)
plt.ylabel('Curvature [1/m]',fontsize=20)
ax.tick_params(axis="both", labelsize=18)
plt.show()
"""