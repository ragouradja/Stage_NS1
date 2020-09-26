from pymol import cmd
from math import sqrt
import os

#FONCTION POUR DETECTER LES CONFORMATIONS QUI ONT LE LIGAND PROCHE DU RESIDU 38 (= DANS LE RBD)
def detect_res38(path_dock,distance,pic = 0):

	dossier_dock =  os.listdir(path_dock)
	ok = {}


	for conformation in dossier_dock:
		
		cmd.load("{}/{}/{}.pdbqt".format(path_dock,conformation,conformation),"conf")
		cmd.load("{}/{}/out_{}.pdbqt".format(path_dock,conformation,conformation),"lig")



		cmd.create("obj","lig",1)

		cmd.center("obj")
		poz_lig = cmd.get_position()


		cmd.select("r38","res 38")
		cmd.center("r38")

		poz_38 = cmd.get_position()


		D = sqrt((poz_lig[0]-poz_38[0])**2 +(poz_lig[1]-poz_38[1])**2 +(poz_lig[2]-poz_38[2])**2)





		if(D < distance):	

			if(pic == 1):
				cmd.show("surface","r38")
				cmd.set_view ("\
				    -0.298310757,    0.680330575,   -0.669443905,\
				     0.016840594,    0.705018342,    0.708981633,\
				     0.954314768,    0.200224459,   -0.221768484,\
				    -0.000218070,   -0.000902027,  -86.197776794,\
				    40.384254456,   78.192932129,   43.972404480,\
				    -5.481759548,  177.321334839,  -20.000000000" )
				cmd.png(conformation,width = 1700, height = 750)
			ok.update({conformation:D})
		
		cmd.delete("conf")
		cmd.delete("lig")


	ok = sorted(ok.items(),key= lambda t:t[1])

	return ok



"""

path_dock = "C:/Users/Radja/Desktop/NS1/Vina/result"


dossier_dock =  os.listdir(path_dock)


ok = detect_res38(path_dock,20)

print("\nConformation \t Distance \t\t\t Energie\n")
for conf, dis in ok:
	nrj = energie.valeur_energie(path_dock,conf,"1")
	print(conf,"\t\t",dis,"\t\t",nrj)

print("\nNombre de conformations ayant le ligand proche du résidu 38 : ",len(ok))

"""