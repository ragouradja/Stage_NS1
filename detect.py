from pymol import cmd
from math import sqrt
import os

#FONCTION POUR DETECTER LA POCHE QUI CONTIENT LE LIGAND

#CONFORMATION : CONFORMATION POUR LAQUELLE IL FAUT DETECTER LA POCHE QUI CONTIENT LE LIGAND
#PATH_DOCK : CHEMIN QUI MENE AU DOSSIER QUI CONTIENT LES RESULTATS DE DOCKINGS
#PATH_POCHE : CHEMAIN QUI MENE AU DOSSIER QUI CONTIENT LES POCHES POUR LA CONFORMATION

def detect_distance(conformation ,path_dock,path_poche):

    #DOSSIER QUI CONTIENT LES POCHES
	dossier_poche = os.listdir(path_poche)

    #DOSSIER QUI CONTIENT LES RESULTATS DE DOCKING
	dossier_dock =  os.listdir(path_dock)



    #DOSSIER QUI CONTIENT LES CONFORMATIONS
	dossier_conf = os.listdir("{}/{}".format(path_poche,conformation))


	#ON CHARGE DANS PYMOL LA CONFORMATION ET LE LIGAND
	cmd.load("{}/{}/{}.pdbqt".format(path_dock,conformation,conformation),"conf")
	cmd.load("{}/{}/out_{}.pdbqt".format(path_dock,conformation,conformation),"lig")



    #ON SE FOCALISER SUR LA PREMIERE POSE DU LIGAND
	cmd.create("obj","lig",1)
	cmd.center("obj")

    #ON SAUVEGARDE LA POSITION DU CENTRE D'INERTIE DU LIGAND
	poz_lig = cmd.get_position()


    #VALEUR DE REFERENCE POUR LA DISTANCE QUI CHANGE AU FUR ET A MESURE
	D_ref = 100
	pock = ''
	
    #POUR TOUTES LES POCHES DE LA CONFORMATION
	for i in range(len(dossier_conf) - 1):

        #ON CHARGE LA POCHE DANS PYMOL
		nom = "pocket{}".format(i)
		cmd.load('{}/{}/{}_atm.pdb'.format(path_poche,conformation,nom),nom)
		cmd.center(nom)
        
        #ON SAUVEGARDE LA POSITION DU CENTRE D'INERTIE DE LA POCHE
		poz_pock = cmd.get_position()

        #ON CALCULE LA DISTANCE ENTRE LE CENTRE D'INERTIE DE LA POCHE ET DU LIGAND
		D = sqrt((poz_lig[0]-poz_pock[0])**2 +(poz_lig[1]-poz_pock[1])**2 +(poz_lig[2]-poz_pock[2])**2)
		
        #ON RETIENT LES POCHES QUI ONT UNE DISTANCE PAR RAPPORT AU LIGAND INFERIEUR A UNE DISTANCE REFERENCE
		if(D < D_ref):
			
            #ON ACTUALISE LA DISTANCE DE REFERENCE A LA DISTANCE LA PLUS FAIBLE
			D_ref = D
			pock = nom



		cmd.delete(nom)

	cmd.delete("conf")
	cmd.delete("lig")
	#print("La meilleure poche : {} pour le docking {}".format(pock,conformation))	

	return {conformation:pock}





path_dock = "C:/Users/Radja/Desktop/NS1/Vina/result"
path_poche = "C:/Users/Radja/Desktop/NS1/conformation/pockdrug"
dossier_dock =  os.listdir(path_dock)
i = 0

for conformation in dossier_dock:
	
	
	detect_distance(conformation,path_dock,path_poche)
	
