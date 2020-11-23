from .ZoneDepot import ZoneDepot #AireDepose, ZoneStockageTemporaire, ZoneDepotFinal
from .Vehicule import Vehicule 
from .Chemins import Trajectoire, Trajet 
from .Dechets import Dechet, TasDechets 
from .Acteur import Acteur 
import csv
from .CollecteDechets import vider_zone_depot 
import pandas as pd


class scenario :
    """
    Scénario de collecte des déchets issus de plusieurs zones de déblayage
    (= bassin de collecte).
    """
    
    def __init__(self):
        self._ad = [] # Liste des Aires de dépose
        self._zst = [] # Liste des Zones de stockage temporaire
        self._exutoireFinal = [] # Liste des exutoires finaux
        self._acteurCollecte = [] # Liste des acteurs
        
        # Liste des bassins de collecte & les acteurs qui y sont affectés
        columnsBassin = ['idBassin', 'idActeur', 'nbVehicules', 'capa_moy_m3']
        self._bassinCollecte = pd.DataFrame(columns= columnsBassin) 
        
        # Liste des bassins & des ZST associées
        columnBassinZST = ['idBassin', 'idZST']
        self._bassinZST = pd.DataFrame(columns= columnBassinZST)
        
        # Liste des chemins AD->ZST
        columnsCheminsVersZST = ['idAD', 'idZST', 'cost', 'idBassin']
        self._chemin_AD_ZST = pd.DataFrame(columns=columnsCheminsVersZST)
        
        # Liste des chemins ZST->exutoires finaux
        columnsCheminsVersISDND = ['idZST', 'idISDND', 'cost']
        self._chemin_ZST_ISDND = pd.DataFrame(columns=columnsCheminsVersISDND)
        
        # Durées de chargement / déchargement : 1h30 par défaut
        self.duree_chgt_h = 1.5
        self.duree_dechgt_h = 1.5
        
    @property
    def ad(self):
        return self._ad
    
    @ad.setter
    def ad(self, ad):
        self._ad = ad
        
    def addZoneDepot(self, idZone, vol_dechet, typeZone = 0):
        """ Ajoute une zone de dépôt dans le scénario """
        tas = TasDechets(Dechet(volume_m3 = vol_dechet))
        zone = ZoneDepot()
        zone.idz = idZone
        zone.tasDechets = tas
        
        if typeZone == 0:
            self.ad.append(zone)
        elif typeZone == 1:
            self.zst.append(zone)
        elif typeZone == 2:
           self.exutoireFinal.append(zone)
        
    @property
    def zst(self):
        return self._zst
    
    @zst.setter
    def zst(self, zst):
        self._zst = zst

    @property
    def exutoireFinal(self):
        return self._exutoireFinal
    
    @exutoireFinal.setter
    def exutoireFinal(self, exutoireFinal):
        self._exutoireFinal = exutoireFinal
    
    @property
    def bassinCollecte(self):
        return self._bassinCollecte
    
    @bassinCollecte.setter
    def bassinCollecte(self, b):
        self.bassinCollecte = b
    
    @property
    def acteurCollecte(self):
        return self._acteurCollecte
    
    @acteurCollecte.setter
    def acteurCollecte(self, acteurCollecte):
        self.acteurCollecte = acteurCollecte
    
    def addActeur(self, acteur = Acteur):
        self.acteurCollecte.append(acteur)
    
    @property
    def chemin_AD_ZST(self):
        return self._chemin_AD_ZST
    @chemin_AD_ZST.setter
    def chemin_AD_ZST(self, data):
        self.chemin_AD_ZST = data
    
    @property
    def chemin_ZST_ISDND(self):
        return self._chemin_AD_ZST
    
    @chemin_ZST_ISDND.setter
    def chemin_ZST_ISDND(self, data):
        self.chemin_ZST_ISDND = data
    def resetCheminsVersZST(self):
        col = ['idAD', 'idZST', 'cost']
        self.chemin_AD_ZST = pd.DataFrame(columns=col)
    
    def resetCheminsVersISDND(self):
        col = ['idAD', 'idZST', 'cost']
        self.chemin_AD_ZST = pd.DataFrame(columns=col)
        
    
    def chargerTrajectoires(self, data, colId, colCost, circuit = 1, costType = 'distance'):
        """
            Charge les trajectoires des AD vers les ZST (circuit = 1)
            ou des ZST vers les ISDND (circuit = 2)
        """
        if circuit == 1:
            self.chargerCheminsVersZST(data, colId, colCost, costType)
            
        elif circuit == 2:
            self.chargerCheminsVersZST(data, colId, colCost, costType)
    
    def chargerCheminsVersZST(self, data, colId, colCost, costType = "distance"):
        """
            Charge les chemins vers les ZST
        """
        self.resetCheminsVersZST() # Data reset
    
    def chargerCheminsVersISDND(self, colId, colCost, costType = "distance"):
        """
            Charge les chemins vers les ISDND
        """
        self.resetCheminsVersISDND() # Data reset
    

    