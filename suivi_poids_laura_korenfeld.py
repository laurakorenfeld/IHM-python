#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:30:49 2022

@author: LKorenfeld
"""

import paramiko
import collections
import getpass, sys
import numpy as np
import matplotlib.pyplot as plt
import dbm
import sys
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QMainWindow, QWidget, QTextEdit, QLabel)




class Window(QWidget):
    
    def __init__(self):
        super().__init__()        
        self.init_ui()

    
    def init_ui(self):
        
        self.lbl = QLabel('Veuillez entrer votre poids (en kg) de la semaine pour effectuer votre suivi.')
        self.poids = QLineEdit('')
        self.b1 = QPushButton('Enregistrer')
        self.b2 = QPushButton('Graphique')
        
        
        v_box = QVBoxLayout()
        v_box.addWidget(self.lbl)
        v_box.addWidget(self.poids)
        v_box.addWidget(self.b1)
        v_box.addWidget(self.b2)
        
        self.setLayout(v_box)
        self.setWindowTitle("Suivi du poids")
        
   
        self.b1.clicked.connect(self.btn1_clk)
        self.b2.clicked.connect(self.btn2_clk)
        
        self.show()
    
    def btn1_clk(self):
        print(self.poids.text())
        self.addweight(self.poids.text())
       
    def addweight(self, poids):
        hostname = "192.168.120.129"
        username = "laura"
        password = "vitrygtr"
        port = 22

    
        t = paramiko.Transport((hostname, port)) #lien code et bd
        t.connect(username=username, password=password) #connexion
        sftp = paramiko.SFTPClient.from_transport(t) 

        name = "poids.db"

        path_vm = "/home/laura/poids.db"
        sftp.get(path_vm, name) #accès fichier et "prise"
        self.dbmfile = dbm.open('poids', 'c')
        print(self.dbmfile.keys())
        nombre= len(self.dbmfile.keys())+1
        print(nombre)
        print(poids)
        
        self.dbmfile[str(nombre)] = poids

        t.close()

            
    def btn2_clk(self):
        self.affweight(self.poids.text())
  
        
    def affweight(self, poids):
        hostname = "192.168.120.129"
        username = "laura"
        password = "vitrygtr"
        port = 22
        t = paramiko.Transport((hostname, port)) 
        t.connect(username=username, password=password) 
        sftp = paramiko.SFTPClient.from_transport(t) 

        name = "poids.db"
        path_vm = "/home/laura/poids.db"

        sftp.get(path_vm, name) #accès fichier et "prise"
        
        self.sem_poids = {} #dictionnaire qui sera de la forme clé=n°semaine : valeur=poids
        self.dbmfile = dbm.open('poids', 'c')

        for i in self.dbmfile.keys():
            self.sem_poids[float(i.decode('utf-8'))] = float(self.dbmfile[i].decode('utf-8'))
        self.sem_poids = collections.OrderedDict(sorted(self.sem_poids.items())) #tri du dictionnaire
           
        plt.title("Suivi hebdomadaire de votre poids.")
        plt.xlabel("Numéro de la semaine")
        plt.ylabel("Poids en kg")
        plt.grid()
        plt.plot(self.sem_poids.keys(), self.sem_poids.values())
        plt.show()
        
        self.dbmfile.close()
        sftp.put(name, path_vm)
        t.close()
        return self.weight
    


app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())

