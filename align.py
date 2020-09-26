from pymol import cmd
import os

def detect_poche(conformation ,path_dock,path_poche):

	dossier_poche = os.listdir(path_poche)
	dossier_dock =  os.listdir(path_dock)



	cmd.load("{}/{}/{}.pdbqt".format(path_dock,conformation,conformation),"conf")
	cmd.load("{}/{}/out_{}.pdbqt".format(path_dock,conformation,conformation),"lig")

	cmd.create("obj","lig",1)
	

	score = 0
	score_max = 0
	pock = ''
	dossier_conf = os.listdir("{}/{}".format(path_poche,conformation))

	for i in range(len(dossier_conf) - 1):
	

		nom = "pocket{}".format(i)

		cmd.load('{}/{}/{}_atm.pdb'.format(path_poche,conformation,nom),nom)

		cmd.select("autour","obj around 4")
		align =cmd.align(nom,"autour")

		cmd.delete("autour")
		score = align[5]

		if score > score_max:
			score_max = score

			score = 0
			pock = nom

		cmd.delete(nom)

	cmd.delete("conf")
	cmd.delete("lig")

	print("La meilleure poche : {} pour le docking {}".format(pock,conformation))	
	return {conformation:pock}





path_dock = "C:/Users/Radja/Desktop/NS1/Vina/result"
path_poche = "C:/Users/Radja/Desktop/NS1/conformation/pockdrug"
dossier_dock =  os.listdir(path_dock)
i = 0

for conformation in dossier_dock:
	if i == 15:
		break
	i+=1
	detect_poche(conformation,path_dock,path_poche)
"""
	if(len(waiting) > 1):

		der = waiting[-1]
		avder = waiting[-2]

		cmd.load('{}/{}/{}_atm.pdb'.format(path_poche,conformation,der),der)
		cmd.load('{}/{}/{}_atm.pdb'.format(path_poche,conformation,avder),avder)

		Ader = cmd.align(der,"autour")
		Aavder = cmd.align(avder,"autour")
		print("Align entre",der,avder)

		if(Ader[5] > Aavder[5]):
			print("Align win par ",der)
			pock = der
		else:
			print("Align win par ",avder)
			pock = avder
"""