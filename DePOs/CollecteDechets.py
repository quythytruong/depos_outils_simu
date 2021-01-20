from .Vehicule import Vehicule
from .ZoneDepot import AireDepose, ZoneStockageTemporaire, ZoneDepotFinal
from .Chemins import Trajectoire
import pandas as pd

def chargement(vehicule = Vehicule, a_depose = AireDepose) :
    """
    Méthode de chargement de déchet dans un véhicule.
    
    Dans le cas où le volume du déchet excède le volume disponible du véhicule, 
    le volume de déchets chargés correspond au volume disponible du véhicule.
    Dans le cas contraire, le véhicule charge tout le volume de déchet en entrée.
    Le chargement du véhicule va également induire une diminution de volume 
    de la quantité de déchet en entrée.


    Parameters
    ----------
    vehicule : TYPE, optional
        DESCRIPTION. The default is Vehicule.
    a_depose : TYPE, optional
        DESCRIPTION. The default is AireDepose.

    Returns
    -------
    Le volume de déchets chargés (en m3).

    """
    volume_charge = 0
    # Cas n °1 : le volume disponible dans le véhicule est trop faible 
    # pour charger tout le tas de déchets en entrée
    if a_depose.tas_dechets.volume_m3 > vehicule.volume_disponible :
        # Le volume chargé est le volume disponible dans le véhicule
        volume_charge = vehicule.volume_disponible
        
        a_depose.tas_dechets.dechets.volume_m3 -= vehicule.volume_disponible
        
        # On charge le véhicule de tout le volume disponible
        vehicule.tas_dechets_charges.dechets.volume_m3 = vehicule.capacite_max_m3
        
    # Cas n°2 : le volume disponible dans le véhicule est suffisant pour 
    # charger tout le tas de déchets en entrée
    else :
        # Le volume chargé est celui du tas de déchets de l'aire de dépose
        volume_charge = a_depose.tas_dechets.volume_m3
        
        vehicule.tas_dechets_charges.__add__(a_depose.tas_dechets.dechets)
        a_depose.tas_dechets.dechets.volume_m3 = 0
    
    print("Volume restant à l'AD " + str(a_depose.tas_dechets.volume_m3))
    return volume_charge

def dechargement(vehicule = Vehicule, zd_final = ZoneDepotFinal):
    """
    

    Parameters
    ----------
    vehicule : TYPE, optional
        DESCRIPTION. The default is Vehicule.
    zd_final : TYPE, optional
        DESCRIPTION. The default is ZoneDepotFinal.

    Returns
    -------
    Le volume de déchets déchargés (en m3).

    """
    volume_decharge = 0
    # Cas n°1 : la zone de dépôt est une zone de stockage temporaire
    if isinstance(zd_final, zd.ZoneStockageTemporaire):
        # Cas où le véhicule ne peut pas être entièrement déchargé
        if vehicule.volume_dechets_charges > zd_final.volume_disponible_m3:
                    
            volume_decharge = zd_final.volume_disponible_m3
            vehicule.tas_dechets_charges.dechets.volume_m3 -= volume_decharge
            zd_final.tas_dechets.dechets.volume_m3 += volume_decharge
                    
        # Cas où le véhicule peut être entièrement déchargé
        else:
            volume_decharge = vehicule.vider_vehicule()
            zd_final.tas_dechets.dechets.volume_m3 += volume_decharge
                
    else : # Cas n°2 : la zone de dépôt est finale
        volume_decharge = vehicule.vider_vehicule()
        zd_final.tas_dechets.dechets.volume_m3 += volume_decharge
    
    return volume_decharge

def vider_zone_depot(vehicule = Vehicule, trajectoire = Trajectoire, 
                     vitesse_km_h = 30, duree_chgt_h = 1.5, duree_dechgt_h = 1.5):
    """
    Vide entièrement une zone de dépôt par un véhicule.

    Parameters
    ----------
    vehicule : vehicule.Vehicule, optional
        Véhicule utilisé pour vider la zone de dépôt. The default is Vehicule.
    trajectoire : Trajectoire, optional
        Trajectoire effectuée par le véhicule. The default is Trajectoire.
    vitesse_km_h : Float, optional
        Vitesse du véhicule. The default is 30.
    duree_chgt_h : Float, optional
        Durée de chargement / déchargement du véhicule (en heures). 
        The default is 1.5 (1h30).

    Returns
    -------
    infos_collecte : pandas.Series
        Indicateurs de suivi de la collecte de la zone de dépôt :
            - Distance de la trajectoire empruntée (en km)
            - Durée de la trajectoire empruntée (en h)
            - Nombre d'allers-retours effectués sur la trajectoire
            - Distance totale du trajet (en km)
            - Durée totale du trajet (en h)            

    """
    
    index_infos = ['dist_trajectoire_km','duree_trajectoire_h',
                   'nb_ar','dist_tot_km','duree_estimee_h']
    
    dist_trajectoire_km = None
    count_total_dist =0
    count_ar = 0
    
    # Infos sur la trajectoire
    if hasattr(trajectoire, 'distance_km'):
        dist_trajectoire_km = trajectoire.distance_km
        # Estimation de la duree en fonction de la vitesse indiquéee
        # Par défaut, la vitesse = 30 km/h
        print('vitesse en km/h: ' + str(vitesse_km_h))
        duree_trajectoire_h = dist_trajectoire_km/vitesse_km_h
    elif hasattr(trajectoire, 'duree_h'):
        duree_trajectoire_h = trajectoire.duree_h   
    
    # Vidage de la zone de dépôt
    print('Volume à décharger' + str(trajectoire.
                                     destination.
                                     tas_dechets.
                                     volume_m3))
    while trajectoire.destination.tas_dechets.volume_m3 != 0 :
        # Le véhicule effectue un aller
        print('Chargement')
        chargement(vehicule, trajectoire.destination)
        # Le véhicule effectue un retour
        print('Déchargement')
        dechargement(vehicule, trajectoire.origine)
        
        print('Volume restants à décharger' + str(trajectoire.
                                     destination.
                                     tas_dechets.
                                     volume_m3))
        if hasattr(trajectoire, 'distance_km'):
            count_total_dist += trajectoire.distance_km*2
            
        count_ar += 1
    
    # Durée totale
    print('Calcul de la durée totale')
    if hasattr(trajectoire, 'distance_km'):
        # Estimation de la duree en fonction de la vitesse indiquéee
        # Par défaut, la vitesse = 30 km/h
        duree_totale_h = count_total_dist/vitesse_km_h
    elif hasattr(trajectoire, 'duree_h'):
        duree_totale_h = trajectoire.duree_h * 2 * count_ar
    # Ajoute les durées de (dé-)chargement du camion (1h30 par défaut)
    duree_totale_chargement = count_ar * (duree_chgt_h + duree_dechgt_h)
    # duree_totale_h += 2 * count_ar * duree_chgt_h 
    duree_totale_h += duree_totale_chargement
    
    infos_collecte = pd.Series([dist_trajectoire_km, duree_trajectoire_h,
                      count_ar, count_total_dist, duree_totale_h])
    infos_collecte.index = index_infos
    return infos_collecte
    
def vider_zone_depot_durant_periode(vehicule = Vehicule, 
                                     trajectoire = Trajectoire,
                                     vitesse_km_h = 30, 
                                     duree_chgt_h = 1.5,
                                     duree_dechgt_h = 1.5,
                                     periode_semaine = 1):
    periode_h = periode_semaine*7*24
    index_infos = ['dist_trajectoire_km','duree_trajectoire_h',
                   'nb_ar','dist_tot_km','duree_estimee_h',
                   'vol_dechets_AD']
    
    dist_trajectoire_km = None
    count_total_dist  = 0
    count_ar = 0
    count_duration = 0
    
    # Infos sur la trajectoire
    if hasattr(trajectoire, 'distance_km'):
        dist_trajectoire_km = trajectoire.distance_km
        # Estimation de la duree en fonction de la vitesse indiquéee
        # Par défaut, la vitesse = 30 km/h
        print('vitesse en km/h : ' + str(vitesse_km_h))
        duree_trajectoire_h = dist_trajectoire_km/vitesse_km_h
    elif hasattr(trajectoire, 'duree_h'):
        duree_trajectoire_h = trajectoire.duree_h   
    
    print('Durée cumulée : {} h'.format(count_duration))
    print('Volume AD : {} m3'.format(trajectoire.destination.tas_dechets.volume_m3))
    # Collecte des déchets à la zone de dépôt pendant la durée en paramètres
    while count_duration < periode_h:
        if trajectoire.destination.tas_dechets.volume_m3 != 0 :
            # Le véhicule effectue un aller
            chargement(vehicule, trajectoire.destination)
            # Le véhicule effectue un retour
            dechargement(vehicule, trajectoire.origine)
            
            count_ar += 1
            print('Nombre AR : {} '.format(count_ar))
            # Distance
            if hasattr(trajectoire, 'distance_km'):
                count_total_dist += trajectoire.distance_km*2
                # Durée
                count_duration = count_total_dist/vitesse_km_h
                
            
            elif hasattr(trajectoire, 'duree_h'):
                count_duration += trajectoire.duree_h * 2 * count_ar
            # Ajoute les durées de (dé-)chargement du camion (1h30 + 1h30 par défaut)
            count_duration += count_ar * (duree_chgt_h + duree_dechgt_h) 
        else:
            break
    print('Durée cumulée : {} h'.format(count_duration))
            
            
    infos_collecte = pd.Series([dist_trajectoire_km, duree_trajectoire_h,
                      count_ar, count_total_dist, count_duration,
                      trajectoire.destination.tas_dechets.volume_m3])
    infos_collecte.index = index_infos
    return infos_collecte

def vider_zone_depot_duree_variable_selon_volume(vehicule = Vehicule,
                                                 trajectoire = Trajectoire,
                                                 vitesse_km_h = 30):
    index_infos = ['dist_trajectoire_km','duree_trajectoire_h',
                   'nb_ar','dist_tot_km','duree_estimee_h',
                   'vol_dechets_AD']
    
    dist_trajectoire_km = None
    count_total_dist =0
    count_ar = 0
    duree_totale_h = 0
    
    # Infos sur la trajectoire
    if hasattr(trajectoire, 'distance_km'):
        dist_trajectoire_km = trajectoire.distance_km
        # Estimation de la duree en fonction de la vitesse indiquéee
        # Par défaut, la vitesse = 30 km/h
        print('vitesse en km/h: ' + str(vitesse_km_h))
        duree_trajectoire_h = dist_trajectoire_km/vitesse_km_h
    elif hasattr(trajectoire, 'duree_h'):
        duree_trajectoire_h = trajectoire.duree_h   
    
    # Vidage de la zone de dépôt
    print('Volume à décharger' + str(trajectoire.
                                     destination.
                                     tas_dechets.
                                     volume_m3))
    while trajectoire.destination.tas_dechets.volume_m3 != 0 :
        # Le véhicule effectue un aller
        print('Chargement')
        chargement(vehicule, trajectoire.destination)
        trajet_aller = c.Trajet(trajectoire = trajectoire, vehicule = vehicule)
        duree_totale_h += trajet_aller.duree
        # Le véhicule effectue un retour
        print('Déchargement')
        dechargement(vehicule, trajectoire.origine)
        trajet_retour = c.Trajet(trajectoire = trajectoire, vehicule = vehicule)
        duree_totale_h += trajet_retour.duree
        print('Volume restants à décharger' + str(trajectoire.
                                     destination.
                                     tas_dechets.
                                     volume_m3))
        if hasattr(trajectoire, 'distance_km'):
            count_total_dist += trajectoire.distance_km*2
            
        count_ar += 1
    
    # Durée totale
    print('Calcul de la durée totale')
    if hasattr(trajectoire, 'distance_km'):
        # Estimation de la duree en fonction de la vitesse indiquéee
        # Par défaut, la vitesse = 30 km/h
        duree_totale_h = count_total_dist/vitesse_km_h
    elif hasattr(trajectoire, 'duree_h'):
        duree_totale_h = trajectoire.duree_h * 2 * count_ar
        
    """
    # Ajoute les durées de (dé-)chargement du camion (1h30 par défaut)
    duree_totale_chargement = count_ar * (duree_chgt_h + 
                                          duree_dechgt_h)
    # duree_totale_h += 2 * count_ar * duree_chgt_h 
    duree_totale_h += duree_totale_chargement
    """
    infos_collecte = pd.Series([dist_trajectoire_km, duree_trajectoire_h,
                      count_ar, count_total_dist, duree_totale_h])
    infos_collecte.index = index_infos
    return infos_collecte

def duree_chargement(volume_dechets, typefonction = 'linéaire',
                     duree_h_min = 0,
                     duree_h_max = 3,
                     volume_min = 0,
                     volume_max = 32,
                     heure_par_m3 = 0.5/30):
    duree_h = 0
    if typefonction == 'linéaire':
        if volume_dechets <= volume_min:
            duree_h = duree_h_min
        elif volume_dechets >= volume_max:
            duree_h = duree_h_max
        else :
            duree_h = volume_dechets
    return duree_h

def dureeCollecteBassin(dureesVidageZoneDepot,
                        nbVehicules,
                        nbHeuresTravailParJour = 8):
    """ 
    Estime la durée moyenne de collecte des déchets de toutes les zones 
    de dépôt situées dans le même bassin de collecte.
    
    Parameters
    ----------
    dureesVidageZoneDepot: list
        Liste contenant les durées de vidage de chaque zone de dépôt
        
    nbVehicules: int
        Le nombre de véhicules présents sur le bassin pour effectuer la collecte
    
    nbHeuresTravailParJour: float
        Le nombre d'heures de travail par jour pour un véhicule
        
    """
    dureeTotale = sum(dureesVidageZoneDepot)/nbVehicules
    dureeTotaleParJour = dureeTotale/nbHeuresTravailParJour
    durees = {'duree_h' : dureeTotale,
              'duree_jour': dureeTotaleParJour,
              #'duree_semaine': dureeTotaleParJour/7,
              #'duree_mois': dureeTotaleParJour/(7*4)
              }
    return durees

def dureeVidageZoneDepot(volumeDechets, 
                         capaMaxVehicule,
                         distance_km, 
                         vitesse_km_h = 30,
                         duree_chgt_h = 1.5,
                         duree_dechgt_h = 1.5):
    """ 
    Calcule la durée totale qu'une zone de dépôt soit complètement vidée
    par un véhicule de capacité donnée.
    
    Parameters
    ----------
    volumeDechets: float
        Le volume de déchets présents sur la zone de dépôt collecter
    
    capaMaxVehicule: float
        La capacité maximale (en m3) du véhicule de collecte
    
    distance_km: float
        La distance (en km) du chemin entre la zone de dépôt à collecter 
        et la zone de dépôt où le véhicule va décharger les déchets
    
    vitesse_km_h: float
        Vitesse (en km/h) du véhicule de collecte. Par défaut, la vitesse 
        du véhicule est de 30 km/h.
        
    duree_chgt_h: float
        La durée nécessaire pour charger les déchets dans le véhicule.
        Par défaut, elle vaut 1h30.
        
    duree_dechgt_h: float
        La durée nécessaire pour décharger les déchets du véhicule.
        Par défaut, elle vaut 1h30.
    """
    
    nbAR = getNbAR(volumeDechets, capaMaxVehicule)
    dTrajet = dureeTrajet(distance_km, vitesse_km_h, duree_chgt_h,
                          duree_dechgt_h)
    dureeTotale = nbAR * dTrajet
    
    return dureeTotale
    
def getNbAR(volumeDechets, capaMaxVehicule):
    """ 
    Calcule le nombre d'allers-retours nécessaires 
    par un véhicule donné pour vider une zone de dépôt.
    
    """
    # Nombre de fois où le véhicule est complètement chargé de déchets
    nbARPlein = volumeDechets//capaMaxVehicule
    # Reste éventuel à charger (véhicule partiellement chargé)
    nbARPartiel = volumeDechets%capaMaxVehicule
    if nbARPartiel == 0:
        return nbARPlein
    else :
        return nbARPlein + 1

def dureeTrajet(distance_km,
                vitesse_km_h = 30, 
                duree_chgt_h = 1.5, 
                duree_dechgt_h = 1.5):
    """
    Calcule la durée d'un trajet, en tenant compte des durées des opérations
    de collecte.
    Un trajet = un aller + un chargement + un retour + un déchargement
    """
    dureeAR = 2*distance_km/vitesse_km_h
    dureeTotale = dureeAR + duree_chgt_h + duree_dechgt_h
    return dureeTotale