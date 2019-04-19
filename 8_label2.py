import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("8_labels2")
print(100*"~")
#tete de graphe2:
cur.execute("select tete from arbre2 limit 0 , 1")
ligne = cur.fetchone()
tete_actuel=ligne[0]
print("tete_actuel est: ", tete_actuel)
#max niveau:
cur.execute("select max(niveau) from arbre2")
ligne = cur.fetchone()
max=ligne[0]
cur.execute("select sommets from arbre2 where niveau=0")
ligne = cur.fetchone()
sommet=ligne[0]
#niveau0
cur.execute("select sommets from arbre2 where niveau=1")
ligne = cur.fetchone()
sommets=ligne[0]
list_sommets=sommets.split(',')
bas=len(list_sommets)
bas=str(bas)
label="0-0-0-"+bas
print("le label de ",sommet, " est ", label)
#os.system("cls")#effacer l'ecran
etat=True
cur.execute("select sommet, etiquette from labels1 where etiquette=?",(label,))
lignes = cur.fetchall()
list_image=[]
for img in lignes:
	somet=img[0]
	list_image.append(somet)
if(len(list_image)==0):
	print("pas d images pour le label:",label)
	etat=False
else:
	#insertion
	cur.execute("insert into labels2 (sommet, etiquette) values (?, ?)", (sommet, label))
	list_image.sort()
	str_image=",".join(list_image)
	cur.execute("insert into solutions (sommet, images, tete) values (?, ?, ?)", (sommet, str_image, tete_actuel))
	con.commit()#sauvgarde
#autres niveau
niv=1
while(niv<max):
	niv_haut=niv-1
	niv_bas=niv+1
	#haut:
	cur.execute("select sommets from arbre2 where niveau=?", (niv_haut,))
	ligne = cur.fetchone()
	sommets_h=ligne[0]
	list_sommets_h=sommets_h.split(',')
	set_sommets_h=set(list_sommets_h)
	#horizon
	cur.execute("select sommets from arbre2 where niveau=?", (niv,))
	ligne = cur.fetchone()
	sommets_h=ligne[0]
	list_sommets_m=sommets_h.split(',')
	set_sommets_m=set(list_sommets_m)
	#bas:
	cur.execute("select sommets from arbre2 where niveau=?", (niv_bas,))
	ligne = cur.fetchone()
	sommets_b=ligne[0]
	list_sommets_b=sommets_b.split(',')
	set_sommets_b=set(list_sommets_b)
	for som in list_sommets:
		#adjacents de som
		cur.execute("select adjacents from graphe2 where sommet=?", (som,))
		ligne = cur.fetchone()
		adjacents=ligne[0]
		list_adjacents=adjacents.split(',')
		set_adjacents=set(list_adjacents)
		#haut
		haut=len(set_adjacents & set_sommets_h)
		haut=str(haut)
		#horizon
		horison=len(set_adjacents & set_sommets_m)
		horison=str(horison)
		#bas
		bas=len(set_adjacents & set_sommets_b)
		bas=str(bas)
		#label
		niv_str=str(niv)
		label=niv_str+"-"+haut+"-"+horison+"-"+bas
		print("le label de ",som, " est ", label)
		#os.system("cls")#effacer l'ecran
		cur.execute("select sommet, etiquette from labels1 where etiquette=?",(label,))
		lignes = cur.fetchall()
		list_image=[]
		for img in lignes:
			somet=img[0]
			list_image.append(somet)
		if(len(list_image)==0):
			print("pas d images pour le label:",label)
			etat=False
			break
		else:
			#insertion
			cur.execute("insert into labels2 (sommet, etiquette) values (?, ?)", (som, label))
			list_image.sort()
			str_image=",".join(list_image)
			cur.execute("insert into solutions (sommet, images, tete) values (?, ?, ?)", (som, str_image, tete_actuel))
			con.commit()#sauvgarde
		if(etat==False):
			break
		print(30*"*")
	niv=niv+1
	list_sommets=list_sommets_b
#niveau dernier
if(etat):
	niv_haut=niv-1
	#haut:
	cur.execute("select sommets from arbre2 where niveau=?", (niv_haut,))
	ligne = cur.fetchone()
	sommets_h=ligne[0]
	list_sommets_h=sommets_h.split(',')
	set_sommets_h=set(list_sommets_h)
	#horizon
	cur.execute("select sommets from arbre2 where niveau=?", (niv,))
	ligne = cur.fetchone()
	sommets_h=ligne[0]
	list_sommets_m=sommets_h.split(',')
	set_sommets_m=set(list_sommets_m)
	for som in list_sommets:
		#adjacents de som
		cur.execute("select adjacents from graphe2 where sommet=?", (som,))
		ligne = cur.fetchone()
		adjacents=ligne[0]
		list_adjacents=adjacents.split(',')
		set_adjacents=set(list_adjacents)
		#haut
		haut=len(set_adjacents & set_sommets_h)
		haut=str(haut)
		#horizon
		horison=len(set_adjacents & set_sommets_m)
		horison=str(horison)
		#label
		niv_str=str(niv)
		label=niv_str+"-"+haut+"-"+horison+"-0"
		print("le label de ",som, " est ", label)
		#os.system("cls")#effacer l'ecran
		cur.execute("select sommet, etiquette from labels1 where etiquette=?",(label,))
		lignes = cur.fetchall()
		list_image=[]
		for img in lignes:
			somet=img[0]
			list_image.append(somet)
		if(len(list_image)==0):
			print("pas d images pour le label:",label)
			etat=False
			break
		else:
			#insertion
			cur.execute("insert into labels2 (sommet, etiquette) values (?, ?)", (som, label))
			list_image.sort()
			str_image=",".join(list_image)
			cur.execute("insert into solutions (sommet, images, tete) values (?, ?, ?)", (som, str_image, tete_actuel))
			con.commit()#sauvgarde
		print(30*"*")
if(etat):
	# passer a 9_valider_solutions.py
	cmd = '9_valider_solutions.py' # 9_valider_solutions.py		9_valider_solutions.py
	os.system("cls")#effacer l'ecran
else:
	#tete2
	cur.execute("select sommets from arbre2 where niveau=0")
	ligne = cur.fetchone()
	sommet=ligne[0]
	#delete arbre2
	cur.execute("DELETE FROM arbre2")
	cur.execute("delete from sqlite_sequence where name='arbre2'")# pour id=1
	#delete solutions
	cur.execute("DELETE FROM solutions where tete=?", (tete_actuel,))
	#cur.execute("delete from sqlite_sequence where name='solutions'")# pour id=1
	#delete labels2
	cur.execute("DELETE FROM labels2")
	cur.execute("delete from sqlite_sequence where name='labels2'")# pour id=1
	#fait='oui' dans graphe2
	cur.execute("update graphe2 set fait='oui' where sommet=?", (sommet,))
	con.commit()# Sauvgarde
	cur.execute("select count(id) from graphe2 where fait='non'")
	ligne = cur.fetchone()
	cnt=ligne[0]
	if(cnt==0):
		print("Les deux graphes ne sont pas isomorphes!")
		cmd = '10_fin.py'
	else:
		# passer a 6_arbres2.py
		cmd = '6_arbres2.py'
		os.system("cls")#effacer l'ecran
con.close()#fermer data base
print("aller ver",cmd)
#input("cliquez pour quiter!!!")
os.startfile(cmd)