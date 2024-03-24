#bibliotheque
#biblio interrupt mettre toute les fonctions par type (parrallélisme, interruptions, tampon)
#biblio cohérente avec le programme
#un fichier python correspond à une classe, biblio donnée de fonction

import threading
from threading import Semaphore
from time import sleep
from random import uniform
import networkx as nx
import matplotlib.pyplot as plt
import time


#classe tache
class Task:
    name = ""
    reads = []
    writes = []
    run = None

    #constructeur
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run





class TaskSystem:
    list_task = []
    contraints_preced = {} #dictionnaire

    def __init__(self, list_task, contraints_preced):
        self.list_task = list_task
        self.contraints_preced = contraints_preced


    #retourne liste des tâches qui s'éxecute avant nomTache
    def getDependencies(self, nomTache):
         return self.contraints_preced.get(nomTache)

    #execution sequentielle
    """Parcourez la liste de précédence de chaque tâche dans le système.
    Pour chaque tâche, exécutez-la seulement si toutes ses tâches précédentes ont été exécutées.
    Marquez chaque tâche comme exécutée après son exécution.
    Répétez les étapes 2 et 3 jusqu'à ce que toutes les tâches aient été exécutées"""
    


    def runSeq(self):
        list_exec = []  # Liste pour stocker l'ordre d'exécution des tâches
        success_list = []  # Liste pour indiquer si chaque tâche a été exécutée avec succès

        #si la dépendances de la tâche actuelle n'a pas été executé (n'apparait pas dans list_run) alors on met dependices_satisfied a false
        for task in self.list_task:
            dependencies = self.getDependencies(task.name)
            dependencies_satisfied = True
            for dep in dependencies:
                if dep not in list_exec:
                    dependencies_satisfied = False
                    print(f"Problème : Les dépendances de la tâche {task.name} ne sont pas toutes satisfaites.")
                    success_list.append(False)  # Indiquer que la tâche n'a pas été exécutée avec succès
                    break

            if dependencies_satisfied:
                task.run()
                list_exec.append(task.name)
                success_list.append(True)  # Indiquer que la tâche a été exécutée avec succès

        return list_exec, success_list
        





    #verifie condtion de bernstein
    #si vrai alors les taches sont non interferentes sinon elles sont interferentes
    """Vérifier les conditions de Bernstein entre deux tâches"""
    def cond_bernstein(self, task1, task2):
        if(task1==task2):
            print("ce sont les mêmes tâches")
            return False
        else :
            # T1 ne doit pas lire ce que T2 écrit
            for read_task in task1.reads:
                if read_task in task2.writes:
                    print(f"{task1.name} interfere avec {task2.name}")
                    return False
            # T2 ne doit pas lire ce que T1 écrit
            for read_task in task2.reads:
                if read_task in task1.writes:
                    print(f"{task1.name} interfere avec {task2.name}")
                    return False
            # T1 et T2 ne doivent pas écrire dans les mêmes cellules
            for write_task in task1.writes:
                if write_task in task2.writes:
                    print(f"{task1.name} interfere avec {task2.name}")
                    return False

            print(f"{task1.name} non interfere avec {task2.name}")
            return True
            

   #execution parallèle 
   #Un sémaphore est utilisé pour contrôler l'accès à une ressource partagée. 
   #Par défaut, un sémaphore est initialisé avec une valeur de 1, ce qui signifie qu'un seul thread peut acquérir le sémaphore à la fois

    def run(self):
        result_dict = {}  # Dictionnaire pour stocker les tâches interférentes pour chaque tâche

        # Créer un sémaphore global pour assurer l'exclusivité mutuelle lors de la mise à jour du dictionnaire résultant
        semaphore = threading.Semaphore(1)

        # Fonction pour rechercher les tâches interférentes pour une tâche donnée
        def find_interfering_tasks(task1, task_list, start_index, end_index, result_dict, semaphore):
            interfering_tasks = set()  # Ensemble pour stocker les tâches interférentes avec task1

            # Parcourir les tâches pour trouver les tâches interférentes avec task1
            for task2 in task_list[start_index:end_index]:
                if not self.cond_bernstein(task1, task2):
                    interfering_tasks.add(task2.name)

            # Mettre à jour le dictionnaire résultant en acquérant le sémaphore global
            semaphore.acquire()
            result_dict[task1.name] = list(interfering_tasks)
            semaphore.release()

        # Créer une liste pour stocker les threads
        threads = []

        # Parcourir les tâches pour diviser le travail entre les threads
        for i, task1 in enumerate(self.list_task):
            # Créer un thread pour chaque tâche
            thread = threading.Thread(target=find_interfering_tasks, args=(task1, self.list_task, i + 1, len(self.list_task), result_dict, semaphore))
            threads.append(thread)

        # Démarrer tous les threads
        for thread in threads:
            thread.start()

        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()

        return result_dict


    #rajouter semaphore


    def redundances(self):
        # Récupérer le graphe de parallélisme maximal
        parallel_graph = self.run()
        redundant_edges = []  # Liste pour stocker les arcs redondants
        visited = set()  # Ensemble pour stocker les nœuds déjà visités

        # Fonction récursive pour parcourir le graphe en profondeur
        def parcours_graph(current_task, parent_task):
           
            # Marquer le nœud actuel comme visité
            visited.add(current_task)

            # Récupérer les contraintes de précédence pour la tâche actuelle
            precedence_constraints = self.getDependencies(current_task)

            # Parcourir les tâches voisines du nœud actuel
            for neighbor_task in parallel_graph.get(current_task, []):
                # Vérifier si l'arc n'a pas de contrainte de précédence
                if (parent_task, neighbor_task) not in precedence_constraints:
                    redundant_edges.append((parent_task, neighbor_task))

                # Continuer la recherche en profondeur à partir du voisin
                parcours_graph(neighbor_task, current_task)

        # Appeler la fonction parcours_graph pour chaque nœud du graphe
        for task in parallel_graph :
            if task not in visited:
                parcours_graph(task, None)

        return redundant_edges



    
    def draw(self):
        # Obtenir les informations sur les tâches interférentes de la fonction run()
        result_dict = self.run()

        # Créer un graphe dirigé
        G = nx.DiGraph()

        # Ajouter les nœuds correspondant aux tâches de la liste des tâches
        for task in self.list_task:
            G.add_node(task.name)

        # Parcourir le dictionnaire des tâches interférentes et ajouter les arêtes
        for task, interfering_tasks in result_dict.items():
            for interfering_task in interfering_tasks:
                G.add_edge(task, interfering_task)

        # Supprimer les arcs redondants
        redundant_edges = self.redundances()
        G.remove_edges_from(redundant_edges)

        # Afficher le graphe
        plt.figure(figsize=(8, 6))
        nx.draw(G, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')
        plt.show()


        
    #test de déterminisme
            # si toute les tâches sont non interferentes alors déterministe
    def detTestRnd(self):
        pass


    #comparer temps d'execution séquentielle et parallèle
    #time(), perf_counter(), process_time()
    def parCost(self):

        start = time.perf_counter()
        self.runSeq()
        end = time.perf_counter()
        costRunSeq = end - start
        print("Temps d'exécution de runSeq : ", costRunSeq, "secondes")

        start = time.perf_counter()
        self.run()
        end = time.perf_counter()
        costRun = end - start
        print("Temps d'exécution de run : ", costRun, "secondes")



class InterruptManager:
    pass
