# -*- coding: utf-8 -*-


from copy import deepcopy
import itertools
import numpy as np
import argparse


        
def matrix_creation(path):
    """
    Fonction permettant de créer une matrice d'adjacence à partir d'un fichier .txt

    Parameters
    ----------
    path : str
        Chemin du fichier contenent le graphe.

    Returns
    -------
    matrix : np.array (int)
        Matrice d'adjacence.
    args : str
        Noms des noeuds du graphe.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.

    """
    with open(path) as file:
        lines = file.read().split()
    
    nb_args = 0
    args = []
    for line in lines:
        if 'arg' in line:
            nb_args += 1
            args.append(line.split('(')[1].split(')')[0])
            
    matrix = np.zeros(shape=(nb_args,nb_args), dtype=int)
    
    for line in lines:
        if 'att' in line:
            arg1 = line.split('(')[1].split(')')[0].split(',')[0]
            arg2 = line.split('(')[1].split(')')[0].split(',')[1]
            matrix[args.index(arg1)][args.index(arg2)] = 1
            
            
    ind = {}
    for arg in args:
        ind[arg] = args.index(arg)
            
    return matrix, args, ind
    




def combinations(args):
    """
    Fonction permettant d'avoir toutes les combinaisons de noeuds.

    Parameters
    ----------
    args : list
        Liste des noeuds (str).

    Returns
    -------
    c : list
        Liste de listes des différentes combinaisons.

    """
    c = []
    for a in range(len(args)+1):
        for s in itertools.combinations(args, a):
            c.append(list(s))
    return c






def conflict_free(matrix, combi, args, ind):
    """
    Fonction permettant de supprimer de la liste combi les listes dont les noeuds s'attaquent entre eux.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence du graphe.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.
    """
    def cf(ind, args):
        #Fonction permettant de savoir si la liste args est conflict-free (cette fonction est appelée pour chaque liste de combi)
        for i in args:
            for j in args:
                if matrix[ind[i]][ind[j]] == 1:
                    return False
        return True
    
    to_delete = []
    for c in combi:
        if cf(ind, c) == False:
            to_delete.append(c)
            
    for t in to_delete:
        combi.remove(t)
            





def defends_itself(matrix, combi, args, ind):
    """
    Fonction permettant de supprimer de la liste combi les listes de noeuds qui ne se defendent pas de tous leurs attaquants.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.
    """
    def df(ind, args):
        #Fonction permettant de savoir si un ensemble de noeuds se défend de tous ses attaquants (appelée pour chaque liste de combi)
        for arg in args:
            for i in range(len(matrix)):
                if matrix[i][ind[arg]] == 1:
                    boolean = False
                    for j in args:
                        if matrix[ind[j]][i] == 1:
                            boolean = True
                    if boolean == False:
                        return False
        return True
    
    to_delete = []
    for c in combi:
        if df(ind, c) == False:
            to_delete.append(c)
            
    for t in to_delete:
        combi.remove(t)
        
        
        
        
        
        
def complete(matrix, combi, args, ind):
    """
    Fonction permettant de trouver toutes les extensions complètes parmi les listes de combi.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.

    Returns
    -------
    list
        Liste des extensions complètes.

    """
    def defended_by_args(node, args):
        #Vérifie si un noeud 'node' est défendu par tous les noeuds de la liste 'args'. 
        l = [False for a in range(sum(matrix.T[node]))]
        j = 0

        for i in range(len(matrix)):

            if matrix[i][node] == 1:

                boolean = False
                for arg in args:

                    if matrix[ind[arg]][i] == 1:
                        boolean = True

                if boolean == True:
                    l[j] = True
                j += 1
                
        return False if False in l else True
    
    def co(args):
        #Fonction permettant de savoir si tous les noeuds d'un ensemble sont défendus ce même ensemble (la liste args).
        for i in range(len(matrix)):
            if list(ind.keys())[list(ind.values()).index(i)] not in args:
                if defended_by_args(i, args) == True:
                    return False
        return True
                
            

    to_delete = []
    for c in combi:
        if co(c) == False:
            to_delete.append(c)
            
    c_copy = deepcopy(combi)
    for t in to_delete:
        c_copy.remove(t)
        
    return c_copy
        
def grounded(matrix, combi, args, ind):
    """
    Fonction permettant de trouver toutes l'extension grounded parmi les listes de combi.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.

    Returns
    -------
    list
        L'extensions grounded.

    """
    def not_attacked(matrix):
        #Retourne la liste des noeuds qui ne sont pas attqués.
        l = []
        for i in range(len(matrix)):
            if sum(matrix.T[i]) == 0:
                l.append(i)
        return l
    
    m_copy = deepcopy(matrix)
    
    acc = set()
    rej = set()
    loop = True
    while(loop):
        na = not_attacked(m_copy)
        length = len(acc)
        for i in na:
            if i not in rej:
                for j in range(len(m_copy)):
                    if m_copy[i][j] == 1:
                        m_copy[:,j] = 0
                        m_copy[j,:] = 0
                        rej.add(j)
        
        for i in range(len(matrix)):
            if sum(m_copy.T[i]) == 0 and i not in rej:
                acc.add(i)

        if length == len(acc):
            loop = False
    
    re = []
    for i in acc:
        re.append(list(ind.keys())[list(ind.values()).index(i)])
    return re
    


def DC_CO(matrix, combi, args, ind, arg):
    """
    Fonction qui permet de parcourir la liste des combinaisons 'combi', si on trouve une extension complète et que l'argument s'y trouve, alors on retourne 'YES', 'NO' sinon.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.
    arg : str
        Argument à trouver dans les extensions complètes.

    Returns
    -------
    str
        YES si on trouve une extension complète qui contient arg, NO sinon.

    """
    comb = deepcopy(combi)
    for c in comb:
        cc = [deepcopy(c)]
        conflict_free(matrix, cc, args, ind)
        defends_itself(matrix, cc, args, ind)
        if complete(matrix, cc, args, ind) == [c] and cc!= [] and arg in cc[0]:
            return 'YES'
    return 'NO'
            




def stable(matrix, combi, args, ind):
    """
    Fonction qui renvoie la liste des extensions stables.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.

    Returns
    -------
    list
        Liste des extensions stables.

    """
    def st(ind, args):
        #Vérifie pour la liste 'args' si elle attaque tout ce qui est en dehors de la liste.
        for i in range(len(matrix)):
            if list(ind.keys())[list(ind.values()).index(i)] not in args:
                boolean = False
                for arg in args:
                    if matrix[ind[arg]][i] == 1:
                        boolean = True
                if boolean == False:
                    return False
        return True
        
        
    
    
    to_delete = []
    for c in combi:
        if st(ind, c) == False:
            to_delete.append(c)
            
    c_copy = deepcopy(combi)
    for t in to_delete:
        c_copy.remove(t)
        
    if [] in c_copy:
        c_copy.remove([])
    return c_copy



def SE_ST(matrix, combi, args, ind):
    """
    Fonction qui permet de parcourir la liste des combinaisons 'combi', on retourne une extension stable si on la trouve, 'NO' sinon.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.

    Returns
    -------
    str / list
        'NO' si pas d'extension stable, la liste contenant l'extension sinon.

    """
    comb = deepcopy(combi)
    comb.remove([])
    for c in comb:
        cc = [deepcopy(c)]
        conflict_free(matrix, cc, args, ind)
        defends_itself(matrix, cc, args, ind)
        co = complete(matrix, cc, args, ind)
        st = stable(matrix, co, args, ind)
        if st != []:
            return st[0]
    return 'NO'

def DC_ST(matrix, combi, args, ind, arg):
    """
    Fonction qui permet de parcourir la liste des combinaisons 'combi',
    si on trouve une extension stable et que l'argument s'y trouve, alors on retourne 'YES', 'NO' sinon.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.
    arg : TYPE
        L'argument à trouver dans une des extensions.

    Returns
    -------
    str
        YES si on trouve une extension complète qui contient arg, NO sinon.

    """
    comb = deepcopy(combi)
    comb.remove([])
    for c in comb:
        cc = [deepcopy(c)]
        conflict_free(matrix, cc, args, ind)
        defends_itself(matrix, cc, args, ind)
        co = complete(matrix, cc, args, ind)
        st = stable(matrix, co, args, ind)
        if st != [] and arg in st[0]:
            return 'YES'
    return 'NO'


def DS_CO(matrix, combi, args, ind, arg):
    """
    Renvoie 'YES' si l'argument arg est dans toutes les extensions complètes, 'NO' sinon.

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.
    arg : TYPE
        L'argument à trouver dans une des extensions.

    Returns
    -------
    str
        'YES' si l'argument arg est dans toutes les extensions complètes, 'NO' sinon.

    """
    #On vérifie d'abord si l'argument est dans la grounded, si ce n'est pas le cas on retourne 'NO'.
    gr = grounded(matrix, combi, args, ind)
    if gr == []:
        return 'NO'
    elif arg not in gr:
        return 'NO'
    
    at_least_one_complete = False
    comb = deepcopy(combi)
    for c in comb:
        cc = [deepcopy(c)]
        conflict_free(matrix, cc, args, ind)
        defends_itself(matrix, cc, args, ind)
        co = complete(matrix, cc, args, ind)
        if co!= [] and co == [c]:
            at_least_one_complete = True
            if arg not in co[0]:
                return 'NO'
            
    if at_least_one_complete == False:
        return 'NO'
    
    return 'YES'



def DS_ST(matrix, combi, args, ind, arg):
    """
    Renvoie 'YES' si l'argument arg est dans toutes les extensions stables, 'NO' sinon.
    S'il n'y a pas d'extension stable, tous les arguments sont sceptiquement acceptés (donc 'YES').

    Parameters
    ----------
    matrix : np.array
        Matrice d'adjacence.
    combi : list
        Liste des combinaisons de noeuds.
    args : list
        Liste des noeuds.
    ind : dict
        Dictionnaire associant les noms des noeuds avec leur index dans la matrice.
    arg : TYPE
        L'argument à trouver dans une des extensions.

    Returns
    -------
    str
        'YES' si l'argument arg est dans toutes les extensions stables, 'NO' sinon.

    """
    comb = deepcopy(combi)
    comb.remove([])
    at_least_one_stable = False
    for c in comb:
        cc = [deepcopy(c)]
        conflict_free(matrix, cc, args, ind)
        defends_itself(matrix, cc, args, ind)
        co = complete(matrix, cc, args, ind)
        st = stable(matrix, co, args, ind)
        if st != [] and st == [c]:
            at_least_one_stable = True
            if arg not in st[0]:
                return 'NO'
    #S'il n'y a pas d'extension stable, tous les arguments sont sceptiquement acceptés.
    if at_least_one_stable == False and arg in combi[-1]:
        return 'YES'
    
    if arg in combi[-1]:
        return 'YES'
    return 'NO'

def print_ext(l):
    """
    Affichage d'une liste

    Parameters
    ----------
    l : list
        Liste à afficher.

    Returns
    -------
    li : list
        Liste transformée.

    """
    if type(l) == str:
        return l
    
    li = '['
    for i in range(len(l)):
        li += l[i]
        if i != len(l)-1:
            li += ','
    li += ']'
    return li


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='task')
    parser.add_argument('-f', dest='file')
    parser.add_argument('-a', dest='arg')
    params = parser.parse_args()
    
    
    matrix, args, ind = matrix_creation(params.file)
    combi = combinations(args)
    
    
    if 'CO' in params.task:
        if 'SE' in params.task:
            print(print_ext(grounded(matrix, combi, args, ind)))
        if 'DC' in params.task:
            if params.arg in grounded(matrix, combi, args, ind):
                print('YES')
            else:
                print(DC_CO(matrix, combi, args, ind, params.arg))
        if 'DS' in params.task:
            print(DS_CO(matrix, combi, args, ind, params.arg))
            
            
    if 'ST' in params.task:
        if 'SE' in params.task:
            print(print_ext(SE_ST(matrix, combi, args, ind)))
        if 'DC' in params.task:
            print(DC_ST(matrix, combi, args, ind, params.arg))
        if 'DS' in params.task:
            print(DS_ST(matrix, combi, args, ind, params.arg))


    




