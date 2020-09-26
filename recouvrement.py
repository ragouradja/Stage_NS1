from pymol import cmd
import res38
import detect
import os


path_dock = "C:/Users/Radja/Desktop/NS1/Vina/result"
path_poche = "C:/Users/Radja/Desktop/NS1/conformation/pockdrug"
distance = 20

dossier_dock =  os.listdir(path_dock)

#  0019 0015
# CORRECTION MANUELLE
dico_poche = {"0019" : "pocket0","0015":"pocket0"}
proche_res38 = res38.detect_res38(path_dock,20)

for conformation, dis in proche_res38:
	if(conformation not in dico_poche):
		dico_poche.update(detect.detect_distance(conformation,path_dock,path_poche))

print("Conformation\t\t Poche\t\t Recouvrement\n")
for conformation,poche in dico_poche.items():

#	conformation = "0101"
#	poche = "pocket0"

	cmd.load("{}/{}/{}.pdbqt".format(path_dock,conformation,conformation),conformation)
	cmd.load("{}/{}/out_{}.pdbqt".format(path_dock,conformation,conformation),"lig")


	cmd.create("obj","lig",1)
	cmd.select("autour","obj around 4")


	dossier_conf = os.listdir("{}/{}".format(path_poche,conformation))


	cmd.load('{}/{}/{}_atm.pdb'.format(path_poche,conformation,poche),poche)
	cmd.show("surface",poche)
	
	np1 = cmd.count_atoms(poche)
	np2 = cmd.count_atoms("autour")

	#align = cmd.align(poche,"autour")
	#nc = align[4]


	cmd.select("a","autour in {}".format(poche))
	nc = cmd.count_atoms("a")


	rec = (100 * nc) / (np1+np2-nc)
	print(conformation,'\t\t\t',poche,'\t',round(rec,2),"%")
	cmd.reinitialize()

print("\nRecouvrement en ne comptant pas les atomes de la poche parmi les atomes proches du ligand")