from .ZoneDepot import ZoneDepot #as zd
from .Vehicule import Vehicule #as v

class Trajectoire:
    def __init__(self, origine = ZoneDepot, destination = ZoneDepot):
        self._origine = origine
        self._destination = destination
    
    @property
    def origine(self):
        return self._origine
    
    @origine.setter
    def origine(self, origine):
        self._origine = origine
    
    @property
    def destination(self):
        return self._destination
    
    @destination.setter
    def destination(self, destination):
        self._destination = destination
    
    @property
    def distance_km(self):
        return self._distance_km
    
    @distance_km.setter
    def distance_km(self, dist_km):
        self._distance_km = dist_km
    
    @property
    def duree_h(self):
        return self._duree_h
    
    @duree_h.setter
    def duree_h(self, duree):
        self._duree_h = duree

class Trajet:
    def __init__(self, trajectoire = Trajectoire, vehicule = Vehicule):
        self._trajectoire = trajectoire
        self._vehicule = vehicule
        self._dechets_transportes = vehicule.tas_dechets_charges
        self._nb_AR = 0
        self._total_distance_km = 0
        # Attributs servant à calculer la durée du chargement
        self._type_duree = 'lineaire'
        self._seuil_vmin = 0
        self._seuil_vmax = 32
        self._seuil_duree_min = 0
        self._seuil_duree_max = 3
        self._pente_h_par_m3 = 0.5/30 # La durée du chargement augmente de 30 min tous les 30m3
        
    def __repr__(self):
        info = 'Informations trajet :\n'
        if hasattr(self.trajectoire.origine, 'idz'):
            info += 'Origine ID : {}\n'.format(self.trajectoire.origine.idz)
        elif hasattr(self.trajectoire.origine, 'nom'):
            info += 'Origine : {}\n'.format(self.trajectoire.origine.nom)
            
        if hasattr(self.trajectoire.destination, 'idz'):
                   info += 'Destination ID : {}\n'.format(self.trajectoire.destination.idz)
        
        if hasattr(self.trajectoire, 'distance_km'):
            info += 'Distance trajectoire : {} km \n'.format(self.trajectoire.distance_km)
        
        if hasattr(self, 'nb_AR'):
            info += 'Nombre allers-retours : {} \n'.format(self._nb_AR)
            info += 'Distance totale : {} km \n'.format(self.total_distance_km)
        
        if hasattr(self, 'duree_h'):
            info += 'Durée trajet : {} h \n'.format(self._duree_h)
        
        return info
        
    @property
    def trajectoire(self):
        return self._trajectoire
    
    @trajectoire.setter
    def trajectoire(self, traj):
        self._trajectoire = traj
        
    @property
    def date_depart(self):
        return self._date_depart
    
    @date_depart.setter
    def date_depart(self, date_depart):
        self._date_depart = date_depart
        
    @property
    def date_arrivee(self):
        return self._date_arrivee
    
    @date_arrivee.setter
    def date_arrivee(self, date_arrivee):
        self._date_arrivee = date_arrivee
        
    @property
    def duree_h(self):
        return self._duree_h
    
    @duree_h.setter
    def duree_h(self, d):
        self._duree_h = d
        
    @property
    def duree_min(self):
        return self._duree_min
    
    @duree_min.setter
    def duree_min(self, d):
        self._duree_min = d
    
    @property
    def nb_AR(self):
        return self._nb_AR
    
    @nb_AR.setter
    def nb_AR(self, ar):
        self._nb_AR = ar
        # Met à jour automatiquement la distance totale du trajet
        if hasattr(self.trajectoire, 'distance_km'):    
            self.total_distance_km = ar * 2 * self.trajectoire.distance_km
        
    @property
    def total_distance_km(self):
        return self._total_distance_km
    
    @total_distance_km.setter
    def total_distance_km(self, distance):
        self._total_distance_km = distance
    
    @property
    def cout_euros(self):
        pass
    
    @property
    def cout_CO2(self):
        pass