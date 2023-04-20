
import numpy as np

def setupgraph(A, val, diag):
    if diag == 1:
        np.fill_diagonal(A, val)
    else:
        A[A==0] = val
    return A

def exchangenode(A, n1, n2=1):
    A[[n1-1, n2-1],:] = A[[n2-1, n1-1],:]
    A[:,[n1-1, n2-1]] = A[:,[n2-1, n1-1]]
    return A

def listdijkstra(L, W, s, d):
    while d != s:
        L.insert(0, np.where(W[:,d] == min(W[:,d]))[0][0]+1)
        d = L[0]-1
    return L

def dijkstra(A, s, d):
    if s == d:
        e = 0
        L = [s]
    else:
        A = setupgraph(A, np.inf, 1)
        if d == 1:
            d = s
        A = exchangenode(A, 1, s)
        lengthA = A.shape[0]
        W = np.zeros((lengthA, lengthA))
        for i in range(1, lengthA):
            W[0,i] = i
            W[1,i] = A[0,i]
        D = np.zeros((lengthA, 2))
        for i in range(lengthA):
            D[i,0] = A[0,i]
            D[i,1] = i
        D2 = D[1:,:]
        L = [2]
        while L[-1] <= (W.shape[0]-1):
            L.append(L[-1]+1)
            D2 = D2[D2[:,0].argsort()]
            k = int(D2[0,1])
            W[L[-1]-1,0] = k+1
            D2 = np.delete(D2, 0, 0)
            for i in range(D2.shape[0]):
                if D[int(D2[i,1]),0] > (D[k,0] + A[k,int(D2[i,1])]):
                    D[int(D2[i,1]),0] = D[k,0] + A[k,int(D2[i,1])]
                    D2[i,0] = D[int(D2[i,1]),0]
            for i in range(1, lengthA):
                W[L[-1]-1,i] = D[i,0]
        if d == s:
            L = [1]
        else:
            L = [d]
        e = W[-1,d-1]
        L = listdijkstra(L, W, s-1, d-1)
    return e, L
