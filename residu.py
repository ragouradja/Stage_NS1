import os
from shutil import copyfile

def chercher_residu(path,pos_ref):  #FORMAT DE pos_ref : LISTE AVEC LES RESIDUS; FORMAT : [" XX "," XX "," XX "...]

	os.chdir(path)

	conf_actuelle = path[-4:]
	print("\n###################################################")
	print("\nAnalyse de la conformation : {} \n".format(conf_actuelle))
	

	#pos_ref = [" 34 "," 35 "," 36 "," 37 "," 38 "," 39 "," 40 "]
	poche_pos = {}
	bonne_conformation = {}

	pos = []


	nb_poche_ouverte = 0

	i = 0

	while(1):

		nom_poche = "pocket{}".format(i)

		try:
			fich = open("{}_atm.pdb".format(nom_poche),"r")
		except:		
			break
		
		nb_poche_ouverte += 1
		i += 1


		for ligne in fich:

			if ligne[:4] == "ATOM":
				
				for num in pos_ref:

					if num in ligne:

						if num not in pos:
							pos.append(num)


		if len(pos) != 0:
			poche_pos[nom_poche] = pos
			bonne_conformation[conf_actuelle] = poche_pos
							
		pos = []



		fich.close()



	if len(poche_pos) != 0:
		for pock in poche_pos.keys():

			print("La poche {} contient des residus en positions : {}".format(pock,poche_pos[pock]))
		

	print("\nNombre de poches ouvertes : {}".format(nb_poche_ouverte))
	print("\n###################################################\n\n\n")


	return bonne_conformation




#	MAIN	#


################################################################


liste = [" 38 "]

pockdrug = "C:/Users/Ragou/Desktop/NS1/conformation/pockdrug"

#POUR CREER LES DOSSIERS
source = "C:/Users/Ragou/Desktop/NS1/conformation/PDB_NS1"

destination = "C:/Users/Ragou/Desktop/NS1/conformation"

nom_dossier_global = "global"
nom_dossier_conf= "conf_ok"
nom_dossier_conf_poche = "conf_poche"


################################################################





nb_test = 0
bonne_conformation = {}

dossier_poche = os.listdir(pockdrug)

for dossier in dossier_poche :
	

	path_conf = "{}/{}".format(pockdrug,dossier)

	bonne_conformation.update(chercher_residu(path_conf,liste))


	nb_test += 1



print("Nombre de conformations testes : {} \n".format(nb_test))
print("\nNombre de conformation interessantes : {} \n".format(len(bonne_conformation)))

print(bonne_conformation.values())








#POUR DOCKING AVEC TOUS
if input("\n\nCreer un dossier avec ces conformations ? o/n \n") == "o":


	nv_dossier_global = "{}/{}".format(destination,nom_dossier_global)
	nv_dossier_conf = "{}/{}/{}".format(destination,nom_dossier_global,nom_dossier_conf)
	nv_dossier_conf_poche ="{}/{}/{}".format(destination,nom_dossier_global,nom_dossier_conf_poche)
	print(nv_dossier_conf_poche)

	try:
		os.mkdir(nv_dossier_global)
		os.mkdir(nv_dossier_conf)
		os.mkdir(nv_dossier_conf_poche)
		
	except:
		print("\nUn des dossiers existe deja \n")


		
	else:
		for conf in bonne_conformation.keys():


			
			#DOSSIER ALL CONF
			copyfile("{}/{}.pdb".format(source,conf),"{}/{}.pdb".format(nv_dossier_conf,conf))

			dossier_BC = "{}/{}".format(nv_dossier_conf_poche,conf)

			os.mkdir(dossier_BC)

			for poche in bonne_conformation[conf].keys():

				copyfile("{}/{}.pdb".format(source,conf),"{}/{}.pdb".format(dossier_BC,conf))
				copyfile("{}/{}/{}_atm.pdb".format(pockdrug,conf,poche),"{}/{}_atm.pdb".format(dossier_BC,poche))




		print("\nLes dossiers [{}], [{}] et [{}] ont ete crees".format(nom_dossier_global,nom_dossier_conf,nom_dossier_conf_poche))



"""

#DOSSIER CONF POCHE
if input("\n\nMettre les conformations et leurs poches dans un dossier ? ? o/n \n") == "o":


	nv_dossier_conf_poche = "{}/{}".format(destination,nom_dossier_conf)

	try:
		os.mkdir(nv_dossier_conf_poche)

	except:
		print("\nCe dossier existe deja \n")
		
	else:
		for pock in bonne_conformation.keys():
			

			copyfile("{}/{}.pdb".format(source,conf),"{}/{}.pdb".format(nv_dossier_conf_poche,conf))


		print("\nDossier [{}] cree".format(nom_dossier_conf))
"""