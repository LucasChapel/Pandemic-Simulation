#Projet épidémie - Lucas Chapel

"""
Ce programme a pour objectif de simuler graphiquement une épidémie avec des
paramètres modifiables.
"""


import random as rnd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import time
import tkinter as tk


#Initialisation de constantes (facilement modifiables si souhaité)
DUREE_CONTAGION = 10
PROBA_MORT = 0.5


#Initialisation de la fenetre tkinter et du canvas qu'elle contient
fenetre = tk.Tk()
fenetre.geometry("500x500+500+150")
fenetre.title("")
figure = plt.Figure()
a = figure.add_subplot(111)
a.tick_params(axis='both', which='both', bottom=False,
                    top=False, labelbottom=False, right=False,
                    left=False, labelleft=False)
canvas = FigureCanvasTkAgg(figure, master=fenetre)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)



class Individu:
    """ 
    Cette classe permet d'instancier des individus ayant comme attributs 
    leur statut d'infection, leurs coordonnées (x,y) et le nombre de jours 
    d'infection restants.
    
    Méthodes:
    - infection : l'individu est contaminé
    - mort: l'individu décède
    - mouvement_alea: l'individu bouge aléatoirement dans un rayon de 5 autour de lui
    - jour_passe : un jour passe pour l'individu
    """
    def __init__(self,statut,x,y,jours_restants):
        self.statut  = statut
        self.x = x
        self.y = y
        self.jours_restants = jours_restants

    def infection(self):
        self.statut  = "positif"

    def mort(self):
        self.statut = "mort"

    def mouvement_alea(self):
        cord_x = rnd.randint(-5,5)
        cord_y = rnd.randint(-5,5)
        if ( 0 <= (self.x + cord_x) <= 100) and (0 <= (self.y + cord_y) <= 100):
           self.x += cord_x
           self.y += cord_y

    def jour_passe(self):
        self.jours_restants-=1

    

def graphique(pop):
    """
    Cette fonction représente graphiquement la population
    (liste d'instances de la classe Individu) passée en
    argument dans une fenêtre tkinter. Elle modifie
    la fenêtre déja existante pour l'adapter
    à la population pop.
    
    Code couleur:
    - Individus négatifs: vert
    - Individus positifs: rouge
    - Individus décédés: noir
    - Individus guéris (immunisés): jaune
    """
    
    x_negatif = []
    y_negatif = []
    
    x_positif = []
    y_positif = []

    x_gueri = []
    y_gueri = []

    x_mort = []
    y_mort = []

    for e in pop:
        if e.statut == "negatif":
            x_negatif.append(e.x)
            y_negatif.append(e.y)

        if e.statut == "positif":
            x_positif.append(e.x)
            y_positif.append(e.y)

        if e.statut == "gueri":
            x_gueri.append(e.x)
            y_gueri.append(e.y)

        if e.statut == "mort":
            x_mort.append(e.x)
            y_mort.append(e.y)

    a.set_title('Epidémie')
    
    a.scatter(x_negatif, y_negatif, c="green", marker='o', s=5)
    a.scatter(x_positif, y_positif, c="red", marker='o', s=5)
    a.scatter(x_gueri, y_gueri, c="yellow", marker='o', s=5)
    a.scatter(x_mort, y_mort, c="black", marker='o', s=5)

    canvas.draw()
    canvas.flush_events()

    time.sleep(0.3)

    a.clear()
    
    return 



def population_negative(n):
    """
    Cette fonction créer une population saine de taille n.
    Un individu est sain si son statut est "negatif"
    int -> list
    """
    pop = []
    for i in range (n):
        x = rnd.randint(0,100)
        y = rnd.randint(0,100)
        pop.append(Individu("negatif",x,y,0))
    return pop



def contamination(r0, I1, voisins):
    """
    Les r0 plus proches voisins de I1 sont contaminés (leur statut devient "positif").
    Paramètres: int, Individu, list
    """
    
    x = I1.x
    y = I1.y
    
    liste_distances = []
    
    for e in voisins:
        distance = math.sqrt((e.x - x)**2 + (e.y - y)**2)
        liste_distances.append((e,distance))
    
    liste_distances.sort(key = lambda x: x[1])

    for i in range (r0):
        if len(liste_distances)>i:
            liste_distances[i][0].statut = "positif"
            liste_distances[i][0].jours_restants = DUREE_CONTAGION

    return



def voisins(pop, I):
    """
    Cette fonction renvoie une liste contenant les voisins de I négatifs.
    On considère un voisin un individu qui se situe dans un rayon de 3 de I.
    list, Individu -> list
    """
    voisins = []

    x = I.x
    y = I.y
    
    for e in pop:
        distance = math.sqrt((e.x - x)**2 + (e.y - y)**2)
        if distance<=3 and e.statut == "negatif":
            voisins.append(e)

    return voisins



def affiche_informations(pop):
    """
    Cette fonction affiche dans la console les informations suivantes
    sur la population pop passée en argument:
    - Nombre d'individus positifs
    - Nombre d'individus négatifs
    - Nombre d'individus gueris
    - Nombre d'individus décédés
    - Nombre d'individus vivants
    """
    compteur_positif = 0
    compteur_negatif = 0
    compteur_gueri = 0
    compteur_mort = 0

    for e in pop:
        if e.statut == "positif":
            compteur_positif += 1
            
        if e.statut == "negatif":
            compteur_negatif += 1

        if e.statut == "gueri":
            compteur_gueri += 1

        if e.statut == "mort":
            compteur_mort += 1

    print("Nombre d'individus positifs: " + str(compteur_positif))
    print("Nombre d'individus negatifs: " + str(compteur_negatif))
    print("Nombre d'individus gueris: " + str(compteur_gueri))
    print("Nombre d'individus décédés: " + str(compteur_mort))
    print("Nombre d'individus vivants: " + str(compteur_positif+compteur_negatif+compteur_gueri))
    print("")



def test_jours_restants(pop):
    """
    Au sein de la population pop passée en argument, tous les individus
    positifs avec 0 jours restans changent de statut: soit "gueri",
    soit "negatif" (avec une probabilite egale d'etre gueri (immunise)
    ou de simplement redevenir negatif (encore contaminable))

    paramètre: list
    """
    for e in pop:
        if e.statut == "positif" and e.jours_restants == 0:
            i = rnd.randint(0,1)
            if i==0:
                e.statut = "gueri"
            elif i==1:
                e.statut = "negatif"
    return



def aucun_positif(pop):
    """
    Cette fonction vérifie si aucun individu de la population pop
    (liste d'instances de la classe Individu) est positif.
    Elle renvoie True si c'est le cas, False sinon.
    list -> Bool
    """
    for e in pop:
        if e.statut == "positif":
            return False
    return True



def epidemie(taille, r0, proba_mort):
    """
    Cette fonction simule l'épidémie en utilisant toutes les fonctions
    précédentes. L'épidémie s'arrête quand le virus a disparu
    (tous les individus sont décédés, négatifs ou guéris).
    Probabilité de mort d'un individu positif chaque jour: proba_mort %
    """
    
    jour = 0

    pop = population_negative(taille)

    #creation du patient 0
    pop[0].statut = "positif"
    pop[0].jours_restants = DUREE_CONTAGION

    
    while aucun_positif(pop)!=True:
        
        jour+=1

        graphique(pop)
        
        print("Jour n°"+str(jour))

        affiche_informations(pop)

        test_jours_restants(pop)

        for e in pop:
            
            if e.statut == "positif":
                e.jour_passe()

                v = voisins(pop, e)

                contamination(r0, e, v)

                p = rnd.randint(1,(100//proba_mort))
                
                if p == 1:
                    e.statut = "mort"
            
            if e.statut != "mort":
                e.mouvement_alea()


    # Représentation et affichage des informations du dernier jour
    jour+=1
    
    graphique(pop)
    
    print("Jour n°"+str(jour))
    affiche_informations(pop)
    print("")
    print("Virus battu en " + str(jour) + " jours.")
    
    return



def main():
    """
    Cette fonction commence la simulation de l'épidémie en fonction
    des paramètres demandés à l'utilisateur.
    """
    
    print("Bienvenue dans ce simulateur d'épidémie.")
    print("Veuillez choisir les paramètres de votre épidémie:")

    
    while True:
        try:
            taille = int(input("Choisissez la taille de la population (<2000 conseillé) : "))
            assert type(taille)==int and taille>=2
            break
        
        except ValueError:
            print("Veuillez entrer un entier supérieur ou égal à 2")
            
        except AssertionError:
            print("Veuillez entrer un entier supérieur ou égal à 2")


    
    while True:
        try:
            r0 = int(input("Chosissez votre r0: "))
            assert type(r0)==int and r0>=1
            break

        except ValueError:
            print("Veuillez entrer un entier supérieur ou égal à 1")
            
        except AssertionError:
            print("Veuillez entrer un entier supérieur ou égal à 1")

    print("")
    
    epidemie(taille, r0, PROBA_MORT)

    tk.mainloop()

main()
