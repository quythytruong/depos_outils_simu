# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SimuDePOsDialog
                                 A QGIS plugin
 Outils pour générer des données et simuler la collecte de déchets post-ouragans
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Quy Thy Truong
        email                : quy-thy.truong2@univ-eiffel
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import QgsMapLayerProxyModel
from .fenetre_principale_depos8 import Ui_MainWindow

class DePosMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(DePosMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.suivi_couche_ad.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.suivi_couche_zst.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.suivi_couche_ad.setLayer(None)
        self.suivi_couche_zst.setLayer(None)
        self.suivi_couche_exutoire.setLayer(None)
        self.input_layer_ad_zst.setLayer(None)
        self.groupBox_5.setHidden(True)
        self.pushButton_4.setHidden(True)
        # Collecte par bassins
        self.partition_radio_on.toggled.connect(lambda : self.groupBox_5.setHidden(False)) # Collecte par bassin : ON
        self.partition_radio_on.toggled.connect(lambda : self.pushButton_4.setHidden(False)) # Collecte par bassin : ON
        self.partition_radio_off.toggled.connect(lambda : self.groupBox_5.setHidden(True)) # Collecte par bassin : OFF
        self.partition_radio_off.toggled.connect(lambda : self.pushButton_4.setHidden(True)) # Collecte par bassin : OFF
        self.bassinLayer_CBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.bassinLayer_CBox.setLayer(None)
        '''
        self.partition_radio_on.toggled.connect(lambda : self.nbVehicules_spinBox.setEnabled(False))
        self.partition_radio_on.toggled.connect(lambda : self.capaMaxMoy_doubleSpinBox.setEnabled(False))
        self.partition_radio_on.toggled.connect(lambda : self.capaMaxMoy_doubleSpinBox.setEnabled(False))
        self.partition_radio_off.toggled.connect(lambda : self.groupBox_5.setEnabled(False)) 
        self.partition_radio_off.toggled.connect(lambda : self.nbVehicules_spinBox.setEnabled(True))
        self.partition_radio_off.toggled.connect(lambda : self.capaMaxMoy_doubleSpinBox.setEnabled(True))
        self.pushButton_5.clicked.connect(lambda: self.fenetre_ppale.setCurrentWidget(self.tab))
        '''
        self.okModalitesCollecte_pushButton.clicked.connect(lambda: self.fenetre_ppale.setCurrentWidget(self.tab))        
        # Command line buttons        
        self.command_param_durees.clicked.connect(lambda: self.fenetre_ppale.setCurrentWidget(self.tab_durees))
        self.command_voir_resultats_simu.clicked.connect(lambda: self.fenetre_ppale.setCurrentWidget(self.tab3_result))
    
    def getInput(self):
        """ Récupère les données de paramétrage utiles pour la simulation """
        # Circuits à simuler
        simuCircuit1 = self.checkBox_ad_zst.isChecked()
        simuCircuit2 = self.checkBox_zst_isdnd.isChecked()
        
        # Couches des zones de dépôt
        zdLayer1 = self.suivi_couche_ad.currentLayer()
        zdLayer2 = self.suivi_couche_zst.currentLayer()
        zdLayer3 = self.suivi_couche_exutoire.currentLayer()
        
        isCollecteParBassin = self.partition_radio_on.isChecked() # Collecte par bassin 
        bassinLayer = self.bassinLayer_CBox.currentLayer()
        idBassinAttr = self.idBassin_CBox.currentText()
        chemin2ZSTLayer = self.input_layer_ad_zst.currentLayer() # Couche des chemins AD-ZST
        
        # Durées des opérations
        dureeChgt = self.input_chgt_duree_base.value()
        dureeDechgt = self.input_duree_base_dechgt.value()
        # Durées des opérations : options avancées
        isDureeChgtSelonVolume = self.check_duree_selon_volume.isChecked() # Durée en fonction du volume
        isDureeDechgtSelonVolume = self.check_duree_selon_volume_2.isChecked()        

        isDureeChgtSelonEquipment = self.checkBox_duree_reduite.isChecked() # Durée en fonction de l'équipement
        isDureeDechgtSelonEquipment = self.checkBox_duree_reduite_4.isChecked()
        isPenaliteTrafic = self.checkBox_18.isChecked() # Pénalité due au trafic
        
        # Acteurs de collecte
        nbVehicules = self.nbVehicules_spinBox.value()
        capaMaxMoy = self.capaMaxMoy_doubleSpinBox.value()
        
        return { "simuCircuit1" : simuCircuit1, "simuCircuit2" : simuCircuit2,
        "zdLayer1" : zdLayer1, "zdLayer2" : zdLayer2, "zdLayer3" : zdLayer3,
        "chemin2ZSTLayer" : chemin2ZSTLayer,
        "isCollecteParBassin" : isCollecteParBassin,
        "bassinLayer" : bassinLayer, "idBassin" :idBassinAttr,
        "dureeChgt" : dureeChgt, "dureeDechgt" : dureeDechgt,
        "isDureeChgtSelonVolume" : isDureeChgtSelonVolume,
        "isDureeDechgtSelonVolume" : isDureeDechgtSelonVolume,
        "isDureeChgtSelonEquipment" : isDureeChgtSelonEquipment,
        "isDureeDechgtSelonEquipment" : isDureeDechgtSelonEquipment,
        "isPenaliteTrafic" : isPenaliteTrafic,
        "nbVehicules" : nbVehicules,
        "capaMaxMoy" : capaMaxMoy
        }
        
    def recapScenario(self, paramScenario = {"simuCircuit1" : False, "simuCircuit2" : False,
        "zdLayer1" : None, "zdLayer2" : None, "zdLayer3" : None,
        "chemin2ZSTLayer" : None,
        "isCollecteParBassin" : False,
        "dureeChgt" : 0, "dureeDechgt" : 0,
        "isDureeChgtSelonVolume" : False,
        "isDureeDechgtSelonVolume" : False,
        "isDureeChgtSelonEquipment" : False,
        "isDureeDechgtSelonEquipment" : False,
        "isPenaliteTrafic" : False,
        "nbVehicules" : 0,
        "capaMaxMoy" : 0}):
        """ Récapitule le scénario simulé dans l'onglet "Résultats" de l'interface 
            
        Parameters
        ----------
        paramScenario : dict
            Paramétrage du scénario simulé.
        """
        # Circuit simulé
        self.recap_circuit1checkBox.setChecked(paramScenario["simuCircuit1"])
        self.recap_circuit2checkBox.setChecked(paramScenario["simuCircuit2"])
        # Zones de dépôt
        self.recap_gisementLayer.setLayer(paramScenario["zdLayer1"])
        self.recap_zstLayer.setLayer(paramScenario["zdLayer2"])
        self.recap_exutoireLayer.setLayer(paramScenario["zdLayer3"])
        # Acteurs
        self.recap_nbVehicules.setValue(paramScenario["nbVehicules"])
        self.recap_capaMaxMoy.setValue(paramScenario["capaMaxMoy"])            
        self.recap_collecteParBassin_checkBox.setChecked(paramScenario["isCollecteParBassin"]) # Collecte par bassin
        self.recap_cheminLayer.setLayer(paramScenario["chemin2ZSTLayer"]) # Chemins vers les ZST
        # Durées de chargement / déchargement
        self.recap_dureeChgt.setValue(paramScenario["dureeChgt"])
        self.recap_dureeDechgt.setValue(paramScenario["dureeDechgt"])
        self.recap_dureeChgtFoncVolume.setChecked(paramScenario["isDureeChgtSelonVolume"])
        self.recap_dureeDechgtFoncVolume.setChecked(paramScenario["isDureeDechgtSelonVolume"])
        self.recap_dureeChgFoncEquipt.setChecked(paramScenario["isDureeDechgtSelonEquipment"])
        self.recap_penaliteTrafic.setChecked(paramScenario["isPenaliteTrafic"])
    
    def displayResult(self, resultSimu, header = None):
        """ Affiche le résultat de la simulation dans l'onglet Résultats de l'interface 
        
        Parameters
        ----------
        resultSimu : list of list
        
        header : list
            Entête du tableau, contient les noms de colonnes
            
        """
        if not header is None:
            self.tableWidget.setColumnCount(len(header))
            self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.setRowCount(len(resultSimu))
        for i in range(len(resultSimu)):
            result = resultSimu[i]
            for j in range(len(result)):
                cellValue = result[j]
                if isinstance(cellValue, float):
                    cellValue = round(cellValue, 2)
                newitem = QTableWidgetItem(str(cellValue))
                self.tableWidget.setItem(i, j, newitem)
    
    def displayVisu(self, resultSimu, header = None):
        """
        Affiche les durées de collecte par zone de dépôt (de chargement) dans l'onglet Visualisation
        de l'interface.
        
        Parameters
        -----------
        resultSimu: list of list
        
        header : list
            Entête du tableau contenant les noms de colonnes
            
        """
        if not header is None:
            self.tableWidget_3.setColumnCount(len(header))
            self.tableWidget_3.setHorizontalHeaderLabels(header)
        self.tableWidget_3.setRowCount(len(resultSimu))
        for i in range(len(resultSimu)):
            result = resultSimu[i]
            for j in range(len(result)):
                cellValue = result[j]
                if isinstance(cellValue, float):
                    cellValue = round(cellValue, 2)
                newitem = QTableWidgetItem(str(cellValue))
                self.tableWidget_3.setItem(i, j, newitem)