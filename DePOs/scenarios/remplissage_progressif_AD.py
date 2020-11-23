from . import sc1
import Vehicule as v
import Chemins as c
import CollecteDechets as cd
import pandas as pd

class scenario3(sc1.scenario1):
    def __init__(self):
        super().__init__()
        self._periode_remplissage_semaine = 1

    @property
    def periode_remplissage_semaine(self):
        return self._periode_remplissage_semaine
    
    @periode_remplissage_semaine.setter
    def periode_remplissage_semaine(self, periode):
        self._periode_remplissage_semaine = periode
        
    def collecte_dechets_AD(self, camion = v.Vehicule):
    # def collecte_dechets_AD(self, camion = v.Vehicule, duree_chgt_h = 1.5, duree_dechgt_h =1.5):
        """
        Effectue la collecte des déchets des AD vers la ZST par un camion.
        Scénario où les AD se remplissent progressivement :
            - Période 1 : 1/2 du volume total de déchets
            - Période 2 : +1/4 du volume de déchets est apporté 
            - Période 3 : +1/4 du volume de déchets est apporté


        Parameters
        ----------
        camion : TYPE, optional
            DESCRIPTION. The default is v.Vehicule.
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
            vol_dechets_s1 = traj.destination.tas_dechets.volume_m3/2
            vol_dechets_s2_3 = traj.destination.tas_dechets.volume_m3/4
            
            # traj_s1 = deepcopy(traj)
            traj.destination.tas_dechets.volume_m3 = vol_dechets_s1
            
            print('ID aire de dépose : ' + str(traj.destination.idz))
            print('Volume de déchets à collecter semaine 1 : {} m3'
                  .format(vol_dechets_s1))
            print('Volume de déchets à collecter semaines 2 et 3 : {} m3'
                  .format(vol_dechets_s2_3))
            if hasattr(traj, 'distance_km'):
                print('Longueur de la trajectoire (km) : ' + str(traj.distance_km))
            elif hasattr(traj, 'duree_h'):
                print('Duree de la trajectoire (h) : ' + str(traj.duree_h))
        
            # Instanciation d'un trajet:
            nv_trajet = c.Trajet(traj, camion)
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
            # Collecter la zone de dépôt Semaine 1
            infos_collecte_s1 = cd.collecter_dechets_durant_periode(camion,
                                                                 traj,
                                                                 duree_chgt_h=self._duree_chgt_h,
                                                                 periode_semaine = self._periode_remplissage_semaine)
            
            # Nombre d'AR : intégré dans l'objet Trajet
            nv_trajet.nb_AR = infos_collecte_s1.loc['nb_ar']
            
            # Semaine 2 : de nouveaux déchets arrivent aux AD
            traj.destination.tas_dechets.volume_m3 += vol_dechets_s2_3
            # Collecter la zone de dépôt Semaine 2
            infos_collecte_s2 = cd.collecter_dechets_durant_periode(camion,
                                                                 traj,
                                                                 duree_chgt_h=self._duree_chgt_h)
            # Nombre d'AR : intégré dans l'objet Trajet
            nv_trajet.nb_AR += infos_collecte_s2.loc['nb_ar']
            
            # Semaine 3 : de nouveaux déchets arrivent aux AD
            traj.destination.tas_dechets.volume_m3 += vol_dechets_s2_3
            # Vider la zone de dépôt
            infos_collecte_s3 = cd.vider_zone_depot(camion,
                                                    traj,
                                                    duree_chgt_h=self._duree_chgt_h,
                                                    duree_dechgt_h=self._duree_dechgt_h)
            # Nombre d'AR : intégré dans l'objet Trajet
            nv_trajet.nb_AR += infos_collecte_s3.loc['nb_ar']
            
            
            col_nb_ar.append(nv_trajet.nb_AR)
            if hasattr(traj, 'distance_km'):
                # Longueur totale du trajet
                col_tot_dist_km.append(infos_collecte_s1.loc['dist_tot_km']+
                                       infos_collecte_s2.loc['dist_tot_km']+
                                       infos_collecte_s3.loc['dist_tot_km'])
                print('Longueur trajectoire : {} km'.format(nv_trajet.
                                                                trajectoire.
                                                                distance_km))
                print('Longueur du trajet : {} km'.format(nv_trajet.
                                                              total_distance_km))
            else:
                col_tot_dist_km.append(0)
            
            # Durée du trajet
            duree_totale = infos_collecte_s1.loc['duree_estimee_h'] + infos_collecte_s2.loc['duree_estimee_h'] + infos_collecte_s3.loc['duree_estimee_h']
            nv_trajet.duree_h = duree_totale
            col_duree_h.append(nv_trajet.duree_h)
            
            # Distance totale
            dist_totale = infos_collecte_s1.loc['dist_tot_km'] + infos_collecte_s2.loc['dist_tot_km'] + infos_collecte_s3.loc['dist_tot_km']
            
            # Affichage
            print('Durée du trajet : {} h'.format(nv_trajet.duree_h))
            print('---------------------------------------')
            print('Nombre d\'AR sur la trajectoire : {} ({} km)\n'
                  .format(nv_trajet.nb_AR, dist_totale))
                
            if hasattr(traj, 'distance_km'):
                count_total_dist += dist_totale
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