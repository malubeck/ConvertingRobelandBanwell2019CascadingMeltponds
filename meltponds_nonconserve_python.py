# The following description is from Robel and Banwell (2019): 
#"""meltponds_nonconserve is a cellular automaton model for the filling,
#draining, and interaction of a regularly-spaced network of melt ponds on 
#an ice shelf. The model is described in Robel & Banwell 2019 in GRL
#(note this is a type of nonconservative sanpdile model, a few small
#changes can be implemented to make the model conservative)
#Inputs: n - dimension of square melt pond network of size n x n
#        iters - number of meltwater perturbations to add (model
#        iterations)
#        th_init - initial value of k, ice strength
#        heal_speed - rate of ice strength increase (number of sites
#        strengthened per iteration - not used in paper)
#        hf_dmg - rate of damaging per hydrofracture event (D in paper)
#Outputs: zs - mean meltpond depth as a function of iteration
#         thsp - mean ice strength as a function of iteration
#         avs - number of hydrofracture cascades as a function of iteration
#         av_plt - cascade size counter
#         zs_big - meltwater pond thickness at every iteration and
#         sub-iteration
#         ths_big - ice strength at every iteration and sub-iteration""" 

         
#The following code is a conversion from the Robel and Banwell (2019) paper into Python:

from numpy import roll, empty, maximum, greater_equal, mean
from numpy.random import randint 
import pandas as pd
import numpy.ma as ma 
import math as math
 

def meltponds_nonconserve(n,iters,th_init,heal_speed,hf_dmg): 
    big_save_on=1   
    if (big_save_on):
        #zs_big=[]
        #ths_big=[]
        bst=-1 #start here so it can then go to 0
        zs_big=np.nan * np.empty((iters**2,n,n))
        ths_big=np.nan * np.empty((iters**2,n,n))
    else:
        zs_big=[]
        ths_big=[]
    
    z = np.zeros((n,n),dtype=int)  
    av_plt= np.zeros(iters) 
    th=th_init*np.ones((n,n),dtype = int)
    seeds = np.random.randint(n,size=(2, iters)) 
    seeds2 = np.random.randint(n,size=(heal_speed,2,iters)) 
    
    zs =np.empty(iters) # initialize these arrays 
    thsp = np.empty(iters)
    avs = np.empty(iters)
    
    for i in range(iters):
        z[seeds[0][i],seeds[1][i]] += 1  
        z = z.astype(int)
        for q in range(heal_speed): 
            if (z[seeds2[q][0][i]],[seeds2[q][1][i]] == 0):
                th[seeds2[q][0][i],seeds2[q][1][i]]=th[seeds2[q][0][i],seeds2[q][1][i]] + 1
                th[seeds2[q][0][i],seeds2[q][1][i]]=min(pd.concat(th[seeds2[q][0][i],seeds2[q][1][i]],th_init))
        th = th.astype(int)
        av=0
        if (big_save_on):
            bst += 1
            zs_big[bst][:][:] = z
            ths_big[bst][:][:] = th
        
        mask = np.empty((n,n))
        for row in range(len(z)):
            for col in range(len(z)):
                if (z[row][col] > 0) & (z[row][col] >= th[row][col]):
                    mask[row][col] = 1
                else:
                    mask[row][col] = 0
        mask = mask.astype(int)
        mask_sum = mask.sum()

        while (mask.sum() > 0):
            
            av = int(av + mask_sum + 0.1)
            
            sft_11=np.roll(mask,1)
            sft_11[0][:]=0
            sft_m11=np.roll(mask,-1) 
            sft_m11[-1][:]=0
            sft_12=np.roll(mask,[1,2]) 
            sft_12[:][0]=0 
            sft_m12=np.roll(mask,[-1,2])
            sft_m12[:][-1]=0
            
            
            z= z-z*mask # removing water, multipling z by a mask to only take out meltpond water depth where there is a hydrofracture
            # hydrofracture where the meltpond water depth is equal or greater than the ice strength
            
            th2 = mask + sft_11 + sft_m11 + sft_12 + sft_m12
            th = th-(hf_dmg*th2).astype(int)
            th=np.maximum(th,np.zeros((n,n)))
            if (big_save_on):
                
                bst=bst + 1
                
                zs_big[bst][:][:] = z
                ths_big[bst][:][:] = th
            mask = np.empty((n,n))
            for row in range(len(z)):
                for col in range(len(z)):
                    if (z[row][col] > 0) & (z[row][col] >= th[row][col]):
                        mask[row][col] = 1
                    else:
                        mask[row][col] = 0
            mask_sum = mask.sum()
                
        av_ind = av -1  
        if av > 0:
            if av_plt[av_ind] >= 1:
                av_plt[av_ind] = av_plt[av_ind] + 1
            else:
                av_plt[av_ind]=1  
        zs[i]=np.mean(z)
        thsp[i]=np.mean(th)
        
        avs[i]=av 
        
    keep_z = 0
    for sheet in range(len(zs_big)):
        if (np.isnan(zs_big[sheet]).any()):
            keep_z +=0
        else:
            keep_z += 1 
            
    keep_th = 0
    for sheet in range(len(ths_big)):
        if (np.isnan(ths_big[sheet]).any()):
            keep_th +=0
        else:
            keep_th += 1 
           
    zs_big = zs_big[0:keep_z]
    ths_big = ths_big[0:keep_th]
    
    return zs, thsp, avs, av_plt, zs_big, ths_big, keep_z
         
