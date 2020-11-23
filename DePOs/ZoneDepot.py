# -*- coding: utf-8 -*-
from .Dechets import Dechet, TasDechets
import pandas as pd

class ZoneDepot :
    """
    Classe modélisant une zone de dépôt.
    NB : pour gérer les héritages multiples & les méthodes __init__
    cf. https://he-arc.github.io/livre-python/super/index.html
    
    Attributs
    --------
    idZoneDepot : int
        Identifiant unique de la zone de dépôt
    
    tas_dechets : TasDechets
        Tas de déchet présent sur la zone de dépôt.
    
    suivi_dechets : list
        Suivi temporel de la quantité de déchets présents sur l'aire de dépose.
        L'attribut est une liste contenant des objets de type Dechet.
        A chaque passage d'un véhicule de collecte, l'attribut doit être mis à 
        jour pour contenir la nouvelle valeur du volume de déchets présents 
        sur la zone de dépôt.
    
    """     
    
    def __init__(self) :
        self._suivi_dechets = pd.DataFrame()

    def __repr__(self):
        """
        Redéfinition de la méthode __repr__ d'affichage des attributs d'un objet ZoneDepot
        """
        info = '< Zone de dépôt \n'
        if hasattr(self, 'idz'):
            info += 'ID : {} \n'.format(self.idz)
        info += 'Quantité de déchets {} t = {} m3'.format(self._tas_dechets.poids_tonnes, 
                                                          self._tas_dechets.volume_m3)
        info += '>'
        return info
    
    @property
    def idz(self) :
        return self._idz
    
    @idz.setter
    def idz(self, idZDepot):
        self._idz = idZDepot
    
    @property
    def tas_dechets(self):
        return self._tas_dechets
    
    @tas_dechets.setter
    def tas_dechets(self, nouveau_tas):
        self._tas_dechets = nouveau_tas
    
    @property
    def suivi_dechets(self) :
        return self._suivi_dechets
    
    @suivi_dechets.setter
    def suivi_dechets(self, nouveau_suivi):
        self._suivi_dechets = nouveau_suivi
    
    
    def update_suivi_dechets(self):
        """
        Méthode qui permet de mettre à jour l'indicateur de suivi de déchets.
        Dès qu'un véhicule s'y arrête pour charger ou décharger des déchets, 
        l'appel à cette méthode permet d'enregistrer la date d'arrivée du véhicule,
        et les nouvelles valeurs de volume et de poids des déchets.

        Returns
        -------
        None.

        """
        pass

class AireDepose(ZoneDepot) :
    """
    Classe modélisant une aire de dépose.
    Une aire de dépose contient une certaine quantité de déchet à vider.
    
    Attributs
    ---------
    suivi_chargement_vehicules : list
        Suivi temporel des véhicules arrivant à la zone pour collecter les déchets.
        A chaque passage d'un véhicule de collecte, l'attribut est mis à jour       
    """
    
    def __init__(self):
        super().__init__()
        self._suivi_chargement_vehicules = pd.DataFrame()
    
    @property
    def suivi_chargement_vehicules(self):
        return self._suivi_chargement_vehicules
            
class ZoneDepotFinal(ZoneDepot):
    """
    Classe modélisant une zone de dépôt final.
    Une zone de dépôt final ne contient initialement pas de déchets, 
    sur laquelle les véhicules de collecte vont décharger les déchets transportés.
    
    Attributs (non hérités)
    -----------------------
    nom : str
        Nom de la zone
    
    nature : str
        Nature de la zone
        
    suivi_dechargement_vehicules : dict
        Suivi temporel des véhicules arrivant à la zone pour y déposer leurs déchets
    
    """
    
    def __init__(self):
        self._suivi_dechargement_vehicules = pd.DataFrame()
        self._tas_dechets = TasDechets(Dechet(0))
    
    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, nom):
        self._nom = nom
    
    @property
    def nature(self):
        return self._nature
    
    @nature.setter
    def nature(self, nature):
        self._nature = nature
        
    @property
    def suivi_dechargement_vehicule(self):
        return self._suivi_dechargement_vehicules
    
class EcoSite(ZoneDepotFinal):
    pass
       
class ISDND(ZoneDepotFinal):
    pass

       
class ZoneStockageTemporaire(ZoneDepotFinal, AireDepose) : 
    """
    Classe modélisant une zone de stockage temporaire.
    Lorsqu'un véhicule arrive à une zone de stockage temporaire, il peut :
        - Se charger partiellement ou totalement des déchets présents sur la zone
        - Se décharger partiellement ou totalement les déchets qu'il contient
    
    Attributs (non hérités)
    -----------------------
    capacite_max : float
        Volume limite d'accueil des déchets, en m3
        
    """        
    
    @property
    def capacite_max_m3(self):
        return self._capacite_max_m3
    
    @capacite_max_m3.setter
    def capacite_max_m3(self, nv_capacite):
        self._capacite_max_m3 = nv_capacite
    
    @property
    def is_selected(self):
        return self._is_selected
    
    @is_selected.setter
    def is_selected(self, true_or_false):
        self._is_selected = true_or_false
    
    @property
    def volume_disponible_m3(self):
        return self._capacite_max_m3 - self._tas_dechets.volume_m3
        
    def __repr__(self):
        """
        Redéfinition de la méthode __repr__ d'affichage des attributs d'un objet ZoneDepot
        """
        return '< Quantité de déchets {} t = {} m3 ; Volume disponible : {} m3>'.format(self._tas_dechets.poids_tonnes, 
                              self._tas_dechets.volume_m3,
                              self.volume_disponible_m3)
