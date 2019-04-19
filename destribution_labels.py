import head
cur=head.cur
con=head.con
os=head.os
#-------------------------------------------------------------------------------------------------------------------------
print("labels destribution")
print(100*"~")
#les labels:
cur.execute("select distinct etiquette from labels1")
lignes = cur.fetchall()
print("labels")
print(10*":")
for img in lignes:
	etiquette=img[0]
	cur.execute("select count(*) from labels1 where etiquette=?", img)
	ligne1 = cur.fetchone()
	cnt1=ligne1[0]
	cur.execute("select count(*) from labels2 where etiquette=?", img)
	ligne2 = cur.fetchone()
	cnt2=ligne2[0]
	print(etiquette,"\t\t",cnt1,"\t",cnt2)
print("labels")
print(10*":")
for img in lignes:
	etiquette=img[0]
	cur.execute("select sommet from labels1 where etiquette=?", img)
	lignes1 = cur.fetchall()
	list_sommets1=[]
	for sm in lignes1:
		smt=sm[0]
		list_sommets1.append(smt)
	cur.execute("select sommet from labels2 where etiquette=?", img)
	lignes2 = cur.fetchall()
	list_sommets2=[]
	for sm in lignes2:
		smt=sm[0]
		list_sommets2.append(smt)
	print(etiquette,)
	print(list_sommets1)
	print(list_sommets2)
input("cliquez pour quiter!!!")