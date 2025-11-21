import numpy as np
import random as rd
#---------------------------------------------------------------------
# Gera matriz de adjacências
def GerarProblema(n,min1,max1):    
    mat  = np.random.randint(min1,max1,(n,n))
    return mat
#---------------------------------------------------------------------
# Custo/lucro de uma solução
def Avalia(n,mat,sol):
    v = 0   
    for i in range(n-1):
        v += (mat[sol[i]][sol[i+1]])
    
    v += mat[sol[n-1]][sol[0]]    
    return v
#---------------------------------------------------------------------
def Ordena(p,f):
    aux = sorted(zip(p, f), key=lambda x: x[1], reverse=True) 
    p, f = zip(*aux)
    p = list(p)
    f = list(f)
    return p, f
#---------------------------------------------------------------------
# Gera a população inicial
def PopIni(n, tp):
    pop = np.array([np.random.permutation(n) for _ in range(tp)])
    return pop
#---------------------------------------------------------------------
# Calcula aptidao
def Aptidao(n,mat,p,tp):
    fit = np.zeros(tp,float)
    for i in range(tp):
        fit[i] = 1./Avalia(n,mat,p[i])
    soma = sum(fit)
    fit = fit/soma
    soma = sum(fit)
    return fit
#---------------------------------------------------------------------
# Operador Roleta
def Roleta(fit,tp):
    ale = rd.uniform(0,1)
    ind=0
    soma = fit[ind]
    while soma<ale and ind<tp-1:
        ind += 1
        soma += fit[ind]
    return ind
#---------------------------------------------------------------------
# Operador Torneio
def Torneio(tp,fit):
    p1 = rd.randrange(tp)
    p2 = rd.randrange(tp)
    if fit[p1]>fit[p2]:
        return p1
    else:
        return p2
#---------------------------------------------------------------------
# Operador de cruzamento
def Cruzamento(p1,p2,ponto,n):
    d1 = np.concatenate((p1[0:ponto],p2[ponto:n]))
    d2 = np.concatenate((p2[0:ponto],p1[ponto:n]))
    return d1, d2
#---------------------------------------------------------------------
# Operador de mutação- translocação
def Mutacao(d,n):
    pos1 = rd.randrange(n) 
    pos2 = rd.randrange(n)
    temp = d[pos1]
    d[pos1] = d[pos2] 
    d[pos2] = temp    
    return d
#---------------------------------------------------------------------
# Gera os descendentes
def Descendentes(n,pop,fit,tp,tc,tm):
    qd = 2*tp
    desc = np.zeros((qd,n),int)
    corte = rd.randint(1,n-1)
    i = 0
    while i<qd:
        p1 = pop[Roleta(fit,tp)]
        p2 = pop[Roleta(fit,tp)]
        if rd.uniform(0,1) <= tc:
            desc[i],desc[i+1] = Cruzamento(p1,p2,corte,n)
        else:
            desc[i],desc[i+1] = p1, p2
        if rd.uniform(0,1) <= tm:    
            desc[i] = Mutacao(desc[i],n)
        if rd.uniform(0,1) <= tm:    
            desc[i+1] = Mutacao(desc[i+1],n)
        i += 2
    return desc, corte, qd
#---------------------------------------------------------------------
def NovaPop(pop,desc,tp,ig):
    elite = int(ig*tp)
    for i in range(tp-elite):
        pop[i+elite] = desc[i]
    return pop
#---------------------------------------------------------------------
# AJUSTA SOLUÇÃO PARA ATENDER A RESTRIÇÃO PCV
def AjustaRestricao(n,desc,qd,corte):
    for i in range(qd):
        alfabeto = list(range(0,n))
        alfabeto = [x for x in alfabeto if x not in desc[i]]
        rd.shuffle(alfabeto)
        j = corte
        while(j<n and len(alfabeto)>0):
            if(desc[i][j] not in alfabeto):
                desc[i][j] = alfabeto[0]
                alfabeto.remove(alfabeto[0])
            j += 1
    return desc
#---------------------------------------------------------------------
def AlgoritmoGenetico(n,mat,tp,ng,tc,tm,ig):
    pop = PopIni(n,tp)

    fit = Aptidao(n,mat,pop,tp)
    pop, fit = Ordena(pop,fit)
    si = pop[0]
    vi = Avalia(n,mat,si)
    for _ in range(ng):
        desc, corte, qd = Descendentes(n,pop,fit,tp,tc,tm)
        desc = AjustaRestricao(n,desc,len(desc),corte)
        fit_d = Aptidao(n,mat,desc,qd)
        pop, fit = Ordena(pop,fit)
        desc, fit_d = Ordena(desc,fit_d)
        pop  = NovaPop(pop,desc,tp,ig)
        fit = Aptidao(n,mat,pop,tp)
    pop, fit = Ordena(pop,fit)
    sf = pop[0]
    vf = Avalia(n,mat,sf)
    return si, sf, vi, vf 
#---------------------------------------------------------------------
#---------------------------------------------------------------------
# MÓDULO PRINCIPAL
N    = 30   # quantidade de pontos
MIN1 = 10   # valor mínimo para matriz de adjacências
MAX1 = 100  # valor máximo para matriz de adjacências

TP   = 30    # tamanho da população
NG   = 300    # número de gerações
TC   = 0.9  # taxa de cruzamento
TM   = 0.1  # taxa de mutação
IG   = 0.2  # intervalo de geração

mat = GerarProblema(N,MIN1,MAX1)

si, sf, vi, vf = AlgoritmoGenetico(N,mat,TP,NG,TC,TM,IG)
print("Ganho: ",round((100.*abs(vi-vf))/vi),"%")
