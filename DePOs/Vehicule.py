# -*- coding: utf-8 -*-
from .Dechets import Dechet, TasDechets #as d
import pandas as pd

class Vehicule:
    """
    Classe modélisant un véhicule de collecte de déchets
    
    """
    
    def __init__(self, idVehicule, 
                 charge_utile_tonnes = None,
                 capacite_max = None,
                 *args):
        
        self._idVehicule = idVehicule
        self._charge_utile_tonnes = charge_utile_tonnes
        self._capacite_max_m3 = capacite_max
        self._tas_dechets_charges = TasDechets(Dechet(0))
        
        # TODO : Initialiser les dataframes avec des colonnes prédéfinies
        self._suivi_trajets = pd.DataFrame()
        self._suivi_chargement = pd.DataFrame()
        self._suivi_facturation = pd.DataFrame()
        
        
    def __repr__(self):
        """
        Redéfinition de la méthode __repr__ d'affichage des attributs d'un objet Véhicule
        """
        return 'Véhicule ID {}: Charge utile : {} t - Capacité maximale : {} m3 - Volume chargé : {} m3 - Volume disponible : {} m3'.format(self._idVehicule, 
                              self._charge_utile_tonnes, 
                              self._capacite_max_m3,
                              self._tas_dechets_charges.volume_m3,
                              self.volume_disponible)
    
    # getters & setters
    @property
    def idVehicule(self):
        return self._idVehicule
    
    @property
    def charge_utile_tonnes(self):
        return self._charge_utile_tonnes
    
    @charge_utile_tonnes.setter
    def charge_utile_tonnes(self, nouvelle_charge):
        self._charge_utile_tonnes = nouvelle_charge
        self._capacite_max_m3 = 4 * nouvelle_charge
    
    @property
    def capacite_max_m3(self):
        return self._capacite_max_m3
    
    @capacite_max_m3.setter
    def capacite_max_m3(self, nouvelle_capacite):
        self._capacite_max_m3 = nouvelle_capacite
        self._charge_utile_tonnes = nouvelle_capacite / 4
    
    @property
    def tas_dechets_charges(self):
        return self._tas_dechets_charges
    
    @tas_dechets_charges.setter
    def tas_dechets_charges(self, tas_dechets):
        self._tas_dechets_charges = tas_dechets
    
    @property
    def poids_dechets_charges(self):
        return self._tas_dechets_charges.poids_tonnes
    
    @property
    def volume_dechets_charges(self):
        return self._tas_dechets_charges.volume_m3
    
    @property
    def volume_disponible(self):
        return self._capacite_max_m3 - self.volume_dechets_charges
    
    def vider_vehicule(self):
        """
        Vide entièrement le véhicule des déchets qu'il transporte.
        La méthode renvoie le volume (m3) de déchets déchargés.
        
        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        volume_dechargement = self.volume_dechets_charges
        self._tas_dechets_charges.dechets.volume_m3 = 0
        
        return volume_dechargement