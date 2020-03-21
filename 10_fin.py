import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("10_fin")
print(30*"~")
#generer un fichier solution
filename='solutions.txt'
#par defaut:non
#les solutions:
cur.execute("select count(id) from solutions")
ligne = cur.fetchone()
cnt=ligne[0]
if(cnt==0):
	text_corct="Les deux graphes ne sont pas isomorphes!"
else:
	#-------------------vider solutions-----------------------
	cur.execute("DELETE from solutions")
	cur.execute("delete from sqlite_sequence where name='from solutions'")# pour id=1
	#tete
	cur.execute("select tete from arbre2 limit 0, 1")
	ligne = cur.fetchone()
	tete_actuel=ligne[0]
	#-------------------insertion solutions-----------------------
	cur.execute("select sommet, etiquette from labels1 order by sommet")
	lignes = cur.fetchall()
	for lb in lignes:
		solution_sommet=lb[0]
		solution_etiquette=lb[1]
		print(solution_sommet,":",solution_etiquette)
		#chercher dans labels2:
		cur.execute("select sommet from labels2 where etiquette=?",(solution_etiquette,))
		lignes = cur.fetchall()
		list_image=[]
		for img in lignes:
			somet=img[0]
			list_image.append(somet)
		list_image.sort()
		# convert chaque element de list_image en string @@@important@@@
		list_image = list(map(str, list_image))
		str_image=",".join(list_image)
		cur.execute("insert into solutions (sommet, images, tete) values (?, ?, ?)", (solution_sommet, str_image, tete_actuel))
		con.commit()#sauvgarde
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
		text_corct=text_corct+sommet+"="+images+"\n"
print(text_corct)
fichier = open(filename, "w")
fichier.write(text_corct)
fichier.close()
con.close()#fermer data base
#eteindre pc:#os.system ('shutdown /s /t 10')