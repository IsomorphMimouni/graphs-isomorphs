import head
cur=head.cur
con=head.con
os=head.os
#fichier graphe2
print("3_adjacents2.py")
print(30*".")
fichier = open(head.myfichier2, "r")
set_graphe=set()
for line in fichier:
	arete=line.split(' ')#explode php
	a=arete[1]
	b=arete[2]
	b=b.strip()
	set_graphe.add(a)
	set_graphe.add(b)
	#insert aretes
	cur.execute("insert into aretes2 (a, b) values (?, ?)", (a, b))
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
	print(i,":",k)
	# les adjacents avant de sommet k: b=k
	cur.execute("select a from aretes2 where b=?", (k,))
	avant = cur.fetchall()
	avant=str(avant).strip("[]")
	avant=str(avant).strip("()")
	avant=str(avant).strip(",")
	avant=str(avant).split("',), ('")
	avant=','.join(avant)
	avant=avant.strip("'")
	#print("avant(join): ",avant)
	# les adjacents apres de sommet k: a=k
	cur.execute("select b from aretes2 where a=?", (k,))
	apres = cur.fetchall()
	apres=str(apres).strip("[]")
	apres=str(apres).strip("()")
	apres=str(apres).strip(",")
	apres=str(apres).split("',), ('")
	apres=','.join(apres)
	apres=apres.strip("'")
	#print("apres(join): ",apres)
	#insert graphe2 table
	adj=avant+','+apres
	adj=str(adj).strip(',')
	#print("adj: ",adj)
	list_adj=adj.split(',')
	set_adj=set(list_adj)
	list_adj=list(set_adj)
	list_adj.sort()
	adj=','.join(list_adj)
	cur.execute("insert into graphe2 (sommet, adjacents) values (?, ?)", (k, adj))
	i=i+1
# Sauvgarde
con.commit()
# Sauvgarde acomplit
#-------------------vider aretes-----------------------
cur.execute("DELETE FROM aretes2")
cur.execute("delete from sqlite_sequence where name='aretes2'")# pour id=1
# Sauvgarde
con.commit()
con.close()#fermer data base
#-------------------------------------------------------------------------------------------------------------------------
cmd = '4_arbres1.py'
os.startfile(cmd)