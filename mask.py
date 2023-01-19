def mask(n, hf_dmg, z, th, av_val=0):
    #try:
    #if av_val > 0:
    av = av_val
    #except: 
    #av = 0
    
    #print(av)
    mask = np.empty((n,n))
    for row in range(len(z)):
        for col in range(len(z)):
            if (z[row][col] > 0) & (z[row][col] >= th[row][col]):
                mask[row][col] = 1
            else:
                mask[row][col] = 0
    mask = mask.astype(int)
    mask_sum = mask.sum()
    
    if (mask.sum() == 0):
        print("This step will not have any hydrofracture locations.")     
    elif (mask.sum() > 0): # changed to if from while
        av = int(av + mask_sum + 0.1)

        sft_11=np.roll(mask,1)
        sft_11[0][:]=0
        sft_m11=np.roll(mask,-1) 
        sft_m11[-1][:]=0
        sft_12=np.roll(mask,[1,2]) 
        sft_12[:][0]=0 
        sft_m12=np.roll(mask,[-1,2])
        sft_m12[:][-1]=0
        
        # rolling this mask causes the 1 on the mask to go aroung the point of hydrofracture so then thats why the local areas is damaged
        z= z-z*mask # removing hydrofracture water, multipling z by a mask to only take out the ice thickness of 4

        th2 = mask + sft_11 + sft_m11 + sft_12 + sft_m12
        th = th-(hf_dmg*th2).astype(int)
        th=np.maximum(th,np.zeros((n,n))) 
        #if (big_save_on):
            #zs_big.append(z)
            #ths_big.append(th)
            #bst=bst + 1
            #i = i+1
            #np.append(zs_big, [z],axis = 0) 
            #np.append(ths_big, [th],axis = 0)
            #zs_big[bst][:][:] = z
            #ths_big[bst][:][:] = th
    else:
        print("No mask sum should be less than 0")
    
    step_z = np.empty((n,n))
    step_th = np.empty((n,n))
    step_z = z.astype(int)
    step_th = th.astype(int)

    return av, step_z, step_th 
