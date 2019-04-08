import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("4_arbres1")
print(100*"~")
#-------------------------------------------------------------------------------------------------------------------------
#liste des sommets de graphe1
set_graphe=set()
cur.execute("select sommet from graphe1")
lignes = cur.fetchall()
for a in lignes:
	sommet_a=a[0]
	set_graphe.add(sommet_a)
taille=len(set_graphe)
while(taille>0):
	#tete d arbre:
	list_graphe=list(set_graphe)
	list_graphe.sort()
	tete=list_graphe[0]
	cur.execute("select adjacents from graphe1 where sommet=?", (tete,))
	ligne = cur.fetchone()
	adjacents=ligne[0]
	print("le sommet de depart est: ", tete ," a suivre.....")
	#insert dans niveau0:
	cur.execute("insert into arbre1 (niveau, sommets, tete) values (?, ?, ?)", (0, tete, tete))
	con.commit()#sauvgarde
	set_graphe.remove(tete)
	#insert dans niveau1:
	cur.execute("insert into arbre1 (niveau, sommets, tete) values (?, ?, ?)", (1, adjacents, tete))
	con.commit()#sauvgarde
	list_adjacents=adjacents.split(',')
	set_adjacents=set(list_adjacents)
	set_graphe=set_graphe - set_adjacents
	niv=1
	while(len(list_adjacents)>0):
		#insert dans les autres niveaux:
		set_groupe=set()
		niv=niv+1
		for k in list_adjacents:
			k=k.strip("'")
			print("k: ", k)
			cur.execute("select adjacents from graphe1 where sommet=?", (k,))
			ligne = cur.fetchone()
			adjacents_k=ligne[0]
			list_adjacents_k=adjacents_k.split(',')
			set_adjacents_k=set(list_adjacents_k)
			set_adjacents_k=set_adjacents_k & set_graphe#? set_adjacents_k:sql(46) set_graphe:le graphe1
			set_groupe=set_groupe | set_adjacents_k
			set_graphe=set_graphe - set_groupe
			taille=len(set_graphe)
			if (taille==0):
				break
		t_set_groupe=len(set_groupe)
		if (t_set_groupe==0):
			break
		else:
			list_groupe=list(set_groupe)
			list_groupe.sort()
			list_adjacents=list_groupe#????
			groupe=",".join(list_groupe)
			cur.execute("insert into arbre1 (niveau, sommets, tete) values (?, ?, ?)", (niv, groupe, tete))
			con.commit()#sauvgarde
######################################################
# passer a 5_label1.py
con.close()#fermer data base
cmd = '5_label1.py'
os.system("cls")#effacer l'ecran
os.startfile(cmd)