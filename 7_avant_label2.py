import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("7_avant_label2")
print(100*"~")
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#sommet et adjacents de graphe2:
cur.execute("select sommet from graphe2 where fait='non' limit 0 , 1")
ligne = cur.fetchone()
sommet=ligne[0]
#comparer les deux arbres:
#arbre2
cur.execute("select sommets from arbre2")
ligne = cur.fetchall()
list2=[]
for t in ligne:
	sommets=t[0]
	#print(sommets)
	list_sommets=sommets.split(',')
	t2=len(list_sommets)
	list2.append(t2)
#recuperer les tetes de graphe1 dont les max sont egaux avec max niveau de graphe2
fichier = open("tetes.txt", "r")
a=fichier.readline()
fichier.close()
list_a=a.split(',')
#arbre1
etat=False
for a_l in list_a:
	cur.execute("select sommets from arbre1 where tete=?", (a_l,))
	ligne = cur.fetchall()
	list1=[]
	for t in ligne:
		sommets=t[0]
		#print(sommets)
		list_sommets=sommets.split(',')
		t1=len(list_sommets)
		list1.append(t1)
	if (list1==list2):
		etat=True
		break
if (etat):
	print("les deux lists sont egaux")
	print("aller calculer les etiquettes ou labels!!!")
	# passer a 8_label2.py
	cmd = '8_label2.py'
	os.system("cls")#effacer l'ecran
else:
	print("les deux lists sont deferent")
	#tete2
	cur.execute("select sommets from arbre2 where niveau=0")
	ligne = cur.fetchone()
	sommet=ligne[0]
	#delete arbre2
	cur.execute("DELETE FROM arbre2")
	cur.execute("delete from sqlite_sequence where name='arbre2'")# pour id=1
	#delete solutions:	cur.execute("DELETE FROM solutions where tete=?", (tete,)) ???pourqoui vider solutions??????
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
os.startfile(cmd)