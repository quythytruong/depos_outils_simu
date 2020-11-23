import ZoneDepot as zd
import Vehicule as v
import Chemins as c
import Dechets as d
import Acteur as a
import csv
import math
import CollecteDechets as cd
import pandas as pd

class scenario2:
    zst_la_savane = zd.ZoneStockageTemporaire()
    zst_la_savane.nom = 'Plateau sportif de La Savane'
    zst_la_savane.nature = 'Stade'
    zst_la_savane.capacite_max_m3 = 20000
    
    zst_esplanade = zd.ZoneStockageTemporaire()
    zst_esplanade.nom = 'L\'Esplanade'
    zst_esplanade.capacite_max_m3 = 20000
    
    # Instanciation de 3 camions
    charge_utile_t = 8
    capa_max_m3 = charge_utile_t * 4
    camion1 = v.Vehicule(1, charge_utile_t, capa_max_m3)
    camion2 = v.Vehicule(2, charge_utile_t, capa_max_m3)
    camion3 = v.Vehicule(3, charge_utile_t, capa_max_m3)
    flotte = [camion1, camion2, camion3]
    
    # Définition d'un acteur : Entreprise de déblai
    entreprise = a.Acteur('Entreprise de collecte de La Savane')
    entreprise.flotte_vehicules = pd.Series(flotte)
    entreprise.horaires_travail = [8,12,14,18]
    
    volume_total_dechet_ini = 0
    
    def charger_chemins(csv_path_file, type_chemin = 'court'):
        trajectoire_set = []
        with open(csv_path_file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # Instanciation des aires de dépose
                ad = zd.AireDepose()
                ad.idz = row["idz"]
                ad.tas_dechets = d.TasDechets(d.Dechet(None,
                                                           float(row["vol_dechet_m3"])))            
                scenario2.volume_total_dechet_ini += float(row["vol_dechet_m3"])
               
                # Instanciation de la trajectoire entre la ZST
                # et l'aire de dépose
                if type_chemin == 'court':
                    if float(row["dist_esplanade_m"]) < float(row["dist_plateau_sportif_m"]):
                        trajectoire = c.Trajectoire(scenario2.zst_esplanade, ad)
                        trajectoire.distance_km = float(row["dist_esplanade_m"])/1000
                    else:
                        trajectoire = c.Trajectoire(scenario2.zst_la_savane, ad)
                        trajectoire.distance_km = float(row["dist_plateau_sportif_m"])/1000
                    print('Trajectoire de longueur ' + 
                      str(trajectoire.distance_km) + ' km'+'\n')
                elif type_chemin == 'rapide':
                   pass
                trajectoire_set.append(trajectoire)
            
                line_count += 1

        print('Nombre de trajectoires : ' + str(len(trajectoire_set)))
        
        return trajectoire_set
    
    def collecte_par_camion1(trajectoire_set):        
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
        for traj in trajectoire_set:
            print('ID aire de dépose : ' + str(traj.destination.idz))
            print('Volume de déchets à collecter: {} m3'
                      .format(traj.destination.tas_dechets.volume_m3))
            if hasattr(traj, 'distance_km'):
                print('Longueur de la trajectoire (km) : ' + str(traj.distance_km))
            elif hasattr(traj, 'duree_h'):
                print('Duree de la trajectoire (h) : ' + str(traj.duree_h))
        
            # Instanciation d'un trajet:
            nv_trajet = c.Trajet(traj, scenario2.camion1)
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
            infos_collecte = cd.vider_zone_depot(scenario2.camion1,traj)
            # Nombre d'AR : intégré dans l'objet Trajet
            nv_trajet.nb_AR = infos_collecte.loc['nb_ar']
            print('Nombre d\'AR : {}'.format(nv_trajet.nb_AR))
            col_nb_ar.append(nv_trajet.nb_AR)
            if hasattr(traj, 'distance_km'):
                # Longueur totale du trajet
                col_tot_dist_km.append(infos_collecte.loc['dist_tot_km'])
                print('Longueur trajectoire : {} km'.format(nv_trajet.trajectoire.distance_km))
                print('Longueur du trajet : {} km'.format(nv_trajet.total_distance_km))
            else:
                col_tot_dist_km.append(0)
            # Durée du trajet
            nv_trajet.duree_h = infos_collecte.loc['duree_estimee_h']
            col_duree_h.append(infos_collecte.loc['duree_estimee_h'])
            # Affichage
            print('Durée du trajet : {} h'.format(nv_trajet.duree_h))
            print('---------------------------------------')
            print('Nombre d\'AR sur la trajectoire : {} ({} km)'
                  .format(nv_trajet.nb_AR, infos_collecte.loc['dist_tot_km']))
            
            if hasattr(traj, 'distance_km'):
                count_total_dist += infos_collecte.loc['dist_tot_km']
                count_total_ar += nv_trajet.nb_AR
                print('Cumul des d\'AR effectués : {} \n Total km parcourus : {} km '.
                  format(count_total_ar, count_total_dist) + '\n')
                                              
                                              
        df_par_camion = pd.DataFrame(list(zip(col_id_AD, 
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
        # TODO: on redispatche les trajets aux autres camions
        # de manière à homogénéiser la durée de collecte
        # affectation_camion_trajectoires = {}
        return df_par_camion