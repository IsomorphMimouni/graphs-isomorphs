import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("5_labels1")
print(100*"~")
# les entetes:
cur.execute("select distinct tete from arbre1")
ligne = cur.fetchall()
list_tete=[]
for t in ligne:
	list_tete.append(t[0])
for tete in list_tete:
	#max niveau:
	cur.execute("select max(niveau) from arbre1 where tete=?", (tete,))
	ligne = cur.fetchone()
	max=ligne[0]
	#print("max=",max)
	cur.execute("select sommets from arbre1 where niveau=0 and tete=?", (tete,))
	ligne = cur.fetchone()
	sommet=ligne[0]
	#niveau0
	cur.execute("select sommets from arbre1 where niveau=1 and tete=?", (tete,))
	ligne = cur.fetchone()
	sommets=ligne[0]
	list_sommets=sommets.split(',')
	bas=len(list_sommets)
	bas=str(bas)
	label="0-0-0-"+bas
	print("le label de ",sommet, " est ", label)
	#insertion
	cur.execute("insert into labels1 (sommet, etiquette) values (?, ?)", (sommet, label))#il y a des doublon
	con.commit()#sauvgarde
	#autres niveau
	niv=1
	while(niv<max):
		niv_haut=niv-1
		niv_bas=niv+1
		#haut:
		cur.execute("select sommets from arbre1 where niveau=? and tete=?", (niv_haut, tete))
		ligne = cur.fetchone()
		sommets_h=ligne[0]
		list_sommets_h=sommets_h.split(',')
		set_sommets_h=set(list_sommets_h)
		#horizon
		cur.execute("select sommets from arbre1 where niveau=? and tete=?", (niv, tete))
		ligne = cur.fetchone()
		sommets_h=ligne[0]
		list_sommets_m=sommets_h.split(',')
		set_sommets_m=set(list_sommets_m)
		#bas:
		cur.execute("select sommets from arbre1 where niveau=? and tete=?", (niv_bas, tete))
		ligne = cur.fetchone()
		sommets_b=ligne[0]
		list_sommets_b=sommets_b.split(',')
		set_sommets_b=set(list_sommets_b)
		for som in list_sommets:
			#print("som: ", som)
			#adjacents de som
			cur.execute("select adjacents from graphe1 where sommet=?", (som,))
			ligne = cur.fetchone()
			adjacents=ligne[0]
			#print("adjacents: ",adjacents)
			list_adjacents=adjacents.split(',')
			#print("list_adjacents: ",list_adjacents)
			set_adjacents=set(list_adjacents)
			#print("set_adjacents: ",set_adjacents)
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
			#insertion
			cur.execute("insert into labels1 (sommet, etiquette) values (?, ?)", (som, label))
			con.commit()#sauvgarde
		niv=niv+1
		list_sommets=list_sommets_b
	#print("niv apres while: ", niv)
	#niveau dernier
	niv_haut=niv-1
	#haut:
	cur.execute("select sommets from arbre1 where niveau=? and tete=?", (niv_haut, tete))
	ligne = cur.fetchone()
	sommets_h=ligne[0]
	list_sommets_h=sommets_h.split(',')
	set_sommets_h=set(list_sommets_h)
	#horizon
	cur.execute("select sommets from arbre1 where niveau=? and tete=?", (niv, tete))
	ligne = cur.fetchone()
	sommets_h=ligne[0]
	list_sommets_m=sommets_h.split(',')
	set_sommets_m=set(list_sommets_m)
	for som in list_sommets:
		#print("som: ", som)
		#adjacents de som
		cur.execute("select adjacents from graphe1 where sommet=?", (som,))
		ligne = cur.fetchone()
		adjacents=ligne[0]
		#print("adjacents: ",adjacents)
		list_adjacents=adjacents.split(',')
		#print("list_adjacents: ",list_adjacents)
		set_adjacents=set(list_adjacents)
		#print("set_adjacents: ",set_adjacents)
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
		cur.execute("insert into labels1 (sommet, etiquette) values (?, ?)", (som, label))
		con.commit()#sauvgarde
		print(30*"*")
con.close()#fermer data base
# passer a 6_arbres2.py
cmd = '6_arbres2.py'
os.system("cls")#effacer l'ecran 
os.startfile(cmd)