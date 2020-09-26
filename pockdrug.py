from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os



#CHEMINS
#############################################################


#DOSSIER CIBLE POUR LES TELECHARGEMENTS
download_dir = '/home/ragou/Bureau/NS1/conf/pockdrug'


#DOSSIER CONTENANT LES CONFORMATIONS A TESTER
conformation = '/home/ragou/Bureau/NS1/conf/PDB_NS1'


#CHEMIN QUI MENE AU WEBDRIVER DE VOTRE NAVIGATEUR
driver = "/home/ragou/Bureau/NS1/chromedriver"


#############################################################


#PARAMETRES
#############################################################


#NOMBRE DE FICHIER QUI VONT S'OUVRIR AU TOTAL
onglet_total = 68

#TELECHARGEMENT PAR TRANCHE DE
tranche = 10


#############################################################





onglet_ouvert = 0
indice_depart = 0
nb_fichier_ouvert = 0

dossier = os.listdir(conformation)

filename = []


downname = "pocket_PPE.zip"


#OPTIONS POUR DEFINIR LE DOSSIER CIBLE DES TELECHARGEMENT
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"download.default_directory": download_dir })


#OUVRE UNE PAGE CHROME
navigateur = webdriver.Chrome(chrome_options = chrome_options, executable_path = driver) 
navigateur.maximize_window()

#ALLER SUR LE SITE
navigateur.get("http://pockdrug.rpbs.univ-paris-diderot.fr/cgi-bin/index.py?page=Druggability")

#POUR METTRE LES CONFORMATIONS SUR POCKDRUG
for fichier in dossier:		

	
	nb_fichier_ouvert +=1
	onglet_ouvert += 1


	#SI ON A ATTEINT LE NOMBRE DE FICHIER OUVERT VOULU (onglet) ON STOP
	if nb_fichier_ouvert > onglet_total:
		navigateur.close()
		nb_fichier_ouvert -= 1
		break
	

	print("Conformation ouverte : {}".format(fichier))

	filename.append(fichier)
	

	upload = '{}/{}'.format(conformation,fichier)

	#CHOISIR LA 2E SECTION
	navigateur.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/form/fieldset[2]/div/label/font/b/input').click()


	#COCHER "UPLOAD YOUR PDB FILE"
	navigateur.find_element_by_id("Radio1").click()

	#UPLOAD LE FICHIER
	navigateur.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/form/div[2]/div/fieldset[1]/div/div[1]/a/input').send_keys(upload)

	#SUBMIT	
	navigateur.find_element_by_xpath("/html/body/div[2]/div/div[2]/center/input[1]").click()

	#OUVRIR UN NOUVEL ONGLET
	navigateur.execute_script("window.open('http://pockdrug.rpbs.univ-paris-diderot.fr/cgi-bin/index.py?page=Druggability')") 


	if onglet_ouvert == tranche or nb_fichier_ouvert == onglet_total:
		print("\n\n")

		#TELECHARGE LES POCHES DES CONFORMATIONS OUVERTS DANS POCKDRUG
		for i in range(indice_depart,indice_depart + onglet_ouvert):

			
			navigateur.switch_to.window(navigateur.window_handles[0])
			time.sleep(1)
			
			navigateur.find_element_by_xpath('//*[@id="PPE-desc"]/div[2]/form/div/input').click()
			navigateur.close()

			time.sleep(2)
			os.rename("{}/{}".format(download_dir,downname),"{}/{}.zip".format(download_dir,os.path.splitext(filename[i])[0]))

		print("Avancee : {}\n".format(nb_fichier_ouvert))
		indice_depart += onglet_ouvert
		onglet_ouvert = 0



	#ON SWITCH SUR LE NOUVEL ONGLET POUR POUVOIR AGIR DESSUS
	navigateur.switch_to.window(navigateur.window_handles[onglet_ouvert])



print("\nNombre de fichiers telecharges au total : {}".format(nb_fichier_ouvert))