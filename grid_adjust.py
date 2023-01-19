def grid_adjust(n, z, th):
    
    z_adj = np.roll(z,axis=0, shift=1)
    z_adj[0][:] = 0
    
    th_adj = np.roll(th,axis=0, shift=1)
    th_adj[0][:] = 4
    
    return z_adj, th_adj
