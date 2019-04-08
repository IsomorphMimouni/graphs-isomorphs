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
con.close()#fermer data base
#eteindre pc:	os.system ('shutdown /s /t 10')