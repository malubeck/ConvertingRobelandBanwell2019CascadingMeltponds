def pos_loop(n, th_init, hf_dmg, frac, location, location2, heal_speed, i_value = 0, zs_big = 0, ths_big = 0, seed_val=42):
    
    iters=3*(n ** 2)
    rng = random_integer(seed_val)
    
    zs_all=np.nan * np.empty((iters**2,3,n,n))
    ths_all=np.nan * np.empty((iters**2,3,n,n))
    
    z, th, i, max_run_values = meltponds_nonconserve(n,iters,th_init,heal_speed,hf_dmg,rng,location, location2, frac, i_value, zs_big, ths_big)
    zs_all[0][0] = z
    ths_all[0][0]=th
    av, z, th  = mask(n, hf_dmg, z, th, av_val)
    zs_all[0][1] = z
    ths_all[0][1]=th
    z, th = grid_adjust(n, z, th)
    zs_all[0][2] = z
    ths_all[0][2]=th
    #print(zs_all)
    print(max_run_values)
    for step in range(0,max_run_values):
        #print(step)
        point = step + 1
        #print(point)
        z, th, i, max_run_values = meltponds_nonconserve(n,iters,th_init,heal_speed,hf_dmg,rng,location, location2, frac, point, z, th)
        zs_all[point][0] = z
        ths_all[point][0]=th
        av, z, th  = mask(n, hf_dmg, z, th, av_val)
        zs_all[point][1] = z
        ths_all[point][1]=th
        z, th = grid_adjust(n, z, th)
        zs_all[point][2] = z
        ths_all[point][2]=th
        
    
    keep_z = 0
    for sheet in range(len(zs_all)):
        if (np.isnan(zs_all[sheet][0]).any()):
            keep_z +=0
        else:
            keep_z += 1 
            
    keep_th = 0
    for sheet in range(len(ths_all)):
        if (np.isnan(ths_all[sheet][0]).any()):
            keep_th +=0
        else:
            keep_th += 1 
           
    zs_timeseries = zs_all[0:keep_z]
    ths_timeseries = ths_all[0:keep_th]
    
        
    return zs_timeseries, ths_timeseries

 

