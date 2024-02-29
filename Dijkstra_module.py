import numpy as np
def setupgraph(G, b, s):
    G = G.astype(float)
    if s == 1:
        G[G == 0] = b
    elif s == 2:
        G[G == b] = 0
    return G


def exchangenode(G, a, b):
    # Exchange element at lumn a with element at column b
    buffer = np.copy(G[:, a:a+1]) # G[:, a:a+1] instead of G[:, a] to keep 2D shape
    G[:, a:a+1] = G[:, b:b+1]
    G[:, b:b+1] = buffer

    # Exchange element at row a with element at row b
    buffer = np.copy(G[a:a+1, :]) # G[a:a+1, :] instead of G[a, :] to keep 2D shape
    G[a:a+1, :] = G[b:b+1, :]
    G[b:b+1, :] = buffer
    return G


def listdijkstra(L, W, s, d):
    index = int(W.shape[0]-1)
    while index > 0:
        if W[1, d] == W[int(W.shape[0]-1), d]:
            L.append(int(s))
            index = 0
        else:
            index2 = int(W.shape[0])
            while int(index2) > 0:
                if W[int(index2)-1, d] < W[int(index2)-2, d]:
                    L.append(int(W[int(index2)-1, 0]))
                    L = listdijkstra(L, W, s, int(W[int(index2-1), 0]))
                    index2 = 0
                else:
                    index2= int(index2) - 1
            index = 0
    return L

def dijkstra(A, s, d):
    if s == d:
        e = 0
        L = [s]
    else:
        A = setupgraph(A,np.inf,1)
        if d == 1:
            d = s
        A = exchangenode(A,0,s)
        lengthA = A.shape[0]
        W = np.zeros(A.shape)
        for i in range(1,lengthA):
            W[0,i] = i
            W[1,i] = A[0,i]
        D = np.zeros((lengthA,2))
        for i in range(lengthA):
            D[i,0] = A[0,i]
            D[i,1] = i 
        D2 = D[1:len(D),:]
        L = 1
        while L <= (W.shape[0]-2):
            L = L + 1
            D2 = D2[D2[:,0].argsort()]
            k = D2[0,1]
            W[L,0] = k 
           

            D2 = D2[1:]
            
            for i in range(D2.shape[0]):
                k = int(k)
                l = D[int(D2[i,1]),0] 
                m = D[k,0]+A[k,int(D2[i,1])]
                if l>m:
                    D[int(D2[i,1]),0] = m
                    D2[i,0] = D[int(D2[i,1]),0]
            for i in range(1,A.shape[0]):
                W[L,i] = D[i,0]

        if d == s:
            L = [0]
        else:
            L = [d]
        e = W[W.shape[0]-1,d]
        L = listdijkstra(L,W,s,d)
    return e,L


