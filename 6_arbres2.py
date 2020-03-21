import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("6_arbres2")
print(100*"~")
#sommet et adjacents de graphe2:
cur.execute("select sommet, adjacents from graphe2 where fait='non' limit 0 , 1")
ligne = cur.fetchone()
sommet=ligne[0]
adjacents=ligne[1]
print("le sommet de depart est: ", sommet ," a suivre.....")
#-------------------------------------------------------------------------------------------------------------------------
#liste des sommets de graphe2
set_graphe=set()
cur.execute("select sommet from graphe2")
ligne = cur.fetchall()
for a in ligne:
	sommet_a=a[0]
	set_graphe.add(sommet_a)
#print("set_graphe22: ",set_graphe)
#insert dans niveau0:
cur.execute("insert into arbre2 (niveau, sommets, tete) values (?, ?, ?)", (0, sommet, sommet))
con.commit()#sauvgarde
set_graphe.remove(sommet)
#print("set_graphe27(sommet): ",set_graphe)
#insert dans niveau1:
cur.execute("insert into arbre2 (niveau, sommets, tete) values (?, ?, ?)", (1, adjacents, sommet))
con.commit()#sauvgarde
#print("adjacents: ",adjacents)
list_adjacents=adjacents.split(',')
#print("list_adjacents: ",list_adjacents)
set_adjacents=set(list_adjacents)
# convert chaque element de set_adjacents en integer @@@important@@@
set_adjacents = set(map(int, set_adjacents))
set_graphe=set_graphe - set_adjacents
#print("set_adjacents: ",set_adjacents)
#print("set_graphe(apres niv1): ",set_graphe)
niv=1
taille=len(set_graphe)
#insert dans les autres niveaux:
while(taille>0):
	set_groupe=set()
	niv=niv+1
	tete=sommet
	for k in list_adjacents:
		k=k.strip("'")
		#print("k: ", k)
		cur.execute("select adjacents from graphe2 where sommet=?", (k,))
		ligne = cur.fetchone()
		adjacents_k=ligne[0]
		#print("adjacents_k:", adjacents_k)
		list_adjacents_k=adjacents_k.split(',')
		#print("list_adjacents_k: ",list_adjacents_k)
		set_adjacents_k=set(list_adjacents_k)
		# convert chaque element de set_adjacents_k en integer @@@important@@@
		set_adjacents_k = set(map(int, set_adjacents_k))
		set_adjacents_k=set_adjacents_k & set_graphe
		#print("set_adjacents_k(&): ",set_adjacents_k)
		set_groupe=set_groupe | set_adjacents_k
		#print("set_groupe: ",set_groupe)
		set_graphe=set_graphe - set_groupe
		#print("set_graphe: ",set_graphe)
		taille=len(set_graphe)
		#print("taille de set_graphe:", taille)
		if (taille==0):
			break
		#print(35*"+-")
	t_set_groupe=len(set_groupe)
	if (t_set_groupe==0):
		break
	else:
		list_groupe=list(set_groupe)
		list_groupe.sort()
		# convert chaque element de list_groupe en string @@@important@@@
		list_groupe = set(map(str, list_groupe))
		list_adjacents=list_groupe
		groupe=",".join(list_groupe)
		cur.execute("insert into arbre2 (niveau, sommets, tete) values (?, ?, ?)", (niv, groupe, tete))
		con.commit()#sauvgarde
		#print("taille71",taille)
		#print(60*"#")
#comparer les deux arbres:
#pour arbre2
cur.execute("select max(niveau) from arbre2")
ligne = cur.fetchone()
max2=ligne[0]
#pour arbre1
#tete de arbre1
cur.execute("select distinct tete from arbre1")
lignes = cur.fetchall()
list_tete=[]
for t in lignes:
	tete_t=t[0]
	cur.execute("select max(niveau) from arbre1 where tete=?", (tete_t,))
	ligne_t = cur.fetchone()
	max1_t=ligne_t[0]
	if(max1_t==max2):
		list_tete.append(tete_t)
if(len(list_tete)>0):
	#list_tete dans fichier de texte
	# convert chaque element de list_tete en string @@@important@@@
	list_tete = set(map(str, list_tete))
	tete_ch=",".join(list_tete)
	fichier = open("tetes.txt", "w")
	fichier.write(tete_ch)
	fichier.close()
	# passer a 7_avant_label2.py
	cmd = '7_avant_label2.py'
	os.system("cls")#effacer l'ecran
else:
	#delete arbre2
	cur.execute("DELETE FROM arbre2")
	cur.execute("delete from sqlite_sequence where name='arbre2'")# pour id=1
	con.commit()# Sauvgarde
	#fait='oui' dans graphe2
	cur.execute("update graphe2 set fait='oui' where sommet=?", (sommet,))
	con.commit()# Sauvgarde
	#recharger la page
	# passer a 6_arbres2.py
	cmd = '6_arbres2.py'
	os.system("cls")#effacer l'ecran
con.close()#fermer data base
os.startfile(cmd)
