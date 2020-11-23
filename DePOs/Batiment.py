# -*- coding: utf-8 -*-
import Dechets
class Batiment :
    """
    Classe modélisant un bâtiment.
    
    Attributs
    --------
    surface_m2 : float
        Emprise du bâtiment en mètres carrés
    
    hauteur_m : float
        Hauteur du bâtiment en mètres
   
    nature : str
        Nature du bâtiment (ex : école, habitation, etc.)
    
    state_on_sept_2017 : str
        Etat du bâtiment après le passage d'Irma, en septembre 2017 (ex: détruit, fortement endommagé, etc.)
    

    dechets_estimes_sept_2017 : Dechets.TasDechets
        Quantité de déchet estimée en septembre 2017
    
    """
    def __init__(self, idBatiment = None, 
                 area = None, 
                 height = None, 
                 nature = None,
                 state_on_sept_2017 = None,
                 dechets_estimes_sept_2017  = Dechets.TasDechets) :
        
        self._idBatiment = idBatiment
        self._surface_m2 = area
        self._hauteur_m = height
        self._nature = nature
        self._etat_sept_2017 = state_on_sept_2017
        self._dechets_estimes_sept_2017 = dechets_estimes_sept_2017
    
    # getters
    @property
    def surface_m2(self):
        return self._surface_m2
    
    @property
    def hauteur_m(self):
        return self._hauteur_m
    
    @property
    def nature(self):
        return self._nature
    
    @property
    def etat_sept_2017(self):
        return self._etat_sept_2017
    
    @property
    def dechets_estimes_sept_2017(self):
        return self._dechets_estimes_sept_2017
        
  
        
    # setters
    @surface_m2.setter
    def surface_m2(self, area):
        self._surface_m2 = area
    
    @hauteur_m.setter
    def hauteur_m(self, height):
        self._hauteur_m = height
    
    @nature.setter
    def nature(self, nature):
        self._nature = nature
    
    @etat_sept_2017.setter
    def etat_sept_2017(self, state):
        self._etat_sept_2017 = state
    
    @dechets_estimes_sept_2017.setter
    def dechets_estimes_sept_2017(self, dechets):
        self._dechets_estimes_sept_2017 = dechets
        
   
        
        # Les méthodes suivantes permettent de quantifier le poids et le volume des déchets.
        # Elles prennent en compte la nature du bâtiment.
        # D'autres méthodes pourront être ajoutées ici.
    @property
    def estimation_dechets_california_m3(self) :
        """
        Estimation du volume de déchets par la méthode California. 
        Elle ne concerne que les bâtiments détruits

        Returns
        -------
        float
            Volume de déchets en mètres cubes.

        """
        if self._etat_sept_2017 == 'Détruit' :
            return self._surface_m2 * self._hauteur_m / 3
        else :
            return 0
    
    @property
    def estimation_dechets_california_tonnes(self) :
        """
        Estimation du poids de déchets par la méthode California. 
        Elle ne concerne que les bâtiments détruits

        Returns
        -------
        float
            Poids de déchets en tonnes.

        """
        
        # 1 tonne de déchets = 0,25 tonne de déchets
        return self.estimation_dechets_california_m3 / 4
    
    @property
    def estimation_dechets_michelet_m3(self) :
        """
        Estimation du volume de déchets par la formule proposée par Michelet durant son stage. 
        Cette méthode concerne les bâtiments détruits et fortement endommagés

        Returns
        -------
        float
            Volume en mètres cubes.

        """
        
        if self._etat_sept_2017 == 'Détruit' :
            return self._surface_m2 * 1.15
            
        elif self._etat_sept_2017 == 'Fortement endommagé' :
            return self._dechets_estimes_sept_2017_m3 * 0.5
            
        else :
            return 0
   
    @property
    def estimation_dechets_michelet_tonnes(self) :
        """
        Estimation du poids de déchets par la formule proposée par Michelet durant son stage. 
        Cette méthode concerne les bâtiments détruits et fortement endommagés

        Returns
        -------
        float
            Poids en tonnes.

        """
    # 1 tonne de déchets = 0,25 tonne de déchets
        return self.estimation_dechets_michelet_m3 / 4