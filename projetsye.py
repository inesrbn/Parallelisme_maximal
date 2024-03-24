#1. obtenir le système de tâches de parallélisme maximal réunissant les tâches en entrée,
#2. exécuter le système de tâches de façon séquentielle, tout en respectant les contraintes de précédence,
#3. exécuter le système de tâches en parallèle, tout en respectant les contraintes de précédence.



from projetsyebiblio import *





#tache 


"""def runT1():
    global X
    X = 1

def runT2():
    global Y
    Y = 2

def runTsomme():
    global X, Y, Z
    Z = X + Y
"""


X = None
Y = None
Z = None
A = None
B = None
C = None

def runT1():
    global X
    X = 1000  # Création d'une liste avec 1000 éléments, tous égaux à 1

def runT2():
    global Y, X
    Y = X * 1000  # Réplication de la liste X 1000 fois

def runT3():
    global Z, X
    Z = X * 1000  # Réplication de la liste X 1000 fois

def runT4():
    global A, Y, Z
    A = Y + Z # Addition élément par élément des listes Y et Z

def runT5():
    global B, Z
    B = Z * 1000  # Réplication de la liste Z 1000 fois

def runT6():
    global C, A, B
    C = A + B # Création d'une liste avec 1000 éléments, tous égaux à 1

#t1 = Task("T1",[], ["X"], runT1)
#t2 = Task("T2",[], ["Y"], runT2)
#tSomme = Task("somme", ["X", "Y"], ["Z"], runTsomme)


t1 = Task("T1",["X"], ["A"], runT1)
t2 = Task("T2",["Z", "A"], ["X"], runT2)
t3 = Task("T3",["Z", "A"], ["B"], runT3)
t4 = Task("T4",["A"], ["Y"], runT4)
t5 = Task("T5",["B"], ["B"], runT5)
t6 = Task("T6",["X","Y"], ["A"], runT6)


#t1.run()
#t2.run()
#tSomme.run()
#print(X)
#print(Y)
#print(Z)




#systeme de tache
#s1 = TaskSystem([t1,t2, tSomme], {"T1": [], "T2": [], "somme": ["T1", "T2"]})
#s2 = TaskSystem([t1,t2, tSomme], {"T1": ["T2"], "T2": [], "somme": ["T1", "T2"]})
#s3 = TaskSystem([t1,t2, tSomme], {"T1": ["T2"], "T2": [], "somme": ["T2"]})
#s4 = TaskSystem([t1,t2, tSomme], {"T1": [], "T2": [], "somme": []})

s5 = TaskSystem([t1,t2, t3, t4, t5, t6], {"T1": [], "T2": ["T1"], "T3": ["T1"], "T4": ["T2","T3"], "T5": ["T3"], "T6": ["T4","T5"]})
#print(s1.getDependencies("T2"))
#print(s1.cond_bernstein(t2,t2))
#print(s1.cond_bernstein(t2,tSomme))
#print(s1.runSeq())
#print(s2.runSeq())

#print(s1.run())
#print(s4.run())

#affichage
#s5.draw()
#print(s5.draw())
print(s5.parCost())



#systeme de tache peux ne pas refleter bon resultat car voir sa tache qui elle lit et qui elle lit pas 

