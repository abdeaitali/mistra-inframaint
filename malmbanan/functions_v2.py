# -----------------------------------------------------------------
#                                                   Initiate
#                                                   ---------------

# Import packages
import numpy as np
import pandas as pd
import xlrd 
import os
#from datetime import datetime
import csv
import datetime

# -----------------------------------------------------------------
#                                                   Functions
#                                                   ---------------

def convert(lamb,phi):

    # Parameters
    a = 6378137
    f = 1/298.257222101
    lambda_0=15*np.pi/180
    dlambda = lamb*np.pi/180-lambda_0
    phi = phi*np.pi/180
    k0 = 0.9996
    FN = 0
    FE = 500000

    # Calculate help-variables
    eq = f*(2-f)
    n = f/(2-f)
    ah = a/(1+n)*(1+1/4*np.power(n,2)+1/64*np.power(n,4))
    A = eq
    B = 1/6*(5*np.power(eq,2)-np.power(eq,3))
    C = 1/120*(104*np.power(eq,3)-45*np.power(eq,4))
    D = 1/1260*(1237*np.power(eq,4))
    phis = phi-np.sin(phi)*np.cos(phi)*(A+B*np.power(np.sin(phi),2)+C*np.power(np.sin(phi),4)+D*np.power(np.sin(phi),6))
    xip = np.arctan(np.tan(phis)/np.cos(dlambda))
    etap = np.arctanh(np.cos(phis)*np.sin(dlambda))

    beta1 = 1/2*n-2/3*np.power(n,2)+5/16*np.power(n,3)+41/180*np.power(n,4)
    beta2 = 13/48*np.power(n,2)-3/5*np.power(n,3)+557/1440*np.power(n,4)
    beta3 = 61/240*np.power(n,3)-103/140*np.power(n,4)
    beta4 = 49561/161280*np.power(n,4)

    # Calculate coordinates in SWEREF 99 TM
    y = k0*ah*(xip+beta1*np.sin(2*xip)*np.cosh(2*etap)+beta2*np.sin(4*xip)*np.cosh(4*etap)+beta3*np.sin(6*xip)*np.cosh(6*etap)+beta4*np.sin(8*etap)*np.cosh(8*etap))+FN
    x = k0*ah*(etap+beta1*np.cos(2*xip)*np.sinh(2*etap)+beta2*np.cos(4*xip)*np.sinh(4*etap)+beta3*np.cos(6*xip)*np.sinh(6*etap)+beta4*np.cos(8*etap)*np.sinh(8*etap))+FE

    if np.isnan(x) or np.isnan(y):
        debug = 1
   
    return x,y

def open_iore(path,name,column_labels):
    file_iore = os.path.join(path,name)
    wb = pd.read_csv(file_iore)
    w=pd.DataFrame(wb,columns=column_labels)
    n = np.size(w,0)
    val = np.zeros(len(column_labels),dtype=object)
    val_ = np.zeros(len(column_labels),dtype=object)

    count = 0
    for i in range(1,n):
        
        # Variables
        date = w[column_labels[0]][i]
        lat = w[column_labels[1]][i]
        lon = w[column_labels[2]][i]
        Econsum = w[column_labels[3]][i]
        Eregen = w[column_labels[4]][i]
        alt = w[column_labels[5]][i]
        dist = w[column_labels[6]][i]
        
        var = np.isnan(lat) 
        if not var:
            E,N = convert(lon,lat)
            if count==0:
                val[0:7] = [E,N,date,Econsum,Eregen,alt,dist]    
                count = count+1
            else:
                val_[0:7] = [E,N,date,Econsum,Eregen,alt,dist]    
                
            val=np.vstack((val,val_))  

    return val


def open_csv(path,name,column_labels,flag):
    filename = os.path.join(path,name)
    data = csv.reader(open(filename), delimiter=";")
    next(data)    
    val = []
    if flag == 'spl':
        for row in data:
            val.append([int(row[0]),int(row[1]),float(row[2]),float(row[4])*pow(10,3)+float(row[5]),row[6],float(row[7]),float(row[8]),float(row[9]),float(row[24]),float(row[25]),\
                float(row[26]),float(row[28]),float(row[29]),float(row[35]),float(row[39]),float(row[40]),float(row[41])])
        val_o = np.zeros((len(val),16),dtype=object)
    
    elif flag == 'seg':
        for row in data:
            v1=row[1].split()
            v2=row[2].split()
            v3=row[122].split()
            if len(v3)>0:
                R = float(row[122])
            else:
                R = 0
            val.append([float(v1[0])*pow(10,3)+float(v1[2]),float(v2[0])*pow(10,3)+float(v2[2]),R,int(row[123]),int(row[124])])
        val_o = np.zeros((len(val),5),dtype=object)
    
    
    else: #rpm
        for row in data:
            val.append([int(row[0]),int(row[1]),float(row[2]),float(row[4])*pow(10,3)+float(row[5]),row[6],float(row[10]),float(row[11]),float(row[12]),float(row[25]),float(row[26]),\
                float(row[27])])
        val_o = np.zeros((len(val),11),dtype=object)
    
    for i in range(0,len(val)):
        val_o[i,:] = val[i]

    return val_o


def open_xls(path,name,columns):
    for h in range(0,len(name)):
        filename = os.path.join(path,name[h])
        wb = xlrd.open_workbook(filename) 
        sheet = wb.sheet_by_index(0)
        rows = sheet.nrows
        cols = sheet.ncols
        col = columns[h]
        if h==0:
            val = np.empty(len(name),dtype=object)
            label = np.empty(len(name),dtype=object)
        val_ = np.zeros((rows-1,len(col)),dtype=object)
        label_ = np.zeros((1,len(col)),dtype=object)

        for i in range(0,rows):
            for j in range(0,len(col)):
                if i==0:
                    label_[0,j] = sheet.cell_value(i,col[j])

                elif name[h] == 'räl.xlsx':
                    v = sheet.cell_value(i,col[j])
                    if type(v) == int:
                        V = int(v)
                    elif type(v) == str:
                        v_=v.split()
                        if len(v_)==0:
                            V = v                        
                        elif len(v_)==1:
                            V = str(v)
                        else:
                            V = float(v_[0])*pow(10,3)+float(v_[2])
                    else:
                        V = float(v)                    
                    val_[i-1,j] = V
                
                elif name[h] == 'tamping_and_grinding.xlsx':
                    if j==4:
                        a = xlrd.xldate_as_tuple(sheet.cell_value(i,8),wb.datemode)
                        v = a[0]
                    else:
                        v = sheet.cell_value(i,col[j])
                    if type(v) == int:
                        V = int(v)
                    elif type(v) == str:
                        v_=v.split()
                        if len(v_)==0:
                            V = v                        
                        elif len(v_)==1:
                            V = str(v)
                        else:
                            V = float(v_[0])*pow(10,3)+float(v_[2])
                    else:
                        V = float(v)                    
                    val_[i-1,j] = V

                else:
                    v = sheet.cell_value(i,col[j])
                    if type(v) == int:
                        V = int(v)
                    elif type(v) == float:
                        V = float(v)                    
                    elif type(v) == str:
                        v_=v.split()
                        if len(v_)==0:
                            V = v                        
                        elif len(v_)==1:
                            V = float(v)
                        else:
                            V = float(v_[0])*pow(10,3)+float(v_[2])
                    else:
                        V = float(v)                    

                    val_[i-1,j] = V
        val[h] = val_
        label[h] = label_
                    #print(h,i,j)
            #print(sheet.cell_value(i, j))
            #print((sheet.cell_value(i, j))

    return val,label

def analyse_curve(val,val_h,val_sth,val_r,val_coord):
    R_func = np.zeros((len(val[:,1]),14),dtype=object)
    R_func_ = np.zeros((12),dtype=object)
    L_min = np.amin(val[:,0:1])
    L_max = np.amax(val[:,0:1])
    f_1 = 0; f_2 = 0; f_3 = 0; #error counters
    f_1_l = 'No superelevation data found for circular segment'
    f_2_l = 'Superelevation vary within circular segment. Includes segment with constant superelevation'
    f_3_l = 'Superelevation vary within circular segment. No segment with constant superelevation (ramp)'

    # Pre-process superelevation 
    h = np.zeros((len(val_h[:,1]),1))
    for i in range(0,len(val_h[:,1])): 
        h[i] = np.mean([val_h[i,0],val_h[i,1]])

    # Add superelevation to circular segments
    ind = np.intersect1d(np.where(h>L_min),np.where(h<L_max))
    h = h[ind] #pick studied section
    count_extra = 0
    R = np.zeros((len(val[:,1]),1))
    for i in range(0,len(val[:,1])):    #loop over all circular sections
        R[i] = np.mean([val[i,0],val[i,1]]) #mean track following coordinate in circular segment

        # Store values for currect circular segment
        R_func[i,0] = val[i,4] #radius [m]
        R_func[i,1] = val[i,1]-val[i,0] #curve length [m]
        R_func[i,12] = val[i,0] #start coordinate [m]
        R_func[i,13] = val[i,1] #end coordinate [m]

        # Add superelevation
        ind1 = np.where(h>val[i,0])
        ind2 = np.where(h<val[i,1])
        ind = np.intersect1d(ind1[0],ind2[0]) #index superelevation
        if ind.size==0: #no data on superelevation found in the current circular section
            R_func[i,2]=0
            R_func[i,3]=0
            f_1 = f_1+1
        elif len(ind)>1:
            i_=val_h[ind,4]-val_h[ind,5]
            I_ = np.where(i_==0)
            if len(I_[0])>1:
                R_func[i,1] = val_h[ind[I_[0][0]],1]-val_h[ind[I_[0][0]],0]
                R_func[i,2] = val_h[ind[I_[0][0]],4]
                R_func[i,3] = val_h[ind[I_[0][0]],5]
                R_func_[0] = R_func[i,0]
                R_func_[1] = val_h[ind[I_[0][1]],1]-val_h[ind[I_[0][1]],0]
                R_func_[2] = val_h[ind[I_[0][1]],4]
                R_func_[3] = val_h[ind[I_[0][1]],5]

                if count_extra>0:
                    R_func_extra=np.stack((R_func_extra,R_func_))
                else:
                    R_func_extra=R_func_

                count_extra = count_extra+1
            elif not I_[0]:
                R_func[i,2]=0
                R_func[i,3]=0
                f_2 = f_2+1
            else:
                R_func[i,2]=val_h[ind[I_],4]
                R_func[i,3]=val_h[ind[I_],5]
                f_3 = f_3+1
        else:
            R_func[i,2]=val_h[ind[0],4]
            R_func[i,3]=val_h[ind[0],5]
    
    # Add extra curves
    if count_extra>0:
        R_func=np.vstack((R_func,R_func_extra))

    # Add speed, profile/steel type and coordinates
    for i in range(0,len(val[:,1])):    #loop over all circular sections

        if i==176:
            debug=1

        # Pick speed
        ind1 = np.where(R[i]>val_sth[:,0])
        ind2 = np.where(R[i]<val_sth[:,1])
        ind = np.intersect1d(ind1[0],ind2[0]) #index superelevation
        if ind.size==0:
            R_func[i,4] = 0
        else:
            R_func[i,4] = val_sth[ind[0],3] #addera hastighet
        
        # Pick profile/steel type
        ind1 = np.where(R[i]>val_r[:,0])
        ind2 = np.where(R[i]<val_r[:,1])
        ind = np.intersect1d(ind1[0],ind2[0]) #index superelevation
        if ind.size==0:
            R_func[i,5] = 0 
            R_func[i,6] = 0
        else:
            R_func[i,5] = val_r[ind[0],4] 
            R_func[i,6] = val_r[ind[0],5]

        # Add coordinates
        ind = np.where(val[i,2]==val_coord[:,4])
        if len(ind[0])>0:
            R_func[i,7] = val_coord[ind[0][0],0]  #xmin
            R_func[i,8] = val_coord[ind[0][0],1]  #ymin
            R_func[i,9] = val_coord[ind[0][0],2]  #xmax
            R_func[i,10] = val_coord[ind[0][0],3] #Ymax

        # Add BIS-object number
        R_func[i,11] = int(val[i,2])

    # Output
    mes = [f_1,f_2,f_3]
    mes_label = [f_1_l,f_2_l,f_3_l]
    return R_func,mes,mes_label

def analyse_maint(R_func_0,valb_0,val_o):
    nr_R = len(R_func_0[:,1]) #number of curves
    maint = np.zeros((nr_R,2),dtype=object)
    gauge = np.zeros((nr_R,1),dtype=object)

    # Select rail grinding
    v0=valb_0[0]
    ind=np.where(valb_0[0][:,3]=='Rälbearbetning')
    grind=v0[ind[0],:]
    nr_g = len(ind[0])

    for i in range(0,nr_R):    #loop over all circular sections
        start = R_func_0[i,12] #start track following coordinate
        end = R_func_0[i,13] #end track following coordinate
        
        # Rail grinding
        ind_s = np.where(grind[:,1]<start)
        ind_e = np.where(grind[:,2]>end)
        ind = np.intersect1d(ind_s[0],ind_e[0]) #index superelevation
        maint[i,0] = grind[ind,4]

        # Frequency of grindig
        if ind.size!=0:
            grind_min=np.min(grind[ind,4])
            grind_max=np.max(grind[ind,4])
            maint[i,1] = (grind_max-grind_min)/ind.size
            if maint[i,1]==0:
                maint[i,1] = 0.1

        else:
            maint[i,1] = 0

        # Gauge
        indo_s = np.where(val_o[:,1]>start)
        indo_e = np.where(val_o[:,1]<end)
        ind = np.intersect1d(indo_s[0],indo_e[0]) #index superelevation
        gauge[i] = np.mean(val_o[ind,3])

    return maint,gauge

def sort_tracks(val,ind_track):
    val_0 = np.empty(len(val),dtype=object)
    val_1 = np.empty(len(val),dtype=object)
    val_2 = np.empty(len(val),dtype=object)
    val_3 = np.empty(len(val),dtype=object)
    for i in range(0,len(val)):
        count_0 = 0; count_1 = 0; count_2 = 0; count_3 = 0; 
        for j in range(0,len(val[i][:,1])):
            if val[i][j,ind_track[i]]=='':
                v = val[i][j,:]

                if i==0 and count_0==0:
                    exec('val_{}[{}]=v'.format(0,i))
                elif count_0==0:
                    exec('val_{}[{}]=v'.format(0,i))
                else:
                    exec('val_{}[{}]=np.vstack((val_{}[{}],v))'.format(0,i,0,i))            
                
                count_0 = count_0+1

            elif val[i][j,ind_track[i]]==1:
                v = val[i][j,:]

                if i==0 and count_1==0:
                    exec('val_{}[{}]=v'.format(1,i))
                elif count_1==0:
                    exec('val_{}[{}]=v'.format(1,i))
                else:
                    exec('val_{}[{}]=np.vstack((val_{}[{}],v))'.format(1,i,1,i))            
                
                count_1 = count_1+1

            elif val[i][j,ind_track[i]]==2:
                v = val[i][j,:]

                if i==0 and count_2==0:
                    exec('val_{}[{}]=v'.format(2,i))
                elif count_2==0:
                    exec('val_{}[{}]=v'.format(2,i))
                else:
                    exec('val_{}[{}]=np.vstack((val_{}[{}],v))'.format(2,i,2,i))            
                
                count_2 = count_2+1

            elif val[i][j,ind_track[i]]==3:
                v = val[i][j,:]

                if i==0 and count_3==0:
                    exec('val_{}[{}]=v'.format(3,i))
                elif count_3==0:
                    exec('val_{}[{}]=v'.format(3,i))
                else:
                    exec('val_{}[{}]=np.vstack((val_{}[{}],v))'.format(3,i,3,i))            
                
                count_3 = count_3+1

    return val_0,val_1,val_2,val_3

def cat_curve(R_func_0,R_func_1,R_func_2,R_func_3,maint,gauge,R_cat):
    
    # Create empty containers
    cat_ryear = np.empty(len(R_cat),dtype=object)
    cat_veq = np.empty(len(R_cat),dtype=object)
    cat_prof = np.empty(len(R_cat),dtype=object)
    cat_maint = np.empty(len(R_cat),dtype=object)
    cat_gauge = np.empty(len(R_cat),dtype=object)
    nr_cat = np.zeros(len(R_cat)+1)
    L_cat = np.zeros(len(R_cat)+1)
    count = np.zeros(len(R_cat))    
    for ii in range(0,4):
        if ii==0:
            RR = R_func_0
        elif ii==1:
            RR = R_func_1
        elif ii==2:
            RR = R_func_2
        else:
            RR = R_func_3            

        # Divide into curve radius categories
        for i in range(0,len(RR[:,1])):    #loop over all curves    

            for j in range(0,len(R_cat)):
                flag = 0
                if j==0: #low curve radius limit
                    if abs(RR[i,0])<R_cat[j]:
                        nr_cat[j] = nr_cat[j]+1
                        L_cat[j] = L_cat[j]+RR[i,1]
                        flag = 1

                elif j==len(R_cat)-1: #high curve radius limit
                    if abs(RR[i,0])>=R_cat[j-1] and abs(RR[i,0])<R_cat[j]:
                        nr_cat[j] = nr_cat[j]+1
                        L_cat[j] = L_cat[j]+RR[i,1]
                        flag = 1

                    if abs(RR[i,0])>=R_cat[j]:
                        nr_cat[j] = nr_cat[j]+1
                        L_cat[j] = L_cat[j]+RR[i,1]
                        flag = 1

                else: #curve radius categories inbetween
                    if abs(RR[i,0])>=R_cat[j-1] and abs(RR[i,0])<R_cat[j]:
                        nr_cat[j] = nr_cat[j]+1
                        L_cat[j] = L_cat[j]+RR[i,1]
                        flag = 1

                # Equilibrium speed
                veq = np.sqrt((abs(RR[i,0])*RR[i,2])/11.8)

#                # Default value
#                if j==0 and ii==0:
#                    cat_ryear[j] = 0

                if flag==1:
                    if count[j]==0:
                        v_sth = RR[i,4]  #line speed
                        #cat_ryear[j] = RR[i,6]  #year of installation of rail
                        #cat_prof[j] = RR[i,5]  #profile
                        #cat_maint[j] = maint[i,1]
                        #cat_gauge[j] = gauge[i]
                        if RR[i,2]==RR[i,3] and RR[i,2]!=0:
                            cat_veq[j]=v_sth-veq #comparison against equilibrium speed
                            cat_ryear[j] = RR[i,6]  #year of installation of rail
                            cat_prof[j] = RR[i,5]  #profile
                            cat_maint[j] = maint[i,1]
                            cat_gauge[j] = gauge[i]

                        else:
                            cat_veq[j]=0 #comparison against equilibrium speed
                            cat_ryear[j] = 0  #year of installation of rail
                            cat_prof[j] = 0  #profile
                            cat_maint[j] = 0
                            cat_gauge[j] = 0
                            nr_cat[j] = nr_cat[j]-1
                            L_cat[j] = L_cat[j]-RR[i,1]
                        
                        count[j] = 1
                    else:
                        v_sth = RR[i,4]  #line speed
                        ryear = RR[i,6]  #year of installation of rail
                        prof = RR[i,5]  #profile
                        maint_ = maint[i,1]
                        gauge_ = gauge[i]
                        #cat_ryear[j]=np.vstack((cat_ryear[j],ryear))
                        #cat_prof[j]=np.vstack((cat_prof[j],prof))
                        #cat_maint[j]=np.vstack((cat_maint[j],maint_))
                        #cat_gauge[j]=np.vstack((cat_gauge[j],gauge_))
                        if RR[i,2]==RR[i,3] and RR[i,2]!=0:
                            cat_veq[j]=np.vstack((cat_veq[j],v_sth-veq))
                            cat_ryear[j]=np.vstack((cat_ryear[j],ryear))
                            cat_prof[j]=np.vstack((cat_prof[j],prof))
                            cat_maint[j]=np.vstack((cat_maint[j],maint_))
                            cat_gauge[j]=np.vstack((cat_gauge[j],gauge_))

                        else:
                            cat_veq[j]=np.vstack((cat_veq[j],0)) #comparison against equilibrium speed
                            cat_ryear[j]=np.vstack((cat_ryear[j],0))
                            cat_prof[j]=np.vstack((cat_prof[j],0))
                            cat_maint[j]=np.vstack((cat_maint[j],0))
                            cat_gauge[j]=np.vstack((cat_gauge[j],0))
                            nr_cat[j] = nr_cat[j]-1
                            L_cat[j] = L_cat[j]-RR[i,1]

    # Output
    return nr_cat,L_cat,cat_ryear,cat_veq,cat_prof,cat_maint,cat_gauge

def centre(x1,y1,x2,y2,R):
    r = abs(R)
    x0 = [x1/2 + x2/2 + \
        (y1*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2 -\
        (y2*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2,\
        x1/2 + x2/2 - \
        (y1*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2 +\
        (y2*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2]

    y0 = [y1/2 + y2/2 -  \
        (x1*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2 +\
        (x2*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2, \
        y1/2 + y2/2 +  \
        (x1*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2 -\
        (x2*np.power(-(- 4*np.power(r,2) + np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2))/(np.power(x1,2) - 2*x1*x2 + np.power(x2,2) + np.power(y1,2) - 2*y1*y2 + np.power(y2,2)),1/2))/2]
    
    # Pair coordinates
    r_ = np.linalg.norm([x0[0]-x1,y0[0]-y1])
    Y0 = y0
    if r_>abs(R)*0.9 and r_<abs(R)*1.1:
        X0 = x0
    else:
        X0 = [x0[1],x0[0]]

    if (y2-y1)<1:
        alpha = 0
    else:
        alpha = np.arctan((x2-x1)/(y2-y1))
        
    if alpha>-np.pi/4 and alpha<np.pi/4:
        if R<0:
            ind=np.argmax(Y0)
        else:
            ind=np.argmin(Y0)
    else:
        if R<0:
            ind=np.argmax(X0)
        else:
            ind=np.argmin(X0)

    xc = X0[ind]
    yc = Y0[ind]

    return xc,yc
    
def sort_R_cat(cat_ryear,cat_veq,cat_prof,cat_maint,cat_gauge,nr_cat,cat_H):
    
    # Create empty containers
    cat_year_sort = np.zeros((len(cat_ryear),4))
    cat_year_label = [2005,2010,2015]
    cat_veq_sort = np.zeros((len(cat_veq),4))
    cat_veq_label = [20,35,50]
    cat_gauge_sort = np.zeros((len(cat_veq),4))
    cat_gauge_label = [5,10,15]    
    cat_prof_sort = np.zeros((len(cat_prof),2))
    #cat_prof_label = ['UIC','E1', 'BV']
    #cat_prof_label = ['MB6','60E1']
    cat_prof_label = ['UIC','E1'] # UIC (MB6?) or E1 (60E1?)
    cat_maint_sort = np.zeros((len(cat_ryear),4))
    cat_maint_label = [1,2,3]
    cat_H_sort = np.zeros((len(cat_ryear),4))
    cat_H_label = [0.33,0.66,1]

    for i in range(0,len(cat_ryear)):
        year = cat_ryear[i] #rail age
        veq = cat_veq[i] #veq
        grind = cat_maint[i] 
        gauge = cat_gauge[i] 
        H = cat_H[i] 
        if i<len(cat_ryear):
            prof = cat_prof[i] #profile
        
        if np.sum(nr_cat[i])>0:
            for j in range(0,3):
                if j==0:
                    # Year
                    ind1 = np.where(year < cat_year_label[j])
                    ind2 = np.where(year > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_year_sort[i,j] = ind.size

                    # Veq
                    ind1 = np.where(veq < cat_veq_label[j])
                    ind2 = np.where(veq > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_veq_sort[i,j] = ind.size

                    # Prof
                    ind = np.where(prof == cat_prof_label[j])
                    if len(ind)!=0:
                        cat_prof_sort[i,j] = np.size(ind[0])

                    # Maint
                    ind1 = np.where(grind <= cat_maint_label[j])
                    ind2 = np.where(grind > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_maint_sort[i,j] = ind.size

                    # Gauge
                    ind1 = np.where(gauge <= cat_gauge_label[j])
                    ind2 = np.where(gauge > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_gauge_sort[i,j] = ind.size

                    # H-damage
                    ind1 = np.where(H <= cat_H_label[j])
                    ind2 = np.where(H > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_H_sort[i,j] = ind.size

                elif j==1:
                    # Year
                    ind1 = np.where(year >= cat_year_label[j-1])
                    ind2 = np.where(year < cat_year_label[j])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_year_sort[i,j] = ind.size
                    
                    # Veq
                    ind1 = np.where(veq >= cat_veq_label[j-1])
                    ind2 = np.where(veq < cat_veq_label[j])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_veq_sort[i,j] = ind.size

                    # Prof
                    ind = np.where(prof == cat_prof_label[j])
                    if len(ind)!=0:
                        cat_prof_sort[i,j] = np.size(ind[0])

                    # Maint
                    ind1 = np.where(grind <= cat_maint_label[j])
                    ind2 = np.where(grind > cat_maint_label[j-1])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_maint_sort[i,j] = ind.size

                    # Gauge
                    ind1 = np.where(gauge <= cat_gauge_label[j])
                    ind2 = np.where(gauge > cat_gauge_label[j-1])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_gauge_sort[i,j] = ind.size

                    # H-damage
                    ind1 = np.where(H <= cat_H_label[j])
                    ind2 = np.where(H > cat_H_label[j-1])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_H_sort[i,j] = ind.size

                else:
                    #Year
                    ind1_ = np.where(year >= cat_year_label[j-1])
                    ind2_ = np.where(year < cat_year_label[j])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(year >= cat_year_label[j])
                    if ind1.size!=0:
                        cat_year_sort[i,j] = ind1.size
                    if len(ind2)!=0:
                        cat_year_sort[i,j+1] = np.size(ind2[0])

                    #Veq
                    ind1_ = np.where(veq >= cat_veq_label[j-1])
                    ind2_ = np.where(veq < cat_veq_label[j])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(veq >= cat_veq_label[j])
                    if ind1.size!=0:
                        cat_veq_sort[i,j] = ind1.size
                    if len(ind2)!=0:
                        cat_veq_sort[i,j+1] = np.size(ind2[0])

#                    # Prof
#                    ind = np.where(prof == cat_prof_label[j])
#                    if len(ind)!=0:
#                        cat_prof_sort[i,j] = np.size(ind[0])

                    # Maint
                    ind1_ = np.where(grind <= cat_maint_label[j])
                    ind2_ = np.where(grind > cat_maint_label[j-1])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(grind > cat_maint_label[j])
                    if ind1.size!=0:
                        cat_maint_sort[i,j] = ind1.size
                    if len(ind2)!=0:
                        cat_maint_sort[i,j+1] = np.size(ind2[0])

                    # Gauge
                    ind1_ = np.where(gauge <= cat_gauge_label[j])
                    ind2_ = np.where(gauge > cat_gauge_label[j-1])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(gauge > cat_gauge_label[j])
                    if ind1.size!=0:
                        cat_gauge_sort[i,j] = ind1.size
                    if len(ind2)!=0:
                        cat_gauge_sort[i,j+1] = np.size(ind2[0])

                    # H-damage
                    ind1_ = np.where(H <= cat_H_label[j])
                    ind2_ = np.where(H > cat_H_label[j-1])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(H > cat_H_label[j])
                    if ind1.size!=0:
                        cat_H_sort[i,j] = ind1.size
                    if len(ind2)!=0:
                        cat_H_sort[i,j+1] = np.size(ind2[0])


    # Output
    return cat_year_sort,cat_year_label,cat_veq_sort,cat_veq_label,cat_prof_sort,cat_prof_label,cat_maint_sort,cat_maint_label,cat_gauge_sort,cat_gauge_label,cat_H_sort,cat_H_label


# version of sort_R_cat for curve lengths (instead of number of curves)
def sort_R_cat_L(cat_ryear,cat_veq,cat_prof,cat_maint,cat_gauge,nr_cat,cat_H,cat_L):
    
    # Create empty containers
    cat_year_sort = np.zeros((len(cat_ryear),4))
    cat_year_label = [2005,2010,2015]
    cat_veq_sort = np.zeros((len(cat_veq),4))
    cat_veq_label = [20,35,50]
    cat_gauge_sort = np.zeros((len(cat_veq),4))
    cat_gauge_label = [5,10,15]    
    cat_prof_sort = np.zeros((len(cat_prof),2))
    #cat_prof_label = ['UIC','E1', 'BV']
    #cat_prof_label = ['MB6','60E1']
    cat_prof_label = ['UIC','E1'] # UIC (MB6?) or E1 (60E1?)
    cat_maint_sort = np.zeros((len(cat_ryear),4))
    cat_maint_label = [1,2,3]
    cat_H_sort = np.zeros((len(cat_ryear),4))
    cat_H_label = [0.33,0.66,1]

    for i in range(0,len(cat_ryear)):
        year = cat_ryear[i] #rail age
        veq = cat_veq[i] #veq
        grind = cat_maint[i] 
        gauge = cat_gauge[i]

        L = np.atleast_1d(cat_L[i])
        H = cat_H[i] 
        if i<len(cat_ryear):
            prof = cat_prof[i] #profile
        
        if np.sum(nr_cat[i])>0:
            for j in range(0,3):
                if j==0:
                    # Year
                    ind1 = np.where(year < cat_year_label[j])
                    ind2 = np.where(year > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_year_sort[i,j] = L[ind].sum()

                    # Veq
                    ind1 = np.where(veq < cat_veq_label[j])
                    ind2 = np.where(veq > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_veq_sort[i,j] = L[ind].sum()

                    # Prof
                    ind = np.where(prof == cat_prof_label[j])
                    if len(ind[0])!=0:
                        cat_prof_sort[i,j] = L[ind[0]].sum()

                    # Maint
                    ind1 = np.where(grind <= cat_maint_label[j])
                    ind2 = np.where(grind > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_maint_sort[i,j] = L[ind].sum()

                    # Gauge
                    ind1 = np.where(gauge <= cat_gauge_label[j])
                    ind2 = np.where(gauge > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_gauge_sort[i,j] = L[ind].sum()

                    # H-damage
                    ind1 = np.where(H <= cat_H_label[j])
                    ind2 = np.where(H > 0)
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_H_sort[i,j] = L[ind].sum()

                elif j==1:
                    # Year
                    ind1 = np.where(year >= cat_year_label[j-1])
                    ind2 = np.where(year < cat_year_label[j])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_year_sort[i,j] = L[ind].sum()
                    
                    # Veq
                    ind1 = np.where(veq >= cat_veq_label[j-1])
                    ind2 = np.where(veq < cat_veq_label[j])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_veq_sort[i,j] = L[ind].sum()

                    # Prof
                    ind = np.where(prof == cat_prof_label[j])
                    if len(ind[0])!=0:
                        cat_prof_sort[i,j] = L[ind[0]].sum()

                    # Maint
                    ind1 = np.where(grind <= cat_maint_label[j])
                    ind2 = np.where(grind > cat_maint_label[j-1])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_maint_sort[i,j] = L[ind].sum()

                    # Gauge
                    ind1 = np.where(gauge <= cat_gauge_label[j])
                    ind2 = np.where(gauge > cat_gauge_label[j-1])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_gauge_sort[i,j] = L[ind].sum()

                    # H-damage
                    ind1 = np.where(H <= cat_H_label[j])
                    ind2 = np.where(H > cat_H_label[j-1])
                    ind = np.intersect1d(ind1[0],ind2[0])
                    if ind.size!=0:
                        cat_H_sort[i,j] = L[ind].sum()

                else:
                    #Year
                    ind1_ = np.where(year >= cat_year_label[j-1])
                    ind2_ = np.where(year < cat_year_label[j])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(year >= cat_year_label[j])
                    if ind1.size!=0:
                        cat_year_sort[i,j] = L[ind1].sum()
                    if len(ind2[0])!=0:
                        cat_year_sort[i,j+1] = L[ind2[0]].sum()

                    #Veq
                    ind1_ = np.where(veq >= cat_veq_label[j-1])
                    ind2_ = np.where(veq < cat_veq_label[j])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(veq >= cat_veq_label[j])
                    if ind1.size!=0:
                        cat_veq_sort[i,j] = L[ind1].sum()
                    if len(ind2[0])!=0:
                        cat_veq_sort[i,j+1] = L[ind2[0]].sum() 

#                    # Prof
#                    ind = np.where(prof == cat_prof_label[j])
#                    if len(ind)!=0:
#                        cat_prof_sort[i,j] = np.size(ind[0])

                    # Maint
                    ind1_ = np.where(grind <= cat_maint_label[j])
                    ind2_ = np.where(grind > cat_maint_label[j-1])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(grind > cat_maint_label[j])
                    if ind1.size!=0:
                        cat_maint_sort[i,j] = L[ind1].sum() 
                    if len(ind2[0])!=0:
                        cat_maint_sort[i,j+1] = L[ind2[0]].sum() 

                    # Gauge
                    ind1_ = np.where(gauge <= cat_gauge_label[j])
                    ind2_ = np.where(gauge > cat_gauge_label[j-1])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(gauge > cat_gauge_label[j])
                    if ind1.size!=0:
                        cat_gauge_sort[i,j] = L[ind1].sum()
                    if len(ind2[0])!=0:
                        cat_gauge_sort[i,j+1] = L[ind2[0]].sum() 

                    # H-damage
                    ind1_ = np.where(H <= cat_H_label[j])
                    ind2_ = np.where(H > cat_H_label[j-1])
                    ind1 = np.intersect1d(ind1_[0],ind2_[0])
                    ind2 = np.where(H > cat_H_label[j])
                    if ind1.size!=0:
                        cat_H_sort[i,j] = L[ind1].sum()
                    if len(ind2[0])!=0:
                        cat_H_sort[i,j+1] = L[ind2[0]].sum()


    # Output
    return cat_year_sort,cat_veq_sort,cat_prof_sort,cat_maint_sort,cat_gauge_sort,cat_H_sort


# --------------------------------------------------------------------
#                                                   Functions Optram v2
#                                                   ------------------

def analyse_optram_spl(val,val_R_0,val_R_1,val_R_2,val_R_3,R_lim,R_coord,val_iore,val_seg):
    nr_curves = len(R_coord[:,1])

    O_func = np.zeros((nr_curves,16),dtype=object)
    
    # Column
    ind_x = 2
    ind_xi = 3
    ind_sth = 4 # speed
    ind_prof = 5 # rail profile
    ind_g = 8
    ind_R = 9
    ind_h = 10
    ind_Ngps = 11
    ind_Egps = 12
    
    # Pick curves
    for i in range(0,nr_curves): 
                
        # Limit coordinates of curve i
        x_min = R_coord[i,0]
        x_max = R_coord[i,1]

        # Indexes of current curve
        ind = np.intersect1d(np.where(val[:,ind_x]>x_min),np.where(val[:,ind_x]<x_max))
        x_min_tf = val[ind[0],ind_xi]
        x_max_tf = val[ind[-1],ind_xi]

        # GPS-coordinates
        Ngps_s = val[ind[0],ind_Ngps]
        Egps_s = val[ind[0],ind_Egps]
        Ngps_e = val[ind[-1],ind_Ngps]
        Egps_e = val[ind[-1],ind_Egps]

        # Indexes of curve in segment data
        ind_s1 = np.intersect1d(np.where(val_seg[:,0]>x_min_tf),np.where(val_seg[:,0]<x_max_tf))
        ind_s2 = np.intersect1d(np.where(val_seg[:,1]>x_min_tf),np.where(val_seg[:,1]<x_max_tf))
        ind_s3 = np.intersect1d(np.where(val_seg[:,0]>x_min_tf),np.where(val_seg[:,1]<x_max_tf))
        ind_s4 = np.intersect1d(np.where(val_seg[:,0]<x_min_tf),np.where(val_seg[:,1]>x_max_tf))
        ind_s=[]
        for ii in range(0,4):
            if ii==0 and  ind_s1.size>0:
                ind_s = np.append(ind_s,ind_s1[0])
            elif ii==1 and  ind_s2.size>0:
                ind_s = np.append(ind_s,ind_s2[0])                
            elif ii==2 and  ind_s3.size>0:
                ind_s = np.append(ind_s,ind_s3[0])                
            elif ind_s4.size>0: 
                ind_s = np.append(ind_s,ind_s4[0])

        # year of installation
        O_func[i,10] = np.unique(val_seg[ind_s.astype(int),3])[0] # höger/right rail
        O_func[i,11] = np.unique(val_seg[ind_s.astype(int),4])[0] # vänster/left rail

        #print(i,val[i,ind_x])

        # Calculate average radius and superelevation
        h_av = np.mean(val[ind,ind_h])
        R_av = 1/np.mean(val[ind,ind_R])
        xi_av = np.mean(val[ind,ind_xi])
        xi_min = np.min(val[ind,ind_xi])
        xi_max = np.max(val[ind,ind_xi])
        gauge_av = np.mean(val[ind,ind_g])
        
        # Store
        O_func[i,6] = xi_min
        O_func[i,7] = xi_max
        O_func[i,8] = gauge_av
        O_func[i,9] = xi_max-xi_min

        #print(xi_max-xi_min,xi_av)

        # Indexes of current curve
        n = len(val_R_0[:,1])
        for j in range(0,n):
            rfunc_av = np.mean([val_R_0[j,12],val_R_0[j,13]])            
            if (xi_av>val_R_0[j,12] and xi_av<val_R_0[j,13]) or (rfunc_av>xi_min and rfunc_av<xi_max):
                #O_func[i,3] = val_R_0[j,6]
                sth = val_R_0[j,ind_sth]
                prof = val_R_0[j,ind_prof]
        
        if O_func[i,3]==0:
            n = len(val_R_1[:,1])
            for j in range(0,n): 
                rfunc_av = np.mean([val_R_1[j,12],val_R_1[j,13]])            
                if (xi_av>val_R_1[j,12] and xi_av<val_R_1[j,13]) or (rfunc_av>xi_min and rfunc_av<xi_max):
                    #O_func[i,3] = val_R_1[j,6]
                    sth = val_R_1[j,ind_sth]
                    prof = val_R_1[j,ind_prof]
        
        if O_func[i,3]==0:
            n = len(val_R_2[:,1])
            for j in range(0,n): 
                rfunc_av = np.mean([val_R_2[j,12],val_R_2[j,13]])            
                if (xi_av>val_R_2[j,12] and xi_av<val_R_2[j,13]) or (rfunc_av>xi_min and rfunc_av<xi_max):
                    #O_func[i,3] = val_R_2[j,6]
                    sth = val_R_2[j,ind_sth]
                    prof = val_R_2[j,ind_prof]
        
        if O_func[i,3]==0:
            n = len(val_R_3[:,1])
            for j in range(0,n): 
                rfunc_av = np.mean([val_R_3[j,12],val_R_3[j,13]])            
                if (xi_av>val_R_3[j,12] and xi_av<val_R_3[j,13]) or (rfunc_av>xi_min and rfunc_av<xi_max):
                    #O_func[i,3] = val_R_3[j,6]
                    sth = val_R_3[j,ind_sth]
                    prof = val_R_3[j,ind_prof]

        # Update rail profile based on rule by Lars Sundholm, TRV
        if gauge_av>=15:
            O_func[i,5] = 'MB6'
        else:
            O_func[i,5] = '60E1'
        
        # Store
        O_func[i,0] = val[i,ind_x]
        O_func[i,1] = R_av
        O_func[i,2] = h_av
        O_func[i,4] = sth
        O_func[i,5] = prof
        O_func[i,12] = Ngps_s
        O_func[i,13] = Egps_s
        O_func[i,14] = Ngps_e
        O_func[i,15] = Egps_e

        
    return O_func


def analyse_maint_opt(O_func,val_b,val_rpm):
    nr_R = len(O_func[:,1]) #number of curves
    maint = np.zeros((nr_R,2),dtype=object)
    nr_damage = len(val_rpm)
    damage = np.zeros(nr_R,dtype=object)
        
    # Select rail grinding
    v0=val_b[0]
    ind=np.where(val_b[0][:,3]=='Rälbearbetning')
    grind=v0[ind[0],:]
    nr_g = len(ind[0])

    for i in range(0,nr_R):    #loop over all circular sections
        start = O_func[i,6] #start track following coordinate
        end = O_func[i,7] #end track following coordinate
        R = O_func[i,1]
        year = O_func[i,3]
        print(i)
        if i==nr_R-1:
            debug=1

        # Rail damage 
        damage_j = np.zeros(len(val_rpm)*2+1,dtype=float)
        for j in range(0,nr_damage):
            rpm_j = val_rpm[j]
            ind_s = np.where(rpm_j[:,3]>start)
            ind_e = np.where(rpm_j[:,3]<end)
            ind = np.intersect1d(ind_s[0],ind_e[0]) #index superelevation
            if ind.size!=0:
                damage_j[[j*2,j*2+1]] = [np.mean(rpm_j[ind,7]),np.mean(rpm_j[ind,10])]
            else:
                print(j)
                damage_j[[j*2,j*2+1]] = [0,0]
        
        if R<0 and O_func[i,11]<2014 and O_func[i,10]<2014:
            damage_j[[j*2+2]] = (damage_j[[-2]]-damage_j[[1]])/5 #np.mean(damage_j[[1:-1:2]])
        elif R>0 and O_func[i,11]<2014 and O_func[i,10]<2014:
            damage_j[[j*2+2]] = (damage_j[[-3]]-damage_j[[0]])/5 #np.mean(damage_j[[0:-1:2]])

        if damage_j[[j*2+2]]<0:
            debug = 1
        damage[i] = damage_j


        # Rail grinding
        ind_s = np.where(grind[:,1]<start)
        ind_e = np.where(grind[:,2]>end)
        ind = np.intersect1d(ind_s[0],ind_e[0]) #index superelevation
        maint[i,0] = grind[ind,4]

        # Frequency of grindig
        if ind.size!=0:
            grind_min=np.min(grind[ind,4])
            grind_max=np.max(grind[ind,4])
            maint[i,1] = (grind_max-grind_min)/ind.size
            if maint[i,1]==0:
                maint[i,1] = 0.1

        else:
            maint[i,1] = 0

    return maint,damage


def cat_curve_opt(O_func,maint,R_cat,damage):
    
    # Create empty containers
    cat_ryear = np.empty(len(R_cat),dtype=object)
    cat_veq = np.empty(len(R_cat),dtype=object)
    cat_prof = np.empty(len(R_cat),dtype=object)
    cat_maint = np.empty(len(R_cat),dtype=object)
    cat_gauge = np.empty(len(R_cat),dtype=object)
    cat_L = np.empty(len(R_cat),dtype=object)
    cat_H = np.empty(len(R_cat),dtype=object)
    cat_i = np.empty(len(R_cat),dtype=object)
    nr_cat = np.zeros(len(R_cat)+1)
    L_cat = np.zeros(len(R_cat)+1)
    count = np.zeros(len(R_cat))    

    RR = O_func

    # Divide into curve radius categories
    for i in range(0,len(RR[:,1])):    #loop over all curves    
        for j in range(0,len(R_cat)):
            flag = 0
            if j==0: #low curve radius limit
                if abs(RR[i,1])<R_cat[j]:
                    nr_cat[j] = nr_cat[j]+1
                    L_cat[j] = L_cat[j]+RR[i,9]
                    flag = 1

            elif j==len(R_cat)-1: #high curve radius limit
                if abs(RR[i,1])>=R_cat[j-1] and abs(RR[i,1])<R_cat[j]:
                    nr_cat[j] = nr_cat[j]+1
                    L_cat[j] = L_cat[j]+RR[i,9]
                    flag = 1

                if abs(RR[i,1])>=R_cat[j]:
                    nr_cat[j] = nr_cat[j]+1
                    L_cat[j] = L_cat[j]+RR[i,9]
                    flag = 1

            else: #curve radius categories inbetween
                if abs(RR[i,1])>=R_cat[j-1] and abs(RR[i,1])<R_cat[j]:
                    nr_cat[j] = nr_cat[j]+1
                    L_cat[j] = L_cat[j]+RR[i,9]
                    flag = 1

            # Equilibrium speed
            veq = np.sqrt((abs(RR[i,1])*abs(RR[i,2]))/11.8)
            if np.isnan(veq):
                print(1)

#                # Default value
#                if j==0 and ii==0:
#                    cat_ryear[j] = 0

            if flag==1:
                if count[j]==0:
                    v_sth = RR[i,4]  #line speed
                    cat_veq[j]=v_sth-veq #comparison against equilibrium speed
                    cat_ryear[j] = RR[i,10]  #year of installation of rail (10-right and 11-left, not 3)
                    cat_prof[j] = RR[i,5]  #profile
                    cat_maint[j] = maint[i,1]
                    cat_gauge[j] = RR[i,8]
                    cat_L[j] = RR[i,9]
                    cat_H[j] = damage[i][-1]
                    cat_i[j] = i 

                    count[j] = 1
                else:
                    v_sth = RR[i,4]  #line speed
                    ryear = RR[i,10]  #year of installation of rail (10-right and 11-left, not 3)
                    prof = RR[i,5]  #profile
                    maint_ = maint[i,1]
                    gauge_ = RR[i,8]
                    L_ = RR[i,9]
                    cat_H_ = damage[i][-1] 
                    cat_i_ = i 

                    # Store
                    cat_veq[j]=np.vstack((cat_veq[j],v_sth-veq))
                    cat_ryear[j]=np.vstack((cat_ryear[j],ryear))
                    cat_prof[j]=np.vstack((cat_prof[j],prof))
                    cat_maint[j]=np.vstack((cat_maint[j],maint_))
                    cat_gauge[j]=np.vstack((cat_gauge[j],gauge_))
                    cat_L[j]=np.vstack((cat_L[j],L_))
                    cat_H[j]=np.vstack((cat_H[j],cat_H_))
                    cat_i[j]=np.vstack((cat_i[j],cat_i_))

    # Output
    return nr_cat,L_cat,cat_ryear,cat_veq,cat_prof,cat_maint,cat_gauge,cat_H,cat_i,cat_L

def open_iore_v2(path,name,column_labels):
    filename = os.path.join(path,name)
    wb = xlrd.open_workbook(filename) 
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    
    val = np.zeros((rows-1,cols),dtype=object)
    label = np.zeros((cols),dtype=object)

    ind_column = np.zeros((len(column_labels)),dtype=int)
    count = 0
    for i in range(0,rows):
        print(i,rows)
        for j in range(0,cols):
            if i==0:
                label[j] = sheet.cell_value(i,j)
                for jj in range(0,len(column_labels)):
                    if label[j]==column_labels[jj]:
                        ind_column[count] = j
                        count = count+1

            else:
                if label[j]=='tvf' or label[j]=='lvf' or label[j]=='emi' or label[j]=='dir':
                    val[i-1,j] = str(sheet.cell_value(i,j))
                elif label[j]=='time_t':
                    val[i-1,j] = datetime.datetime.fromtimestamp(sheet.cell_value(i,j))
                elif label[j]=='tid':
                    val[i-1,j] = 0
                elif label[j]=='veh_nbr' or label[j]=='id_code':
                    val[i-1,j] = int(sheet.cell_value(i,j))
                else:
                    val[i-1,j] = float(sheet.cell_value(i,j))
    
    #Output
    val_ = val[:,ind_column]
    label_ = label[ind_column]
    
    return val_,label_


def map_iore(val_iore,val_o):
    
    nr_o = len(val_o[:,0])
    nr_iore = len(val_iore[:,0])
    EN = np.zeros((nr_iore,2))
    x_iore = np.zeros((nr_o,3))

    # Convert GPS-coordinate for IORE
    for i in range(0,nr_iore):
        EN[i,:] = convert(val_iore[i,7],val_iore[i,6])

    E_iore = EN[:,1]
    N_iore = EN[:,0]
    for i in range(0,nr_iore):
        E_o = val_o[i,11]
        N_o = val_o[i,12]

        N_diff = np.subtract(N_o,N_iore)
        E_diff = np.subtract(E_o,E_iore)

        r = np.linalg.norm([N_diff,E_diff],axis=0)

        d_min = np.min(np.abs(r))
        if d_min<100:
            print(i)

    x_iore=0
    
    return x_iore

def analyse_iore(O_func,val_iore,val_o,id_vehicle):

    # Initiate
    nr_iore = len(val_iore)
    nr_R = len(O_func)
    speed = np.zeros(len(id_vehicle),dtype=object)
    lim = 50 #use 50 m distance in search for coordinates

    # Index
    ind_Ngps_s = 12
    ind_Egps_s = 13
    ind_Ngps_e = 14
    ind_Egps_e = 15
    ind_N = 6
    ind_E = 7
    ind_v = 9
    ind_N_o = 11
    ind_E_o = 12

    # Create coordinate matrix
    nr_o = len(val_o)
    o_c = np.zeros((nr_o,2))
    for i in range(0,nr_o):
        o_c[i,0] = val_o[i,ind_N_o]
        o_c[i,1] = val_o[i,ind_E_o]

    iore = np.zeros((nr_iore,4))
    one_c = np.ones((nr_o,1))
    for i in range(0,nr_iore):
        
        # Convert to SWEREF 99
        EN = convert(val_iore[i,7],val_iore[i,6])
        iore[i,1] = EN[1]
        iore[i,2] = EN[0]

#        iore_c = np.array([iore[i,1],iore[i,2]])
#        iore_c_m = one_c*np.transpose(iore_c)
#        dist_m = iore_c_m-o_c
#        dist = np.linalg.norm(dist_m,axis=1)
#        np.min(dist)

        # Speed
        iore[i,3] = val_iore[i,9]*3.6

        if val_iore[i,0]==id_vehicle[0]: #different vehicles
            id_v = 1
        elif val_iore[i,0]==id_vehicle[1]:
            id_v = 2
        elif val_iore[i,0]==id_vehicle[2]:
            id_v = 3
        elif val_iore[i,0]==id_vehicle[3]:
            id_v = 4
        
        iore[i,0] = id_v

    r = np.zeros((2,2))            
    for i in range(0,nr_R):
        
        # Start and end coordinates of curve
        N_s = O_func[i,ind_Ngps_s]
        E_s = O_func[i,ind_Egps_s]
        N_e = O_func[i,ind_Ngps_e]
        E_e = O_func[i,ind_Egps_e]
        r[0,:] = np.array([N_s,E_s])
        r[1,:] = np.array([N_e,E_e])
    
    return iore
    """        
        flag = 1
        for j in range(0,nr_iore):
            
            # Current coordinate
            r_iore = np.array([iore[j,1],iore[j,2]])

            dr1 = np.linalg.norm(r_iore-r[0,:],axis=0)
            dr2 = np.linalg.norm(r_iore-r[1,:],axis=0)

            if flag:
                if dr1<lim:
                    flag = 0
                    ind_s = 2
                    ind_gps = [j]
                elif dr2<lim:
                    flag = 0
                    ind_s = 1
                    ind_gps = [j]
            else:
                if ind_s==2:
                    if dr1<lim:

                else:
    """
    

### Output of figures
import matplotlib.pyplot as plt
def output_figure_length(R_cat,Y_cat_L,C,filename):
    plt.figure(1,figsize=(14,6)) 
    ax = plt.axes()
    Y_cat_L_km = Y_cat_L/1000 # convert length in km
    if C == '':
        plt.bar(R_cat, Y_cat_L_km[0:-1], width = 90,color = 'b')
    elif C == 'year':
        ax.bar(R_cat, Y_cat_L_km[:,0], width = 90,color = 'b', label = 'Before year 2005')
        ax.bar(R_cat, Y_cat_L_km[:,1], bottom = Y_cat_L_km[:,0],width = 90,color = 'r', label = 'Between 2005-2010')
        ax.bar(R_cat, Y_cat_L_km[:,2], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1],width = 90,color = 'g', label = 'Between 2010-2015')
        ax.bar(R_cat, Y_cat_L_km[:,3], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1]+Y_cat_L_km[:,2],width = 90,color = 'm', label = 'After 2015')
    elif C == 'speed':
        ax.bar(R_cat, Y_cat_L_km[:,0], width = 90,color = 'b', label = r'$\itv_{\rmSTH} - \itv_{\rmeq}<$' r'$20 \ $' r'$\rm{km/h}$')
        ax.bar(R_cat, Y_cat_L_km[:,1], bottom = Y_cat_L_km[:,0],width = 90,color = 'r', label = r'$20 \ \rm{km/h}$' r'$\leq$' r'$\itv_{\rmSTH} - \itv_{\rmeq}$' r'$<$' r'$35 \ \rm{km/h}$')
        ax.bar(R_cat, Y_cat_L_km[:,2], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1],width = 90,color = 'g', label = r'$35 \ \rm{km/h}$' r'$\leq$' r'$\itv_{\rmSTH} - \itv_{\rmeq}$' r'$<$' r'$50 \ \rm{km/h}$')
        ax.bar(R_cat, Y_cat_L_km[:,3], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1]+Y_cat_L_km[:,2],width = 90,color = 'm', label = r'$\itv_{\rmSTH} - \itv_{\rmeq}>$' r'$50 \ $' r'$\rm{km/h}$')
    elif C == 'profile':
        ax.bar(R_cat, Y_cat_L_km[:,0], width = 90,color = 'b', label = 'MB6 (UIC)')
        ax.bar(R_cat, Y_cat_L_km[:,1], bottom = Y_cat_L_km[:,0],width = 90,color = 'r', label = '60E1 (E1)')
    elif C == 'gauge':
        ax.bar(R_cat, Y_cat_L_km[:,0], width = 90,color = 'b', label = 'Average gauge widening ' r'$\leq$' ' 5 mm')
        ax.bar(R_cat, Y_cat_L_km[:,1], bottom = Y_cat_L_km[:,0],width = 90,color = 'r', label = 'Average gauge widening between 5 - 10 mm')
        ax.bar(R_cat, Y_cat_L_km[:,2], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1],width = 90,color = 'g', label = 'Average gauge widening between 10 - 15 mm')
        ax.bar(R_cat, Y_cat_L_km[:,3], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1]+Y_cat_L_km[:,2],width = 90,color = 'm', label = 'Average gauge widening > 15 mm')
    elif C == 'H-damage':
        ax.bar(R_cat, Y_cat_L_km[:,0], width = 90,color = 'b', label = r'$\Delta_H \leq$' '0.33 mm/year')
        ax.bar(R_cat, Y_cat_L_km[:,1], bottom = Y_cat_L_km[:,0],width = 90,color = 'r', label = r'$\Delta_H$' ' between 0.33 - 0.66 mm/year')
        ax.bar(R_cat, Y_cat_L_km[:,2], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1],width = 90,color = 'g', label =  r'$\Delta_H$' ' between 0.66 - 1 mm/year')
        ax.bar(R_cat, Y_cat_L_km[:,3], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1]+Y_cat_L_km[:,2],width = 90,color = 'm', label = r'$\Delta_H \geq$' '1 mm/year')
    elif C == 'grinding':
        ax.bar(R_cat, Y_cat_L_km[:,0], width = 90,color = 'b', label = 'Average grinding interval ' r'$\leq$' ' 1 year')
        ax.bar(R_cat, Y_cat_L_km[:,1], bottom = Y_cat_L_km[:,0],width = 90,color = 'r', label = 'Average grinding interval between 1 - 2 years')
        ax.bar(R_cat, Y_cat_L_km[:,2], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1],width = 90,color = 'g', label = 'Average grinding interval between 2 - 3 years')
        ax.bar(R_cat, Y_cat_L_km[:,3], bottom = Y_cat_L_km[:,0]+Y_cat_L_km[:,1]+Y_cat_L_km[:,2],width = 90,color = 'm', label = 'Average grinding interval > 3 years')
    plt.xticks(np.arange(100,3100,100)-100/2, np.arange(0,3000,100),rotation=45)
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    plt.ylabel('Length of curves [km]',fontsize=24,labelpad=10)
    plt.xlabel('Curve radius [m]',fontsize=24,labelpad=10)
    plt.xlim((100,3000))
    plt.ylim((0,13))
    ax.legend(fontsize=22)
    plt.savefig(filename,bbox_inches='tight')
    plt.close()