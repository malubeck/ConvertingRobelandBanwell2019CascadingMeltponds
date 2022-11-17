The following description is from Robel and Banwell (2019): 
"""meltponds_nonconserve is a cellular automaton model for the filling,
draining, and interaction of a regularly-spaced network of melt ponds on 
an ice shelf. The model is described in Robel & Banwell 2019 in GRL
(note this is a type of nonconservative sanpdile model, a few small
changes can be implemented to make the model conservative)
Inputs: n - dimension of square melt pond network of size n x n
        iters - number of meltwater perturbations to add (model
        iterations)
        th_init - initial value of k, ice strength
        heal_speed - rate of ice strength increase (number of sites
        strengthened per iteration - not used in paper)
        hf_dmg - rate of damaging per hydrofracture event (D in paper)
Outputs: zs - mean meltpond depth as a function of iteration
         thsp - mean ice strength as a function of iteration
         avs - number of hydrofracture cascades as a function of iteration
         av_plt - cascade size counter
         zs_big - meltwater pond thickness at every iteration and
         sub-iteration
         ths_big - ice strength at every iteration and sub-iteration"""
         
The following code is a converstion from the Robel and Banwell (2019) paper into Python:

from numpy import roll, empty, maximum, greater_equal, mean
from numpy.random import randint 
import pandas as pd
import numpy.ma as ma 
import math as math
#import torch as torch 

def meltponds_nonconserve(n,iters,th_init,heal_speed,hf_dmg):
    # come up with formula for bst since its larger than iters 
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
    
    #zs_big=np.nan * np.empty((iters*2,n,n))
    #ths_big=np.nan * np.empty((iters*2,n,n))
    z = np.zeros((n,n),dtype=int) #,dtype=float, zeros was empty 
    av_plt= np.zeros(iters) # was 0, initiates this so that there is iters long av_plt 
    th=th_init*np.ones((n,n),dtype = int)
    seeds = np.random.randint(n,size=(2, iters)) # this line is working 
    seeds2 = np.random.randint(n,size=(heal_speed,2,iters)) # this line is not working
    
    zs =np.empty(iters) # initialize these arrays 
    thsp = np.empty(iters)
    avs = np.empty(iters)
    
    for i in range(iters):
        z[seeds[0][i],seeds[1][i]] += 1 # changed the parentheses to the [] to test the code 
        z = z.astype(int)
        for q in range(heal_speed): #these lines related to heal speed will have to be dealt wiht later as of now facing syntax issues with this line 65
            if (z[seeds2[q][0][i]],[seeds2[q][1][i]] == 0):
                th[seeds2[q][0][i],seeds2[q][1][i]]=th[seeds2[q][0][i],seeds2[q][1][i]] + 1
                th[seeds2[q][0][i],seeds2[q][1][i]]=min(pd.concat(th[seeds2[q][0][i],seeds2[q][1][i]],th_init))
        th = th.astype(int)
        av=0
        if (big_save_on):
            bst += 1
            #zs_big.append(z)
            #ths_big.append(th)
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
            #bidx = [index for index,v in np.ndenumerate(z) if (v>0 & np.greater_equal(z,th)).all()] # fill in
            av = int(av + mask_sum + 0.1)
            #bidxgrid = np.zeros((n,n))
            #for ind in range(len(bidx)):
                #bidxgrid[bidx[ind][0],bidx[ind][1]] = 1
            #bidxgrid = bidxgrid.astype(int)
            sft_11=np.roll(mask,1)
            sft_11[0][:]=0
            sft_m11=np.roll(mask,-1) 
            sft_m11[-1][:]=0
            sft_12=np.roll(mask,[1,2]) 
            sft_12[:][0]=0 
            sft_m12=np.roll(mask,[-1,2])
            sft_m12[:][-1]=0
            #print(bidxgrid)
            
            z= z-z*mask # removing hydrofracture water, multipling z by a mask to only take out the ice thickness of 4
            
            th2 = mask + sft_11 + sft_m11 + sft_12 + sft_m12
            th = th-(hf_dmg*th2).astype(int)
            th=np.maximum(th,np.zeros((n,n))) # this was changed from matlab th = max(th,zeros(n));
            if (big_save_on):
                #zs_big.append(z)
                #ths_big.append(th)
                bst=bst + 1
                #i = i+1
                #np.append(zs_big, [z],axis = 0) 
                #np.append(ths_big, [th],axis = 0)
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
                
        av_ind = av -1 # keeping track of av number so that the index is one less than it actually is 
        if av > 0:
            if av_plt[av_ind] >= 1:
                av_plt[av_ind] = av_plt[av_ind] + 1
            else:
                av_plt[av_ind]=1 # do the minue one since av is a number and iterations start at 0 so make sure to not start at 1 indices 
        zs[i]=np.mean(z)
        thsp[i]=np.mean(th)
        #zs[i]=np.mean([v for index,v in np.ndenumerate(z)]) # take the mean of the whole array 
        #thsp[i]=np.mean([vth for indexth,vth in np.ndenumerate(th)])
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
         
