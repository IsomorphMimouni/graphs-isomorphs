import head
import time
start_time = time.time()
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("get_one.py")
print(30*"~")
#generer un fichier solution
filename='u_solutions.txt'#unique solution
#par defaut:non
#-------------------------------------------------------------------------------------------------------------------------
#vidage de data:
#delete arbre1
cur.execute("DELETE FROM arbre1")
cur.execute("delete from sqlite_sequence where name='arbre1'")# pour id=1
#delete arbre2
cur.execute("DELETE FROM arbre2")
cur.execute("delete from sqlite_sequence where name='arbre2'")# pour id=1
#delete labels1
cur.execute("DELETE FROM labels1")
cur.execute("delete from sqlite_sequence where name='labels1'")# pour id=1
#delete labels2
cur.execute("DELETE FROM labels2")
cur.execute("delete from sqlite_sequence where name='labels2'")# pour id=1
#-------------------------------------------------------------------------------------------------------------------------
#compter les lignes:
cur.execute("select count(id) from solutions where fait='non'")
ligne = cur.fetchone()
cnt=ligne[0]
if(cnt==0):
	print("fin")
	#les sommets:
	list_graph=[]
	cur.execute("select distinct sommet from solutions")
	lignes = cur.fetchall()
	for s in lignes:
		list_graph.append(s[0])# s est un tuple
	list_graph.sort()
	# convert chaque element de list_graph en string @@@important@@@
	list_graph = list(map(str, list_graph))
	text_corct=""
	for sommet in list_graph:
		cur.execute("select images from solutions where sommet=?" , (sommet,))
		ligne = cur.fetchone()
		images=ligne[0]
		text_corct=text_corct+sommet+" "+images+"\n"
	print(text_corct)
	fichier = open(filename, "w")
	fichier.write(text_corct)
	fichier.close()
	#eteindre pc:	
	os.system ('shutdown /s /t 10')
else:
	cur.execute("select id, sommet, images from solutions where fait='non' limit 0 , 1") # sommet de graphe2 et images de graphe1
	ligne = cur.fetchone()
	id=ligne[0]
	sommet=ligne[1]
	images=ligne[2]
	print("sommet:",sommet," et images:",images)
	list_images=images.split(',')
	cnt_img=len(list_images)
	if(cnt_img==1):
		#update fait='non'
		cur.execute("update solutions set fait='oui' where id=?", (id, ))
		con.commit()#sauvgarde
		cmd = 'get_one.py'
	else:
		# un solution
		image=list_images[0]
		print("image choisi:",image)
		#update fait='non' images='image'
		cur.execute("update solutions set fait='oui' , images=? where id=?", (id, image))
		con.commit()#sauvgarde
		#arbre de sommet (graphe2)
		#adjacents de graphe2:
		cur.execute("select adjacents from graphe2 where sommet=?", (sommet,))
		ligne = cur.fetchone()
		adjacents2=ligne[0]
		#liste des sommets de graphe2
		set_graphe2=set()
		cur.execute("select sommet from graphe2")
		ligne = cur.fetchall()
		for a in ligne:
			sommet_a=a[0]
			set_graphe2.add(sommet_a)
		#insert dans niveau0:
		cur.execute("insert into arbre2 (niveau, sommets, tete) values (?, ?, ?)", (0, sommet, sommet))
		con.commit()#sauvgarde
		set_graphe2.remove(sommet)
		#insert dans niveau1:
		cur.execute("insert into arbre2 (niveau, sommets, tete) values (?, ?, ?)", (1, adjacents2, sommet))
		con.commit()#sauvgarde
		#print("adjacents: ",adjacents)
		list_adjacents2=adjacents2.split(',')
		set_adjacents2=set(list_adjacents2)
		set_graphe2=set_graphe2 - set_adjacents2
		niv2=1
		taille2=len(set_graphe2)
		#insert dans les autres niveaux:
		while(taille2>0):
			set_groupe2=set()
			niv2=niv2+1
			for k2 in list_adjacents2:
				k2=k2.strip("'")
				print("k2:",k2)
				cur.execute("select adjacents from graphe2 where sommet=?", (k2,))
				ligne = cur.fetchone()
				adjacents_k2=ligne[0]
				list_adjacents_k2=adjacents_k2.split(',')
				set_adjacents_k2=set(list_adjacents_k2)
				set_adjacents_k2=set_adjacents_k2 & set_graphe2
				set_groupe2=set_groupe2 | set_adjacents_k2
				set_graphe2=set_graphe2 - set_groupe2
				taille2=len(set_graphe2)
				if (taille2==0):
					break
			t_set_groupe2=len(set_groupe2)
			if (t_set_groupe2==0):
				break
			else:
				list_groupe2=list(set_groupe2)
				list_groupe2.sort()
				list_adjacents2=list_groupe2
				groupe2=",".join(list_groupe2)
				cur.execute("insert into arbre2 (niveau, sommets, tete) values (?, ?, ?)", (niv2, groupe2, sommet))
				con.commit()#sauvgarde
		#labels2
		#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		print("labels2")
		print(100*"~")
		#tete de graphe2:
		cur.execute("select tete from arbre2 limit 0 , 1")
		ligne = cur.fetchone()
		tete_actuel2=ligne[0]
		#max niveau:
		cur.execute("select max(niveau) from arbre2")
		ligne = cur.fetchone()
		max2=ligne[0]
		cur.execute("select sommets from arbre2 where niveau=0")
		ligne = cur.fetchone()
		sommet2=ligne[0]
		#niveau0
		cur.execute("select sommets from arbre2 where niveau=1")
		ligne = cur.fetchone()
		sommets2=ligne[0]
		list_sommets2=sommets2.split(',')
		bas2=len(list_sommets2)
		bas2=str(bas2)
		label2="0-0-0-"+bas2
		print("le label2 de ",sommet2, " est ", label2)
		#insertion
		cur.execute("insert into labels2 (sommet, etiquette) values (?, ?)", (sommet2, label2))
		con.commit()#sauvgarde
		#autres niveau
		niv2=1
		while(niv2<max2):
			niv_haut2=niv2-1
			niv_bas2=niv2+1
			#haut:
			cur.execute("select sommets from arbre2 where niveau=?", (niv_haut2,))
			ligne = cur.fetchone()
			sommets_h2=ligne[0]
			list_sommets_h2=sommets_h2.split(',')
			set_sommets_h2=set(list_sommets_h2)
			#horizon
			cur.execute("select sommets from arbre2 where niveau=?", (niv2,))
			ligne = cur.fetchone()
			sommets_h2=ligne[0]
			list_sommets_m2=sommets_h2.split(',')
			set_sommets_m2=set(list_sommets_m2)
			#bas:
			cur.execute("select sommets from arbre2 where niveau=?", (niv_bas2,))
			ligne = cur.fetchone()
			sommets_b2=ligne[0]
			list_sommets_b2=sommets_b2.split(',')
			set_sommets_b2=set(list_sommets_b2)
			for som2 in list_sommets2:
				#adjacents de som
				cur.execute("select adjacents from graphe2 where sommet=?", (som2,))
				ligne = cur.fetchone()
				adjacents2=ligne[0]
				list_adjacents2=adjacents2.split(',')
				set_adjacents2=set(list_adjacents2)
				#haut
				haut2=len(set_adjacents2 & set_sommets_h2)
				haut2=str(haut2)
				#horizon
				horison2=len(set_adjacents2 & set_sommets_m2)
				horison2=str(horison2)
				#bas
				bas2=len(set_adjacents2 & set_sommets_b2)
				bas2=str(bas2)
				#label
				niv_str2=str(niv2)
				label2=niv_str2+"-"+haut2+"-"+horison2+"-"+bas2
				print("le label2 de ",som2, " est ", label2)
				#insertion
				cur.execute("insert into labels2 (sommet, etiquette) values (?, ?)", (som2, label2))
				con.commit()#sauvgarde
			niv2=niv2+1
			list_sommets2=list_sommets_b2
		#niveau dernier
		niv_haut2=niv2-1
		#haut:
		cur.execute("select sommets from arbre2 where niveau=?", (niv_haut2,))
		ligne = cur.fetchone()
		sommets_h2=ligne[0]
		list_sommets_h2=sommets_h2.split(',')
		set_sommets_h2=set(list_sommets_h2)
		#horizon
		cur.execute("select sommets from arbre2 where niveau=?", (niv2,))
		ligne = cur.fetchone()
		sommets_h2=ligne[0]
		list_sommets_m2=sommets_h2.split(',')
		set_sommets_m2=set(list_sommets_m2)
		for som2 in list_sommets2:
			#adjacents de som
			cur.execute("select adjacents from graphe2 where sommet=?", (som2,))
			ligne = cur.fetchone()
			adjacents2=ligne[0]
			list_adjacents2=adjacents2.split(',')
			set_adjacents2=set(list_adjacents2)
			#haut
			haut2=len(set_adjacents2 & set_sommets_h2)
			haut2=str(haut2)
			#horizon
			horison2=len(set_adjacents2 & set_sommets_m2)
			horison2=str(horison2)
			#label
			niv_str2=str(niv2)
			label2=niv_str2+"-"+haut2+"-"+horison2+"-0"
			print("le label2 de ",som2, " est ", label2)
			#insertion
			cur.execute("insert into labels2 (sommet, etiquette) values (?, ?)", (som2, label2))
			con.commit()#sauvgarde
		#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
		#arbre de image (graphe1)
		#adjacents de graphe1:
		cur.execute("select adjacents from graphe1 where sommet=?", (image,))
		ligne = cur.fetchone()
		adjacents1=ligne[0]
		#liste des sommets de graphe1
		set_graphe1=set()
		cur.execute("select sommet from graphe1")
		ligne = cur.fetchall()
		for a in ligne:
			sommet_a=a[0]
			set_graphe1.add(sommet_a)
		#insert dans niveau0:
		cur.execute("insert into arbre1 (niveau, sommets, tete) values (?, ?, ?)", (0, image, image))
		con.commit()#sauvgarde
		set_graphe1.remove(image)
		#insert dans niveau1:
		cur.execute("insert into arbre1 (niveau, sommets, tete) values (?, ?, ?)", (1, adjacents1, image))
		con.commit()#sauvgarde
		#print("adjacents: ",adjacents)
		list_adjacents1=adjacents1.split(',')
		set_adjacents1=set(list_adjacents1)
		set_graphe1=set_graphe1 - set_adjacents1
		niv1=1
		taille1=len(set_graphe1)
		#insert dans les autres niveaux:
		while(taille1>0):
			set_groupe1=set()
			niv1=niv1+1
			for k1 in list_adjacents1:
				k1=k1.strip("'")
				print("k1:",k1)
				cur.execute("select adjacents from graphe1 where sommet=?", (k1,))
				ligne = cur.fetchone()
				adjacents_k1=ligne[0]
				list_adjacents_k1=adjacents_k1.split(',')
				set_adjacents_k1=set(list_adjacents_k1)
				set_adjacents_k1=set_adjacents_k1 & set_graphe1
				set_groupe1=set_groupe1 | set_adjacents_k1
				set_graphe1=set_graphe1 - set_groupe1
				taille1=len(set_graphe1)
				if (taille1==0):
					break
			t_set_groupe1=len(set_groupe1)
			if (t_set_groupe1==0):
				break
			else:
				list_groupe1=list(set_groupe1)
				list_groupe1.sort()
				list_adjacents1=list_groupe1
				groupe1=",".join(list_groupe1)
				cur.execute("insert into arbre1 (niveau, sommets, tete) values (?, ?, ?)", (niv1, groupe1, image))
				con.commit()#sauvgarde
		#labels1
		#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		print("labels1")
		print(100*"~")
		#tete de graphe1:
		cur.execute("select tete from arbre1 limit 0 , 1")
		ligne = cur.fetchone()
		tete_actuel1=ligne[0]
		#max niveau:
		cur.execute("select max(niveau) from arbre1")
		ligne = cur.fetchone()
		max1=ligne[0]
		cur.execute("select sommets from arbre1 where niveau=0")
		ligne = cur.fetchone()
		sommet1=ligne[0]
		#niveau0
		cur.execute("select sommets from arbre1 where niveau=1")
		ligne = cur.fetchone()
		sommets1=ligne[0]
		list_sommets1=sommets1.split(',')
		bas1=len(list_sommets1)
		bas1=str(bas1)
		label1="0-0-0-"+bas1
		print("le label1 de ",sommet1, " est ", label1)
		#insertion
		cur.execute("insert into labels1 (sommet, etiquette) values (?, ?)", (sommet1, label1))
		con.commit()#sauvgarde
		#autres niveau
		niv1=1
		while(niv1<max1):
			niv_haut1=niv1-1
			niv_bas1=niv1+1
			#haut:
			cur.execute("select sommets from arbre1 where niveau=?", (niv_haut1,))
			ligne = cur.fetchone()
			sommets_h1=ligne[0]
			list_sommets_h1=sommets_h1.split(',')
			set_sommets_h1=set(list_sommets_h1)
			#horizon
			cur.execute("select sommets from arbre1 where niveau=?", (niv1,))
			ligne = cur.fetchone()
			sommets_h1=ligne[0]
			list_sommets_m1=sommets_h1.split(',')
			set_sommets_m1=set(list_sommets_m1)
			#bas:
			cur.execute("select sommets from arbre1 where niveau=?", (niv_bas1,))
			ligne = cur.fetchone()
			sommets_b1=ligne[0]
			list_sommets_b1=sommets_b1.split(',')
			set_sommets_b1=set(list_sommets_b1)
			for som1 in list_sommets1:
				#adjacents de som
				cur.execute("select adjacents from graphe1 where sommet=?", (som1,))
				ligne = cur.fetchone()
				adjacents1=ligne[0]
				list_adjacents1=adjacents1.split(',')
				set_adjacents1=set(list_adjacents1)
				#haut
				haut1=len(set_adjacents1 & set_sommets_h1)
				haut1=str(haut1)
				#horizon
				horison1=len(set_adjacents1 & set_sommets_m1)
				horison1=str(horison1)
				#bas
				bas1=len(set_adjacents1 & set_sommets_b1)
				bas1=str(bas1)
				#label
				niv_str1=str(niv1)
				label1=niv_str1+"-"+haut1+"-"+horison1+"-"+bas1
				print("le label1 de ",som1, " est ", label1)
				#insertion
				cur.execute("insert into labels1 (sommet, etiquette) values (?, ?)", (som1, label1))
				con.commit()#sauvgarde
			niv1=niv1+1
			list_sommets1=list_sommets_b1
		#niveau dernier
		niv_haut1=niv1-1
		#haut:
		cur.execute("select sommets from arbre1 where niveau=?", (niv_haut1,))
		ligne = cur.fetchone()
		sommets_h1=ligne[0]
		list_sommets_h1=sommets_h1.split(',')
		set_sommets_h1=set(list_sommets_h1)
		#horizon
		cur.execute("select sommets from arbre1 where niveau=?", (niv1,))
		ligne = cur.fetchone()
		sommets_h1=ligne[0]
		list_sommets_m1=sommets_h1.split(',')
		set_sommets_m1=set(list_sommets_m1)
		for som1 in list_sommets1:
			#adjacents de som
			cur.execute("select adjacents from graphe1 where sommet=?", (som1,))
			ligne = cur.fetchone()
			adjacents1=ligne[0]
			list_adjacents1=adjacents1.split(',')
			set_adjacents1=set(list_adjacents1)
			#haut
			haut1=len(set_adjacents1 & set_sommets_h1)
			haut1=str(haut1)
			#horizon
			horison1=len(set_adjacents1 & set_sommets_m1)
			horison1=str(horison1)
			#label
			niv_str1=str(niv1)
			label1=niv_str1+"-"+haut1+"-"+horison1+"-0"
			print("le label1 de ",som1, " est ", label1)
			#insertion
			cur.execute("insert into labels1 (sommet, etiquette) values (?, ?)", (som1, label1))
			con.commit()#sauvgarde
		#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	#system solutions
	print("system solutions")
	print(100*"~")
	cur.execute("select id, sommet, images from solutions where fait='non'") # sommet de graphe2 et images de graphe1
	lignes = cur.fetchall()
	for ligne in lignes:
		id=ligne[0]
		sommet=ligne[1]
		images=ligne[2]
		print("solution id:",id," il rest :",cnt)
		list_images2=images.split(',')
		set_images2=set(list_images2)
		#labels2 de sommet:
		cur.execute("select etiquette from labels2 where sommet=?", (sommet,))
		ligne = cur.fetchone()
		etiquette2=ligne[0]
		#chercher dans graphe1 les sommets qui ont etiquette2
		cur.execute("select sommet from labels1 where etiquette=?",(etiquette2,))
		lignes = cur.fetchall()
		list_images1=[]
		for img in lignes:
			somet=img[0]
			list_images1.append(somet)
		set_images1=set(list_images1)
		set_images=set_images1 & set_images2
		list_images=list(set_images)
		list_images.sort()
		images=",".join(list_images)
		taille=len(list_images)
		if(taille==1):
			cur.execute("update solutions set fait='oui' , images=? where id=?", (id, images))
			con.commit()#sauvgarde
		else:
			cur.execute("update solutions set images=? where id=?", (id, images))
			con.commit()#sauvgarde
		cmd = 'get_one.py'
con.close()#fermer data base
# Affichage du temps d execution
fin_time = time.time()
duree=fin_time-start_time
duree=time.localtime(duree)
duree=time.strftime("%H heurs %M minutes %S seconds", duree)
print("script execute en:",duree)
os.startfile(cmd)