# -*- coding: utf-8 -*-
class Dechet:
    """
    Classe modélisant un déchet
     Attributs
    --------
    poids_tonnes : float
        Poids en tonnes
        
    volume_m3 : float
        Volume en mètres cubes
        
    *args : tuple
        Tuple ou une liste de (poids, volume)

    """
    
    def __init__(self, poids_tonnes = None , volume_m3 = None, *args):
        self._poids_tonnes = poids_tonnes
        self._volume_m3 = volume_m3
        if self._poids_tonnes is not None :
            if self._volume_m3 is not None :
                # Vérifier que les valeurs de poids et de volume sont cohérentes
                self.check_poids_volume()
            else:
                # Cas seul le poids est indiqué : on calcule le volume
                self._volume_m3 = self._poids_tonnes*4
                
        else:
            if self._volume_m3 is not None :
                # Cas où seul le volume a été indiqué
                self._poids_tonnes = self._volume_m3/4
        
        
        if len(args) == 2 : # Cas où un tuple est renseigné
            self._poids_tonnes = args[0]
            self._volume_m3 = args[1]
            
    def check_poids_volume(self):
        # On calcule le volume à partir de la valeur de l'attribut poids
        calc_volume = self._poids_tonnes * 4
        if calc_volume != self._volume_m3: # TODO : lever une exception à la place du print
            print("Les poids et volumes indiqués ne sont pas cohérents. \
                  N.B. : 1 tonne de déchets = 4 m3 de déchets ")
             
    def __repr__(self):
        """
        Redéfinition de la méthode __repr__ pour afficher les attributs d'un objet Déchet
        
        """
        return '< Déchet: {} t, {} m3 >'.format(self._poids_tonnes, self._volume_m3)
    
    # getters
    @property
    def poids_tonnes(self):
        return self._poids_tonnes
    
    @poids_tonnes.setter
    def poids_tonnes(self, poids):
        self._poids_tonnes = poids
        self._volume_m3 = poids*4
    
    @property
    def volume_m3(self):
        return self._volume_m3
    
    @volume_m3.setter
    def volume_m3(self, volume):
        self._volume_m3 = volume
        self._poids_tonnes = volume/4
        
class DechetDomestique(Dechet):
    """
    Un déchet de type domestique
    """
    pass
    
class DechetOrganique(Dechet):
    """
    Un déchet de type organique
    """
    pass
    
class DechetMineral(Dechet):
    """
    Un déchet de type minéral
    """    
    pass
    
class DechetMetal(Dechet):
    """
    Un déchet de type métal
    """
    pass
    
class DechetMixte(Dechet):
    """
    Un déchet de type mixte
    """    
    pass

import pandas as pd
class TasDechets :
    """
    Classe modélisant un tas de déchets. 
    Un tas de déchet est composé de plusieurs types de déchets.
    
    Attributs
    ---------
    dechets : Dechet.Dechet
        Ensemble indifférencié de déchets dans le tas
        
    composition_dechets : pandas.Dataframe
        Détail des déchets qui composent le tas de déchets.
        L'attribut est un tableau de n colonnes et de 1 ligne, où :
            - Une colonne décrit un type de déchet
            - Une ligne contient un objet de la classe Dechet
    
    """
   
    def __init__(self, dechets = Dechet, *args):
        self._dechets = dechets
        self._composition_dechets = pd.DataFrame()

    def __add__(self, d = Dechet):
        """
        Redéfinition de la méthode d'addition.
        Permet d'ajouter un déchet au tas de déchet.

        Parameters
        ----------
        d : Dechet.Dechet
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self._dechets._poids_tonnes += d._poids_tonnes
        self._dechets._volume_m3 += d._volume_m3
   
    def __repr__(self):
        """
        Redéfinition de la méthode __repr__ pour afficher les attributs d'un objet Déchet
        
        """
        return '< Tas de déchet : {} t, {} m3 >'.format(self._dechets._poids_tonnes, self._dechets._volume_m3)
    
    # getters
    @property
    def dechets(self):
        return self._dechets
    
    @property
    def composition_dechets(self):
        return self._composition_dechets
    
    @property
    def volume_m3(self):
        return self._dechets.volume_m3
    
    @property
    def poids_tonnes(self):
        return self._dechets.poids_tonnes
    
    # setters
    @dechets.setter
    def dechets(self, d):
        self._dechets = d
    
    @composition_dechets.setter
    def composition_dechets(self, composition):
        self._composition_dechets = composition
        
    @volume_m3.setter
    def volume_m3(self, volume):
        self._dechets.volume_m3 = volume
        
    def calc_quantite_dechets_from_composition(self):
        """
        Méthode de calcul de la quantité de déchets à partir des différents types
        de déchets qui composent le tas, et qui sont renseignées dans l'attribut
        composition_dechets
        
        Returns
        -------
        None.

        """
        pass