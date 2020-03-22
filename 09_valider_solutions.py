import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
filename='correction.txt'
#par defaut:non
fichier = open(filename, "w")
text_corct="non"
fichier.write(text_corct)
fichier.close()
#-------------------------------------------------------------------------------------------------------------------------
os.system("cls")#effacer l'ecran
print("09_valider_solutions")
print(30*"~")
#valider une ligne de solution
cur.execute("select id, sommet, images, tete from solutions where fait='non' limit 0 , 1") # sommet de graphe2 et images de graphe1
ligne = cur.fetchone()
id=ligne[0]
sommet=ligne[1]
images=ligne[2]
tete=ligne[3]
print("sommet:",sommet," et images:",images," et tete:",tete)
list_images=images.split(',')
#adjacents1
cur.execute("select adjacents from graphe2 where sommet=?", (sommet,))
ligne = cur.fetchone()
adjacents1=ligne[0]
list_adjacents1=adjacents1.split(',')
set_adjacents1=set(list_adjacents1)
#----------------------------------------------------------------------------------------------------------------------------
set_upd=set()#pour les images valider
corect_etat=False
for img in list_images:
	#print("tester ",sommet," avec ",img)
	err=0
	#print("valeur initial de err est: ",err)
	#adjacents2
	cur.execute("select adjacents from graphe1 where sommet=?", (img,))
	ligne = cur.fetchone()
	adjacents2=ligne[0]
	list_adjacents2=adjacents2.split(',')
	set_adjacents2=set(list_adjacents2)
	for adj in list_adjacents1:
		#solutions
		cur.execute("select images from solutions where sommet=?", (adj,))
		ligne = cur.fetchone()
		images_adj=ligne[0]
		list_images_adj=images_adj.split(',')
		set_images_adj=set(list_images_adj)
		set_intersection=set_images_adj & set_adjacents2
		#print("adj ",adj)
		#print("set_images_adj: ",set_images_adj)
		#print("set_adjacents2: ",set_adjacents2)
		if(len(set_intersection)==0):
			err=err+1
			break
	#print("nouvelle valeur de err est: ",err)
	if(err!=0):
		print(id,":", sommet,"#",img)
		corect_etat=True
	else:
		set_upd.add(img)
		print("\t\t",id,":", sommet,":",img)
#----------------------------------------------------------------------------------------------------------------------------
if(len(set_upd)==0):
	print(id," Les solutions ne sont pas validé pour sommet:", sommet)
	print(50*"Y")
	#non dans fichier 'correction.txt'
	fichier = open(filename, "w")
	text_corct="non"
	fichier.write(text_corct)
	fichier.close()
	#delete labels2
	cur.execute("DELETE FROM labels2")
	cur.execute("DELETE from sqlite_sequence where name='labels2'")# pour id=1
	#delete arbre2
	cur.execute("DELETE FROM arbre2")
	cur.execute("DELETE from sqlite_sequence where name='arbre2'")# pour id=1
	#DELETE solutions pour tete
	cur.execute("DELETE FROM solutions where tete=?", (tete,))
	#update fait='oui' graphe2
	cur.execute("update graphe2 set fait='oui' where sommet=?", (tete,))
	con.commit()# Sauvgarde
	print("graphe2 set fait='oui' pour tete=", tete)
	#nombre des fait='non' dans graphe2
	cur.execute("select count(id) from graphe2 where fait='non'")
	ligne_g2 = cur.fetchone()
	cnt_g2=ligne_g2[0]
	if(cnt_g2==0):
		print("les deux graphes ne sont pas isomorphes")
		cmd = '10_fin.py'
	else:
		cmd = '06_arbres2.py'
#----------------------------------------------------------------------------------------------------------------------------
else:
	#mise dans solutions:
	list_upd=list(set_upd)
	list_upd.sort()
	upd=",".join(list_upd)
	print(id," La solution est validé pour sommet:", sommet,":",upd)
	print(50*"w")
	cur.execute("update solutions set images=?, fait='oui' where sommet=?", (upd, sommet))
	con.commit()#sauvgarde
	if(corect_etat):
		#oui dans fichier 'correction.txt'
		fichier = open(filename, "w")
		text_corct="oui"
		fichier.write(text_corct)
		fichier.close()
	#nombre des fait='non' dans solutions
	cur.execute("select count(id) from solutions where fait='non'")
	ligne_s = cur.fetchone()
	cnt_s=ligne_s[0]#pour solutions
	if(cnt_s==0):
		#lire fichier 'correction.txt'
		fichier = open(filename, "r")
		content=fichier.readline()
		fichier.close()
		if(content=='oui'):
			print("fichier correction:oui")
			#mise dans solutions: fait='non' pour tete
			cur.execute("update solutions set fait='non' where tete=?", (tete,))
			con.commit()#sauvgarde
			#non dans fichier 'correction.txt'
			fichier = open(filename, "w")
			text_corct="non"
			fichier.write(text_corct)
			fichier.close()
			cmd='09_valider_solutions.py'
		else:
			print("fichier correction:non") # content=='non'
			#update fait='oui' graphe2 pour tous les sommets de arbre2 
			cur.execute("select sommet from solutions where tete=?", (tete,))
			lignes = cur.fetchall()
			for som_sol in lignes:
				cur.execute("update graphe2 set fait='oui' where sommet=?", som_sol)
			con.commit()# Sauvgarde
			#nombre des fait='non' dans graphe2 (pour graphe noconexte)
			cur.execute("select count(id) from graphe2 where fait='non'")
			ligne_g2 = cur.fetchone()
			cnt_g2=ligne_g2[0]
			if(cnt_g2==0):
				print("Fin de programme aller voir la solution!!!!")
				cmd = '10_fin.py' #fin if(cn_g2==0)
			else:
				#fin de traitement d'un composant conexte et passer au composant suivant....
				#DELETE arbre2
				cur.execute("DELETE FROM arbre2")
				cur.execute("DELETE from sqlite_sequence where name='arbre2'")# pour id=1
				#DELETE labels2 
				cur.execute("DELETE FROM labels2")
				cur.execute("DELETE from sqlite_sequence where name='labels2'")# pour id=1
				con.commit()# Sauvgarde
				# passer a 06_arbres2.py
				cmd = '06_arbres2.py'
	else:
		###(cnt_s==0):
		cmd = '09_valider_solutions.py'
#----------------------------------------------------------------------------------------------------------------------------
con.close()#fermer data base
print("fichier:09_valider_solutions.py")
os.startfile(cmd)