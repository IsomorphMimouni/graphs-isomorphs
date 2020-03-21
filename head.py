#coding:utf-8
"""auteur: Mohamed Mimouni
mimouni.mohamed@gmail.com 2019

/************************ Licence **************************
programme isomorphes des graphes polynomial
GI_polynomial application
version: 1.3
mail: mimouni.mohamed@gmail.com
date fin de programation: 2019-04-08 05:00
---------------------------------------------------------------------------
Copyright (c) 2009_2019 mohamed mimouni.
Ce programme est un logiciel libre ; vous pouvez le redistribuer et/ou le
modifier conformément aux dispositions de la Licence Publique Générale GNU,
telle que publiée par la Free Software Foundation ; version 3 de la licence, ou
encore (à votre choix) toute version ultérieure.

Ce programme est distribué dans l'espoir qu'il sera utile, mais SANS AUCUNE
GARANTIE ; sans même la garantie implicite de COMMERCIALISATION ou D'ADAPTATION
A UN OBJET PARTICULIER. Pour plus de détail, voir la Licence Publique Générale
GNU .

Vous devez avoir reçu un exemplaire de la Licence Publique Générale GNU en même
temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software
Foundation Inc., 675 Mass Ave, Cambridge, MA 02139, Etats-Unis.
---------------------------------------------------------------------------
**************************************************/
"""
#*****************************************
import sqlite3
import os
#*****************************************
con = sqlite3.connect('isom_4140_04.db')
cur = con.cursor()
#*****************************************

myfichier1="instances/cfi-rigid-d3/cfi-rigid-d3-0180-01-1"
myfichier2="instances/cfi-rigid-d3/cfi-rigid-d3-0180-01-2"
# si le fichier commence par des lignes descriptions il faut donner le numero de arrets...defaut lignedebut=1
lignedebut=1