import os
import detect
import matplotlib.pyplot as plt
import res38

def valeur_energie(path_dock,conformation,pose):

	with open("{}/{}/log_{}.txt".format(path_dock,conformation,conformation)) as fich:
		for ligne in fich:
			if(ligne[:4] =='   {}'.format(pose)):
				mot = ligne.split(" ")
			
				if(mot[11] ! = ""):
					return (float(mot[11]))          
				else:
					return (float(mot[12]))
                    
def valeur_drug(path_poche,conformation,poche):
	nom = "{}_atm".format(poche)

	with open("{}/{}/pocket_PPE.txt".format(path_poche,conformation)) as fich:
		for ligne in fich:
			mot = ligne.split("\t")
			if(mot[0] == nom):

				return (float(mot[-2]))


path_dock = "C:/Users/Radja/Desktop/NS1/Vina/result"
path_poche = "C:/Users/Radja/Desktop/NS1/conformation/pockdrug"

dossier_poche = os.listdir(path_poche)
dossier_dock =  os.listdir(path_dock)


proche_res38 = res38.detect_res38(path_dock,20)



dico = {}
pose = "1"

energie = []
drug = []
conf_list = []
poche_list= []

"""
#res38
for conf, dis in proche_res38:
	dico.update(detect.detect_distance(conf,path_dock,path_poche))
"""

for conf in dossier_dock:
	dico.update(detect.detect_distance(conf,path_dock,path_poche))

	

for conformation,poche in dico.items():
	conf_list.append(conformation)
	poche_list.append(poche)
	energie.append(valeur_energie(path_dock,conformation,pose))
	drug.append(round(valeur_drug(path_poche,conformation,poche),2))

energie,drug,conf_list,poche_list = zip(*sorted(zip(energie,drug,conf_list,poche_list)))

taille = len(energie)



plt.plot(energie,drug,'ro')
plt.ylabel("Druggability")
plt.xlabel("Valeur d'energie")
plt.axvline(-9.5)
plt.axhline(0.5)

list_HG = []
list_BG = []
list_HD = []
list_BD = []
HG = 0 
HD = 0
BG = 0
BD = 0


for e,d,con,po in zip(energie,drug,conf_list,poche_list):
	if(e < -9.5 and d > 0.5):
		
		list_HG.append((e,d,con,po))
		HG +=1

	if(e < -9.5 and d < 0.5):
		list_BG.append((e,d,con,po))
		BG +=1

	if(e > -9.5 and d > 0.5):
		list_HD.append((e,d,con,po))
		HD +=1

	if(e > -9.5 and d < 0.5):
		list_BD.append((e,d,con,po))
		BD +=1




PHG = round(HG/taille * 100,2)
PHD = round(HD/taille * 100,2)
PBG = round(BG/taille * 100,2)
PBD = round(BD/taille * 100,2)









print("\nPARTIE EN HAUT A GAUCHE\n")
print("Energie\t\t Druggability\t\t Conformation\t Poche")

for e,d,c,p in list_HG:

	print(e,'\t\t',d,'\t\t\t',c,'\t\t',p)
print("\nNombre de conformations : ",len(list_HG))


print("\nPARTIE EN HAUT A DROITE\n")
print("Energie\t\t Druggability\t\t Conformation\t Poche")

for e,d,c,p in list_HD:

	print(e,'\t\t',d,'\t\t\t',c,'\t\t',p)
print("\nNombre de conformations : ",len(list_HD))



print("\nPARTIE EN BAS A GAUCHE\n")
print("Energie\t\t Druggability\t\t Conformation\t Poche")

for e,d,c,p in list_BG:

	print(e,'\t\t',d,'\t\t\t',c,'\t\t',p)
print("\nNombre de conformations : ",len(list_BG))


print("\nPARTIE EN BAS A DROITE\n")
print("Energie\t\t Druggability\t\t Conformation\t Poche")

for e,d,c,p in list_BD:

	print(e,'\t\t',d,'\t\t\t',c,'\t\t',p)
print("\nNombre de conformations : ",len(list_BD))




plt.annotate("{}%".format(PHG),xy=(-9.65,0.52))

plt.annotate("{}%".format(PHD),xy=(-9.45,0.52))

plt.annotate("{}%".format(PBG),xy=(-9.65,0.45))

plt.annotate("{}%".format(PBD),xy=(-9.45,0.45))

#plt.title("Conformations ayant le ligand dans le RBD")
plt.show()