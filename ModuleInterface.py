#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################# Déclaration des classes pour l'interface ##############################
import tkinter as tk
import tkinter.ttk as ttk
import ModuleCreationCorpus as MCC
import ModuleGraphe as MG
import sys

class Interface:
    def __init__(self):
        #Création de la fenêtre
        self.fenetre = tk.Tk()
        
        #Dimensions par défaut
        self.fenetre.geometry("1080x720")

        #Limiter les dimensions
        self.fenetre.maxsize(1080,720)
        self.fenetre.minsize(480,360)

        #Ajout d'un titre de page
        self.fenetre.title("Sélection du document du corpus")
        
        #Ajout d'un titre
        self.labe = tk.Label(self.fenetre, text="Veuillez entrer un thème puis valider", font=("Times", 20), fg='#000000')
        self.labe.pack()
        #Zone de saisie du texte
        self.theme_txt = tk.Entry(self.fenetre, width=50)
        self.theme_txt.pack()

        #Bouton de validation
        self.valid_txt = tk.Button(self.fenetre, text="Valider", font=("Arial",18), bg='#FDFEFE',fg='#212F3D', command =self.suite)
        self.valid_txt.pack()
        self.fenetre.mainloop()
        
        
    def suite(self):
        #Affichage du nom du thème entré
        self.thematique=self.theme_txt.get().lower()
        self.theme = tk.Label(self.fenetre, text="Vous avez entré le thème : " + self.thematique, font=("Calibri", 15), fg='#778899')
        self.theme.pack()
        
        #Appel à la fonction permettant de créer le corpus correspondant au thème choisi
        self.val=MCC.Creation(self.thematique)[0]
        
        #Ajout d'un titre
        self.lab = tk.Label(self.fenetre, text="Veuillez sélectionner le titre d'un document puis valider", font=("Times", 20), fg='#000000')
        self.lab.pack()
        #Liste déroulante affichant les titres des documents
        self.cbox = ttk.Combobox(self.fenetre, values = self.val, width = 75)
        self.cbox.pack()

        #Bouton de validation
        self.valid_bouton = tk.Button(self.fenetre, text="Valider", font=("Arial",18), bg='#FDFEFE',fg='#212F3D', command =lambda:[self.clic()])
        self.valid_bouton.pack()
        
        
    #Fonction associée à la validation
    def clic(self):
        self.valid_bouton.config(text="Génération du graphe...")
        self.valid_bouton.pack()
        self.idx=self.cbox.current()
        self.df = MCC.Creation(self.thematique)[1]
        MG.Grap(self.df[self.idx])
        self.fenetre.destroy()
        sys.exit()