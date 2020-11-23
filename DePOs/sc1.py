from .ZoneDepot import AireDepose, ZoneStockageTemporaire
from .Vehicule import Vehicule 
from .Chemins import Trajectoire, Trajet 
from .Dechets import Dechet, TasDechets 
from .Acteur import Acteur 
import csv
from .CollecteDechets import vider_zone_depot 
import pandas as pd

class scenario1 :
    """
    Scénario n° 1 :
        - Les déchets des AD sont acheminés vers une seule ZST
    """
    
    def __init__(self):
        self._zst = ZoneStockageTemporaire()
        self._zst.capacite_max_m3 = 2000000 # Par défaut
        
        self._duree_chgt_h = 1.5
        self._duree_dechgt_h = 1.5

        self._trajectoires_set = []
        self._volume_total_dechets_ini = 0
        
        self._suivi_collecte_AD = pd.DataFrame()
    
    @property
    def zst(self):
        return self._zst
    
    @zst.setter
    def zst(self, zst):
        self._zst = zst
    
    @property
    def trajectoires_set(self):
        return self._trajectoires_set
    
    @trajectoires_set.setter
    def trajectoires_set(self, trajectoires):
        self._trajectoires_set = trajectoires
    
    @property
    def volume_total_dechets_ini(self):
        return self._volume_total_dechets_ini
    
    @volume_total_dechets_ini.setter
    def volume_total_dechets_ini(self, volume):
        self._volume_total_dechets_ini = volume
    
    @property
    def suivi_collecte_AD(self):
        return self._suivi_collecte_AD
    
    @suivi_collecte_AD.setter
    def suivi_collecte_AD(self, df_suivi):
        self._suivi_collecte_AD = df_suivi
    
    @property
    def acteur(self):
        return self._acteur
    
    @acteur.setter
    def acteur(self, acteur = Acteur):
        self._acteur = acteur
    
    @property
    def duree_chgt_h(self):
        return self._duree_chgt_h
    
    @duree_chgt_h.setter
    def duree_chgt_h(self, duree):
        self._duree_chgt_h = duree
    
    @property
    def duree_dechgt_h(self):
        return self._duree_dechgt_h
    
    @duree_dechgt_h.setter
    def duree_dechgt_h(self, duree):
        self._duree_dechgt_h = duree
        
    def charger_trajectoires(self, csv_path_file, type_chemin = 'court'):
        """
        Charge les trajectoires entre AD et ZST. Les trajectoires sont 
        instanciées et stockées dans l'attribut trajectoires_set 

        Parameters
        ----------
        csv_path_file : TYPE
            DESCRIPTION.
        type_chemin : TYPE, optional
            DESCRIPTION. The default is 'court'.

        Returns
        -------
        None.

        """
        with open(csv_path_file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                # Instanciation des aires de dépose
                ad = AireDepose()
                ad.idz = row["id_0"]
                ad.tas_dechets = TasDechets(Dechet(None,
                                                           float(row["vol_dechet_m3"])))            
                self.volume_total_dechets_ini += float(row["vol_dechet_m3"])
               
                # Instanciation de la trajectoire entre la ZST
                # et l'aire de dépose
                trajectoire = Trajectoire(self.zst, ad)
                if type_chemin == 'court': # Chemin le plus court
                    # Le champs 'cost' indique une distance en mètres
                    trajectoire.distance_km = float(row["cost"])/1000
                    print('Trajectoire de longueur ' + 
                      str(trajectoire.distance_km) + ' km'+'\n')
                    
                elif type_chemin == 'rapide': # Chemin le plus rapide
                    # Le champs 'cost' indique une durée en heures
                    trajectoire.duree_h = float(row["cost"])
                    print('Trajectoire de durée ' + 
                      str(trajectoire.duree_h) + ' h'+'\n')
                    
                self.trajectoires_set.append(trajectoire)
        print('Nombre de trajectoires chargées : ' + str(len(self.trajectoires_set)))
        
        
    def collecte_dechets_AD(self, camion = Vehicule):
        """
        Effectue la collecte des déchets des AD vers la ZST par un camion


        Parameters
        ----------
        camion : TYPE, optional
            DESCRIPTION. The default is Vehicule.
        duree_chgt_h : float, optional
            Durée de chargement / déchargement du véhicule (en heures). 
            The default is 1.5 (1h30).

        Returns
        -------
        df_suivi : pandas.DataFrame
            Indicateurs de suivi de la collecte des aires de dépose : 
                - idz : Identifiant de l'AD
                - vol_dechets_m3 : Volume initial de déchets à l'AD
                - trajet : Trajet effectué
                - dist_AD-ZST_km : Distance de la trajectoire AD-ZST (km)
                - nb_AR : Nombre d'allers-retours effectués sur la trajectoire
                - dist_tot_km : Distance totale effectuée pour vider l'AD (km)
                - duree_estimee_h : Temps estimé pour vider l'AD (h)

        """

        count_total_dist = 0
        count_total_ar = 0
        # On définit les futures colonnes du dataframe de suivi
        col_id_AD = [] # Identifiants des AD
        col_vol_dechet = [] # volume de déchets des AD
        col_nb_ar = [] # Nombre d'allers retours nécessaires pour vider les AD
        col_dist_km = [] # Distance en km de la trajectoire AD-ZST
        col_tot_dist_km = [] # Distance totale en km effectuée pour vider les AD
        col_duree_h = [] # Durée (en heures) pour vider les AD
        col_trajet = [] # Trajet
        
        # Collecte puis affectation aux camions
        # La collecte est effectuée par un des camions de la flotte (camion1)
        for traj in self.trajectoires_set:

            print('ID aire de dépose : ' + str(traj.destination.idz))
            print('Volume de déchets à collecter: {} m3'
                  .format(traj.destination.tas_dechets.volume_m3))
            if hasattr(traj, 'distance_km'):
                print('Longueur de la trajectoire (km) : ' + str(traj.distance_km))
            elif hasattr(traj, 'duree_h'):
                print('Duree de la trajectoire (h) : ' + str(traj.duree_h))
            
            # Instanciation d'un trajet:
            nv_trajet = Trajet(traj, camion)
            col_trajet.append(nv_trajet) 
            # Remplissage de quelques colonnes :
            col_id_AD.append(traj.destination.idz)
            col_vol_dechet.append(traj.destination.tas_dechets.volume_m3)
            if hasattr(traj, 'distance_km'):
                col_dist_km.append(traj.distance_km)
            else:
                col_dist_km.append(0)
                print('Volume de déchets à l\'AD : {} m3'.format(traj.
                                                                 destination.
                                                                 tas_dechets.
                                                                 volume_m3))
            # Vider la zone de dépôt
            infos_collecte = vider_zone_depot(camion, traj, 
                                                 duree_chgt_h=self._duree_chgt_h,
                                                 duree_dechgt_h=self._duree_dechgt_h)
            # Nombre d'AR : intégré dans l'objet Trajet
            nv_trajet.nb_AR = infos_collecte.loc['nb_ar']

            col_nb_ar.append(nv_trajet.nb_AR)
            if hasattr(traj, 'distance_km'):
                # Longueur totale du trajet
                col_tot_dist_km.append(infos_collecte.loc['dist_tot_km'])
                print('Longueur trajectoire : {} km'.format(nv_trajet.
                                                                trajectoire.
                                                                distance_km))
                print('Longueur du trajet : {} km'.format(nv_trajet.
                                                              total_distance_km))
            else:
                col_tot_dist_km.append(0)
            # Durée du trajet
            nv_trajet.duree_h = infos_collecte.loc['duree_estimee_h']
            col_duree_h.append(infos_collecte.loc['duree_estimee_h'])
            # Affichage
            print('Durée du trajet : {} h'.format(nv_trajet.duree_h))
            print('---------------------------------------')
            print('Nombre d\'AR sur la trajectoire : {} ({} km)\n'
                  .format(nv_trajet.nb_AR, 
                          infos_collecte.loc['dist_tot_km']))
                
            if hasattr(traj, 'distance_km'):
                count_total_dist += infos_collecte.loc['dist_tot_km']
                count_total_ar += nv_trajet.nb_AR
                print('Cumul des d\'AR effectués : {} \n Total km parcourus : {} km '.
                      format(count_total_ar, count_total_dist) + '\n')
                                       
        print(len(col_id_AD))
        print(len(col_vol_dechet))
        print(len(col_trajet))
        print(len(col_dist_km))
        print(len(col_nb_ar))
        print(len(col_tot_dist_km))
        print(len(col_duree_h))
        
        df_suivi = pd.DataFrame(list(zip(col_id_AD, 
                                         col_vol_dechet,
                                         col_trajet,
                                         col_dist_km,
                                         col_nb_ar,
                                         col_tot_dist_km,
                                         col_duree_h)),
                                columns =['idz', 'vol_dechets_m3',
                                          'trajet',
                                          'dist_AD-ZST_km',
                                          'nb_AR',
                                          'dist_tot_km',
                                          'duree_estimee_h'])
        self._suivi_collecte_AD = df_suivi
        return df_suivi

    def conservation_volume_AD_ZST(self):
        print('Déchets AD : {} m3'.format(self.volume_total_dechets_ini))
        print('Déchets ZST : {} m3'.format(self.zst.tas_dechets.volume_m3))
        return self.zst.tas_dechets.volume_m3 == self.volume_total_dechets_ini

    def duree_collecte_AD(self):
        """
        Calcule des durées de collecte des AD vers les ZST:
            - Duréee totale en heures
            - Durée en heures par camion
            - Nombre de jours travaillés par camion

        Returns
        -------
        sr_duree_collecte : pandas.Series
            DESCRIPTION.
            
        """
        duree_tot_h = self._suivi_collecte_AD['duree_estimee_h'].sum(axis=0)
        duree_par_camion_h = duree_tot_h / len(self.acteur.flotte_vehicules)
        
        # Nombre de jours travaillés 
        count_jours = duree_par_camion_h // self.acteur.duree_travail_journalier_h
        reste = duree_par_camion_h % self.acteur.duree_travail_journalier_h
        if reste > self.acteur.duree_travail_journalier_h/2:
            count_jours += 1
        else:
            count_jours += 0.5
            
        print('--- Durée de la collecte des AD ---')
        print('Durée totale : {} h'.format(duree_tot_h))
        print('Durée par camion : {} h'.format(duree_par_camion_h))
        print('Jour(s) travaillé(s) par camion : {}'.format(count_jours))
        
        sr_duree_collecte = pd.Series([duree_tot_h, 
                                       duree_par_camion_h, 
                                       count_jours ]) 
        sr_duree_collecte.index = ['duree_tot_h', 
                                   'duree_h_par_camion', 
                                   'jours_travailles']
        return sr_duree_collecte

class scenario2(scenario1):
    def __init__(self):
        super().__init__()
        # On ajoute une zst
        self._zst1 = ZoneStockageTemporaire()
        self._zst1.capacite_max_m3 = 20000 # Par défaut
    
    @property
    def zst1(self):
        return self._zst1
    
    @zst1.setter
    def zst1(self, zst):
        self._zst1 = zst
    
    
    def charger_trajectoires(self, csv_path_file, type_chemin = 'court'):
        with open(csv_path_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip header
            for row in csv_reader:
                # Instanciation des aires de dépose
                ad = AireDepose()
                ad.idz = row[0]
                ad.tas_dechets = TasDechets(Dechet(None,
                                                           float(row[1])))            
                self.volume_total_dechets_ini += float(row[1])
               
                # Instanciation de la trajectoire entre la ZST
                # et l'aire de dépose
                print(row[2])
                print(row[3])
                if float(row[2]) < float(row[3]):
                    trajectoire = Trajectoire(self.zst, ad)
                    cost = float(row[2])
                else:
                    trajectoire = Trajectoire(self.zst1, ad)
                    cost = float(row[3])
                    
                if type_chemin == 'court': # Chemin le plus court
                    # Le champs 'cost' indique une distance en mètres
                    trajectoire.distance_km = cost/1000
                    print('Trajectoire de longueur ' + 
                      str(trajectoire.distance_km) + ' km'+'\n')
                    
                elif type_chemin == 'rapide': # Chemin le plus rapide
                    # Le champs 'cost' indique une durée en heures
                    trajectoire.duree_h = cost
                    print('Trajectoire de durée ' + 
                      str(trajectoire.duree_h) + ' h'+'\n')
                    
                self.trajectoires_set.append(trajectoire)
        print('Nombre de trajectoires chargées : ' + str(len(self.trajectoires_set)))
        
    def conservation_volume_AD_ZST(self):
        print('Déchets AD : {} m3'.format(self.volume_total_dechets_ini))
        print('Déchets ZST {} : {} m3'.format(self.zst.nom,
                                              self.zst.tas_dechets.volume_m3))
        print('Déchets ZST {} : {} m3'.format(self.zst1.nom,
                                              self.zst1.tas_dechets.volume_m3))
        total_dechets_zst = self.zst.tas_dechets.volume_m3 + self.zst1.tas_dechets.volume_m3
        print('Déchets ZST : {} m3'.format(total_dechets_zst))
        return self.zst.tas_dechets.volume_m3+self.zst1.tas_dechets.volume_m3 == self.volume_total_dechets_ini
