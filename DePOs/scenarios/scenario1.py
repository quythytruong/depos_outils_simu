# Instanciation de la zone de stockage temporaire de La Savane
import ZoneDepot as zd
import Vehicule as v
import Chemins as c
import Dechets as d
import Acteur as a
import csv
import math
import CollecteDechets as cd
import pandas as pd

class scenario1:
    
    # Instanciation de la zone de stockage temporaire de La Savane
    # de capacité max = 14000 m3
    zst_la_savane = zd.ZoneStockageTemporaire()
    zst_la_savane.nom = 'Plateau sportif de La Savane'
    zst_la_savane.nature = 'Stade'
    zst_la_savane.capacite_max_m3 = 14000

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
                ad.idz = row["id_0"]
                ad.tas_dechets = d.TasDechets(d.Dechet(None,
                                                           float(row["vol_dechet_m3"])))            
                scenario1.volume_total_dechet_ini += float(row["vol_dechet_m3"])
               
                # Instanciation de la trajectoire entre la ZST
                # et l'aire de dépose
                trajectoire = c.Trajectoire(scenario1.zst_la_savane, ad)
                if type_chemin == 'court':
                    trajectoire.distance_km = float(row["cost"])/1000
                    print('Trajectoire de longueur ' + 
                      str(trajectoire.distance_km) + ' km'+'\n')
                elif type_chemin == 'rapide':
                    trajectoire.duree_h = float(row["cost"])
                    print('Trajectoire de durée ' + 
                      str(trajectoire.duree_h) + ' h'+'\n')
                trajectoire_set.append(trajectoire)
            
                line_count += 1

        print('Nombre de trajectoires : ' + str(len(trajectoire_set)))
        return trajectoire_set
        
    def trajectoires_chemins_les_plus_courts(csv_path_file):
        """
        Lecture du fichier CSV contenant les données
        des chemins les plus courts entre ZST & AD:
            Les longueurs (en km) sont renseignées pour chaque trajectoire
        

        Parameters
        ----------
        csv_path_file : TYPE
            DESCRIPTION.

        Returns
        -------
        Une liste des trajectoires entre ZST et AD.

        """
        ad_set = []
        trajectoire_set = []
        
        with open(csv_path_file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # Instanciation des aires de dépose
                ad = zd.AireDepose()
                ad.idz = row["id_0"]
                ad.tas_dechets = d.TasDechets(d.Dechet(None,
                                                           float(row["vol_dechet_m3"])))            
                scenario1.volume_total_dechet_ini += float(row["vol_dechet_m3"])
                print(ad)
                ad_set.append(ad)
            
                # Instanciation de la trajectoire entre la ZST
                # et l'aire de dépose
                trajectoire = c.Trajectoire(scenario1.zst_la_savane, ad)
                trajectoire.distance_km = float(row["cost"])/1000
                print('Trajectoire de longueur ' + 
                      str(trajectoire.distance_km) + ' km'+'\n')
                trajectoire_set.append(trajectoire)
            
                line_count += 1

        print('Nombre d\'aires de dépose : ' + str(len(ad_set)))
        print('Nombre de trajectoires : ' + str(len(trajectoire_set)))
        
        return ad_set, trajectoire_set
    
    def affectation_camion_aleatoire(ad_set, trajectoire_set):
        """
        Pour chaque camion: 
            affectation des trajectoires à effectuer vers les AD.
        L'affectation se fait de manière homogène en termes de nombre de 
        trajectoires à effectuer (= nombre d'AD à collecter) par camion.

        Parameters
        ----------
        trajectoire_set : list
            Liste des trajectoires ZST-AD

        Returns
        -------
        Un dictionnaire de clé/valeur où :
            - les clés sont les camions (type Vehicule)
            - les valeurs sont des listes des trajectoires associées 
                aux camions
        """
        
        affectation_camion_trajectoires = {}

        index_dernier_camion = len(scenario1.flotte) -1
        nb_ad_par_camion = math.floor(len(ad_set)/3)

        camion_count = 0
        index_chemin_ini = 0
        index_chemin_fin = nb_ad_par_camion
        for camion in scenario1.flotte:
            if camion_count != index_dernier_camion:
                print('Trajectoire n°{}-{}'.format(index_chemin_ini, 
                                                   index_chemin_fin-1))
                affectation_camion_trajectoires[camion] = trajectoire_set[index_chemin_ini:
                                                                  index_chemin_fin]
                print('Nombre de camions affecté à camion' 
                      + str(camion.idVehicule) + ': '
                      + str(len(affectation_camion_trajectoires[camion])))
                print('\n')
                
                index_chemin_ini = index_chemin_fin
                index_chemin_fin += nb_ad_par_camion
                camion_count += 1
    
            else : # Le dernier camion prend toutes les aires de dépose restantes
                affectation_camion_trajectoires[camion] =  trajectoire_set[index_chemin_ini :
                                                                   len(trajectoire_set)]
            
        print('Trajectoire n°{}-{}'.format(index_chemin_ini, 
                                           len(trajectoire_set)-1))
        print('Nombre de camions affecté à camion' 
              + str(camion.idVehicule) + ': ' 
              + str(len(affectation_camion_trajectoires[camion])) + '\n')
        
        return affectation_camion_trajectoires
    
    
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
            nv_trajet = c.Trajet(traj, scenario1.camion1)
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
            infos_collecte = cd.vider_zone_depot(scenario1.camion1,traj)
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
    
    def collecte_via_chemins_les_plus_courts(affectation_camion_trajectoires):
        suivi_collecte_camions= {}
        for camion, trajectoires in affectation_camion_trajectoires.items():
            print('-------------------------------------')
            print('camion' + str(camion.idVehicule))
            print('Nb trajectoires :'+ str(len(trajectoires)))
            # On définit les futures colonnes du dataframe de suivi
            col_id_AD = [] # Identifiants des AD
            col_vol_dechet = [] # volume de déchets des AD
            col_nb_ar = [] # Nombre d'allers retours nécessaires pour vider les AD
            col_dist_km = [] # Distance en km de la trajectoire AD-ZST
            col_tot_dist_km = [] # Distance totale en km effectuée pour vider les AD
            col_duree_h = [] # Durée (en heures) pour vider les AD
            col_trajet = [] # Trajet 
            
            count_total_dist = 0
            count_total_ar = 0
            
            for traj in trajectoires :
                print('ID aire de dépose : ' + str(traj.destination.idz))
                print('Volume de déchets à collecter: {} m3'
                      .format(traj.destination.tas_dechets.volume_m3))
                print('Longueur de la trajectoire (km) : ' + str(traj.distance_km))
                # Instanciation d'un trajet:
                nv_trajet = c.Trajet(traj, camion)
                
                col_id_AD.append(traj.destination.idz)
                col_vol_dechet.append(traj.destination.tas_dechets.volume_m3)
                col_dist_km.append(traj.distance_km)
                
                count_ar = 0
                count_dist = 0
                print('Volume de déchets à l\'AD : {} m3'.format(traj.
                                                              destination.
                                                              tas_dechets.
                                                              volume_m3))
                while traj.destination.tas_dechets.volume_m3 != 0 :
                    # Le véhicule effectue un aller
                    count_total_dist += traj.distance_km
                    count_dist += traj.distance_km
                    cd.chargement(camion, traj.destination)
            
                    # Le véhicule effectue un retour
                    count_total_dist += traj.distance_km
                    count_dist += traj.distance_km
                    cd.dechargement(camion, traj.origine)
            
                    count_ar += 1
                    count_total_ar += 1
                    
                # Nombre d'AR : intégré dans l'objet Trajet
                nv_trajet.nb_AR = count_ar
                #nv_trajet.total_distance_km = count_dist
                print('Nombre d\'AR : {}'.format(nv_trajet.nb_AR))
                col_nb_ar.append(count_ar)
                
                # Longueur totale du trajet
                col_tot_dist_km.append(count_total_dist)
                
                print('Longueur trajectoire : {} km'.format(nv_trajet.
                                                            trajectoire.
                                                            distance_km))
                print('Longueur du trajet : {} km'.format(nv_trajet.
                                                          total_distance_km))
                
                # Estimation de la durée
                # Hypothèse : le véhicule roule à 30 km/h
                # v = d/t => t = d/v
                duree_trajet = count_dist/30
                col_duree_h.append(duree_trajet)
                
                nv_trajet.duree_h = duree_trajet
                col_trajet.append(nv_trajet)       
       
                print('Durée du trajet : {} h'.format(nv_trajet.duree_h))
                print('---------------------------------------')
                print('Nombre d\'AR sur la trajectoire : {} ({} km)'
                  .format(count_ar, count_dist))
                print('Cumul des d\'AR effectués : {} \n Total km parcourus : {} km '.
                  format(count_total_ar, count_total_dist) + '\n')
            
            
            # Calling DataFrame constructor after zipping
            # both lists, with columns specified
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
            suivi_collecte_camions[camion.idVehicule] = df_par_camion
            
            # Volume de déchets présents sur le Plateau de la Savane 
            # à la fin de la collecte
        print('ZST de La Savane :\n {}'.format(scenario1.zst_la_savane))
        print('Volume total de déchets dans les AD : ' 
                  + str(scenario1.volume_total_dechet_ini))
        print('===> Conservation des volumes : ' 
                  + str(scenario1.zst_la_savane.tas_dechets.volume_m3 
                        == scenario1.volume_total_dechet_ini))
        # suivi_collecte_camions_concat = pd.concat(suivi_collecte_camions,
        #                                   keys = [1 , 2, 3])
        camion_keys = []
        for camion in scenario1.flotte:
            camion_keys.append(camion.idVehicule)
        suivi_collecte_camions_concat = pd.concat(suivi_collecte_camions,
                                          keys = camion_keys)
        return suivi_collecte_camions_concat
            
    def histogramme_duree_h(suivi_collecte_camions_concat):
        ax = suivi_collecte_camions_concat.hist(column='duree_estimee_h', 
                   bins=50, 
                   grid=False, 
                   figsize=(8,10), 
                   layout=(3,1), 
                   sharex=True, 
                   color='#86bf91', 
                   zorder=2, 
                   rwidth=0.9)

        ax = ax[0]
        for x in ax:
        
            # Despine
            x.spines['right'].set_visible(False)
            x.spines['top'].set_visible(False)
            x.spines['left'].set_visible(False)
        
            # Switch off ticks
            x.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
            
            
            # Draw horizontal axis lines
            vals = x.get_yticks()
            for tick in vals:
                x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        
            # Remove title
            x.set_title("")
        
            # Set x-axis label
            x.set_xlabel("Durée estimée (heures)", labelpad=20, weight='bold', size=12)
        
            # Set y-axis label
            x.set_ylabel("Nombre de trajets", labelpad=20, weight='bold', size=12)
        
    def trajectoires_chemins_les_plus_rapides(csv_path_file):
        """
        Lecture du fichier CSV contenant les données
        des chemins les plus rapides entre ZST & AD.
        La colonne "cost" renseigne sur la durée estimée (en heures) pour
        effectuer une trajectoire.

        Parameters
        ----------
        csv_path_file : TYPE
            DESCRIPTION.

        Returns
        -------
        ad_set : TYPE
            DESCRIPTION.
        trajectoire_set : TYPE
            DESCRIPTION.

        """
        ad_set = []
        trajectoire_set = []
        with open(csv_path_file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # Instanciation des aires de dépose
                ad = zd.AireDepose()
                ad.idz = row["id_0"]
                ad.tas_dechets = d.TasDechets(d.Dechet(None,
                                                       float(row["vol_dechet_m3"])))            
                scenario1.volume_total_dechet_ini += float(row["vol_dechet_m3"])
                print(ad)
                ad_set.append(ad)
        
                # Instanciation de la trajectoire entre la ZST
                # et l'aire de dépose
                trajectoire = c.Trajectoire(scenario1.zst_la_savane, ad)
                trajectoire.duree_h = float(row["cost"])
                print('Trajectoire de durée ' + 
                      str(trajectoire.duree_h) + ' h'+'\n')
                trajectoire_set.append(trajectoire)
                line_count += 1
        print('Nombre d\'aires de dépose : ' + str(len(ad_set)))
        print('Nombre de trajectoires : ' + str(len(trajectoire_set)))
        return ad_set, trajectoire_set
    
    def collecte_via_chemins_les_plus_rapides(affectation_camion_trajectoires):
        suivi_collecte_camions= {}
        for camion, trajectoires in affectation_camion_trajectoires.items():
            print('-------------------------------------')
            print('camion' + str(camion.idVehicule))
            print('Nb trajectoires :'+ str(len(trajectoires)))
            # On définit les futures colonnes du dataframe de suivi
            col_id_AD = [] # Identifiants des AD
            col_vol_dechet = [] # volume de déchets des AD
            col_nb_ar = [] # Nombre d'allers retours nécessaires pour vider les AD
            col_duree_h = [] # Durée (en heures) pour vider les AD
            col_trajet = [] # Trajet 

            count_total_ar = 0
            
            for traj in trajectoires :
                print('ID aire de dépose : ' + str(traj.destination.idz))
                print('Volume de déchets à collecter: {} m3'
                      .format(traj.destination.tas_dechets.volume_m3))
                print('Durée de la trajectoire (h) : ' + str(traj.duree_h))
                # Instanciation d'un trajet:
                nv_trajet = c.Trajet(traj, camion)                
                col_id_AD.append(traj.destination.idz)
                col_vol_dechet.append(traj.destination.tas_dechets.volume_m3)                
                count_ar = 0
                print('Volume de déchets à l\'AD : {} m3'.format(traj.
                                                              destination.
                                                              tas_dechets.
                                                              volume_m3))
                while traj.destination.tas_dechets.volume_m3 != 0 :
                    # Le véhicule effectue un aller-retour
                    cd.chargement(camion, traj.destination)
                    cd.dechargement(camion, traj.origine)
                    count_ar += 1
                    count_total_ar += 1
                    
                # Nombre d'AR : intégré dans l'objet Trajet
                nv_trajet.nb_AR = count_ar
                #nv_trajet.total_distance_km = count_dist
                print('Nombre d\'AR : {}'.format(nv_trajet.nb_AR))
                col_nb_ar.append(count_ar)

                duree_trajet = count_ar * 2 * traj.duree_h
                col_duree_h.append(duree_trajet)
                
                nv_trajet.duree_h = duree_trajet
                col_trajet.append(nv_trajet)       
       
                print('Durée du trajet : {} h'.format(nv_trajet.duree_h))
                print('---------------------------------------')

            
            # Calling DataFrame constructor after zipping
            # both lists, with columns specified
            df_par_camion = pd.DataFrame(list(zip(col_id_AD, 
                                                  col_vol_dechet,
                                                  col_trajet,
                                                  col_nb_ar,
                                                  col_duree_h)),
                                         columns =['idz',
                                                   'vol_dechets_m3',
                                                   'trajet',
                                                   'nb_AR',
                                                   'duree_estimee_h'])
            suivi_collecte_camions[camion.idVehicule] = df_par_camion
            
        # Volume de déchets présents sur le Plateau de la Savane 
        # à la fin de la collecte
        print('ZST de La Savane :\n {}'.format(scenario1.zst_la_savane))
        print('Volume total de déchets dans les AD : ' 
                  + str(scenario1.volume_total_dechet_ini))
        print('===> Conservation des volumes : ' 
                  + str(scenario1.zst_la_savane.tas_dechets.volume_m3 
                        == scenario1.volume_total_dechet_ini))
        camion_keys = []
        for camion in scenario1.flotte:
            camion_keys.append(camion.idVehicule)
        suivi_collecte_camions_concat = pd.concat(suivi_collecte_camions,
                                          keys = camion_keys)
        return suivi_collecte_camions_concat
        
    def estimation_jours(suivi_collecte_camions_concat):
        print('---------- Jours travaillés ----------')
        estimation_jours_par_camion = {}
        for camion in scenario1.flotte:
            suivi_trajets = suivi_collecte_camions_concat.loc[camion.idVehicule]
            count_jours = suivi_trajets['duree_estimee_h'].sum() // scenario1.entreprise.duree_travail_journalier_h
            reste = suivi_trajets['duree_estimee_h'].sum() % scenario1.entreprise.duree_travail_journalier_h
            if reste > scenario1.entreprise.duree_travail_journalier_h/2:
                count_jours += 1
            else:
                count_jours += 0.5
            
            estimation_jours_par_camion[camion.idVehicule] = count_jours
            print('Camion {} : {}'.format(camion.idVehicule,
                                                               count_jours))
            print('(Total heures : {})'.format(suivi_trajets['duree_estimee_h'].sum()))
        return estimation_jours_par_camion
    
if __name__ == "__main__":
    print(scenario1.entreprise)
    print('Durée travail journalier: {}h'.format(scenario1.entreprise.duree_travail_journalier_h))