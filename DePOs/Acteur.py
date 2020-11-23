# -*- coding: utf-8 -*-
import pandas as pd

class Acteur:
    def __init__(self, nom):
        self._nom = nom
        #self._flotte_vehicules = pd.Series()
        self._nbVehicules = 3 
        self._capaciteMaxMoy = 32 # en m3
        self.duree_travail_journalier_h = 8
    
    @property
    def nom(self):
        return self._nom
    
    @property
    def horaires_travail(self):
        return self._horaires_travail
    
    @horaires_travail.setter
    def horaires_travail(self, horaires):
        self._horaires_travail = horaires
    
    @property
    def distance_max_jour_km(self):
        return self._distance_max_jour_km
    
    @distance_max_jour_km.setter
    def distance_max_jour_km(self, dist):
        self._distance_max_jour_km = dist
    
    @property
    def nbVehicules(self):
        return self._nbVehicules
    
    @nbVehicules.setter
    def nbVehicules(self, nb):
        self.nbVehicules = nb
    
    @property
    def capaciteMaxMoy(self):
        return self._capaciteMaxMoy
    
    @capaciteMaxMoy.setter   
    def capaciteMaxMoy(self, capa):
        self.capaciteMaxMoy = capa
    
    def __repr__(self):
        """
        Affiche les informations d'un acteur de collecte de déchet.

        Returns
        -------
        None.

        """
        info_display = '------------- Acteur --------------\n'
        info_display += '{}\n'.format(self._nom)
        info_display += 'Flotte : {} véhicules\n'.format(self.nb_vehicules)
        info_display += 'Capacité max. moyenne : {} m3\n'.format(self._flotte_vehicules[0].capacite_max_m3)
        '''
        if hasattr(self, 'horaires_travail'):
            info_display += 'Horaires de travail : {}h-{}h / {}h-{}h\n'.format(self.horaires_travail[0]
                                                                             ,self.horaires_travail[1]
                                                                             ,self.horaires_travail[2]
                                                                             ,self.horaires_travail[3])
                                                                             
        '''
        info_display += '----------------------------------'
        return info_display