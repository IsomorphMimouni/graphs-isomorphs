import head
import time
start_time = time.time()
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("get_groupe.py")
print(30*"~")
#generer un fichier groupe solutions
filename='gr_solutions.txt'#groupe solutions
fichier = open(filename, "a")
cur.execute("select distinct etiquette from labels1")
lignes = cur.fetchall()
for etq in lignes:
	etiquette=etq[0]
	print(etiquette)
	print(10*"-")
	fichier.write(etiquette+"\n")
	fichier.write(10*"-"+"\n")
	#graph1:
	cur.execute("select sommet from labels1 where etiquette=?",(etiquette,))
	lignes1 = cur.fetchall()
	list1=[]
	for som1 in lignes1:
		list1.append(som1[0])
	list1.sort()
	# convert chaque element de list1 en string @@@important@@@
	list1 = list(map(str, list1))
	str_list1=",".join(list1)
	print(str_list1)
	fichier.write(str_list1+"\n")
	#graph2:
	cur.execute("select sommet from labels2 where etiquette=?",(etiquette,))
	lignes2 = cur.fetchall()
	list2=[]
	for som2 in lignes2:
		list2.append(som2[0])
	list2.sort()
	# convert chaque element de list2 en string @@@important@@@
	list2 = list(map(str, list2))
	str_list2=",".join(list2)
	print(str_list2)
	print(15*"+")
	fichier.write(str_list2+"\n")
	fichier.write(150*"+"+"\n")
fichier.close()