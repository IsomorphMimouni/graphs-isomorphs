import head
cur=head.cur
con=head.con
os=head.os
#fichier graphe1
print("2_adjacents1.py")
print(30*".")
fichier = open(head.myfichier1, "r")
set_graphe=set()
for line in fichier:
	arete=line.split(' ')#explode php
	a=arete[1]
	b=arete[2]
	b=b.strip()
	set_graphe.add(a)
	set_graphe.add(b)
	#insert aretes
	cur.execute("insert into aretes1 (a, b) values (?, ?)", (a, b))
# Sauvgarde
con.commit()
#fermer le fichier
fichier.close()
#print(set_graphe)
#------------------------------------------
i=1
list_graphe=list(set_graphe)
list_graphe.sort()
for k in list_graphe:
	# les adjacents avant de sommet k: b=k
	cur.execute("select a from aretes1 where b=?", (k,))
	avant = cur.fetchall()
	avant=str(avant).strip("[]")
	avant=str(avant).strip("()")
	avant=str(avant).strip(",")
	avant=str(avant).split("',), ('")
	avant=','.join(avant)
	avant=avant.strip("'")
		# les adjacents apres de sommet k: a=k
	cur.execute("select b from aretes1 where a=?", (k,))
	apres = cur.fetchall()
	apres=str(apres).strip("[]")
	apres=str(apres).strip("()")
	apres=str(apres).strip(",")
	apres=str(apres).split("',), ('")
	apres=','.join(apres)
	print(i,":",k)#,"=>",avant,"|",apres)
	#print(50*"-")
	apres=apres.strip("'")
	#insert graphe1 table
	adj=avant+','+apres
	adj=str(adj).strip(',')
	#print("adj: ",adj)
	list_adj=adj.split(',')
	set_adj=set(list_adj)
	list_adj=list(set_adj)
	list_adj.sort()
	adj=','.join(list_adj)
	cur.execute("insert into graphe1 (sommet, adjacents) values (?, ?)", (k, adj))
	i=i+1
# Sauvgarde
con.commit()
# Sauvgarde acomplit
#-------------------vider aretes-----------------------
cur.execute("DELETE FROM aretes1")
cur.execute("delete from sqlite_sequence where name='aretes1'")# pour id=1
# Sauvgarde
con.commit()
con.close()#fermer data base
#-------------------------------------------------------------------------------------------------------------------------
# passer a 3_adjacents2.py
cmd = '3_adjacents2.py'
os.startfile(cmd)