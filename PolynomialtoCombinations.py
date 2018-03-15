from itertools import combinations, permutations
from copy import deepcopy 
x = input("Put your polynomial here friend (copied from mathematica, note that you may have to paste into a text file and adjust so its all one line with only \' + \' between terms'):")
# example of form: "x[1]^3 + x[1]^4 + x[1]^5 + x[1]^6 + x[1]^2 x[2] + 2 x[1]^3 x[2] + 3 x[1]^4 x[2] + x[1] x[2]^2 + 3 x[1]^2 x[2]^2 + x[2]^3"
#evidently there is a bijection between what is produced here and an eqivalence class of tabloids
#defined by two tabloids p_1, p_2 being equivalent if rows of p_1 can be rearraged such that p_1=p_2 
varsi = x.split(" + ")
coeffs = list()
nums = list()
parts = list()
exps = list()
for part in varsi:	#this deconstructs the input polynomial into four lists, this allows us to keep track of the 
	a = 0			#coefficents, the exponent that corresponds to each subscript, and the sum of the terms
	coeff = 1    	#subscript * exponent of that variable since this gives us the size of the overall diagram
	cur = ""
	while part[a] != 'x':
		if part[a] != ' ':
			cur += part[a]
		a +=1
	if cur != '':
		coeff = int(cur)
		cur = ''
	totnum = 0
	totexp = 0
	totparts = 0
	toteexp = list()
	toteparts = list()
	while a < len(part):
		cur = ''
		thisexp = 1
		thisterm = 0
		a += 2
		while part[a] != ']':
			cur += part[a]
			a += 1
		thisterm = int(cur)
		a +=1
		cur = ""
		if a < len(part) and part[a] == '^':
			a += 1
			while a < len(part) and part[a] != ' ':
				cur += part[a]
				a +=1
			thisexp *= int(cur)
		a += 1
		toteexp.append(thisexp)
		toteparts.append(thisterm)
		totnum += thisexp * thisterm
	coeffs.append(coeff)
	parts.append(toteparts)
	nums.append(totnum)
	exps.append(toteexp)
	toteexp

#note alist is redundant, I could have just used alistre with baselist as a parameter
#alist is the initial call it will return a set of combinations
#these combinations will be such that if we have a term p such that $x[n]^m|p$ then we would expect
#there to be atleast m n-sized sets in the returned combination.
def alist(n,p,e,o): #takes a terms total order, parts, exponents, and the number of combinations needed (coefficient)
	curo = o
	baselist = list()
	thislist = list()
	for i in range(1,n+1):
		baselist.append(i)
	sets = getsubsets(p[0],e[0],baselist,o) #get all subsets, this just gives all possible subsets
	alllists = list()
	for j in sets: #call recursion on all subsets
		jprefix = list()
		compset = list()	#flat set with elements
		if e[0] > 1:
			for k in range(e[0]): #obtain set we will remove
				curlook = j[k]
				jprefix.append(j[k])
				for l in range(p[0]):
					compset.append(int(curlook[l]))
		if e[0] ==1:
			curlook = j[0]
			jprefix.append(j)
			for l in range(p[0]):
					compset.append(int(curlook[l]))
		newlist = [val for val in baselist if val not in compset]
		newp = list()
		newe = list()
		newn = n
		for l in range(1,len(e)):
			newp.append(p[l])
			newe.append(e[l])
		jprefixlist = list()
		if len(p) != 1:	
			suffixes = alistre(newn,newp,newe,curo,newlist) #recursive call
			for l in suffixes:			#go through all the suffixes
				elementt = deepcopy(jprefix)
				for k in l:				#go through and add this suffix list
					elementt.append(k)
				jprefixlist.append(elementt)
			for l in jprefixlist:
				alllists.append(l)
				thislist.append(l)
				curo -= 1       # if we append it means we found a combination so we decrement curo
				if curo == 0:
					return alllists
		if len(p) == 1:
			alllists.append(jprefix)
			thislist.append(jprefix)
			curo -= 1       # if we curoppend it means we found a combination so we decrement curo
			if curo == 0:
				return alllists
	counte = 0
	for i in range(curo):
		alllists.append(thislist[counte])
		counte +=1 
		counte = counte % len(thislist)
	return alllists #this cant happen with valid input, thus empty set return value means failure


def alistre(n,p,e,o,curlist):
	curo = o
	sets = getsubsets(p[0],e[0],curlist,o) #get all subsets
	alllists = list()
	for j in sets: #call recursion on all subsets
		jprefix = list()
		compset = list()	#flat set with elements
		if e[0] > 1:
			for k in range(e[0]): #obtain set we will remove
				curlook = j[k]
				jprefix.append(j[k])
				for l in range(p[0]):
					compset.append(int(curlook[l]))
		if e[0] ==1:
			curlook = j[0]
			jprefix.append(j)
			for l in range(p[0]):
					compset.append(int(curlook[l]))
		newlist = [val for val in curlist if val not in compset]
		newp = list()
		newe = list()
		newn = n
		for l in range(1,len(e)):
			newp.append(p[l])
			newe.append(e[l])
		jprefixlist = list()
		if len(p) != 1:
			suffixes = alistre(newn,newp,newe,curo,newlist) #recursive call
			for l in suffixes:			#go through all the suffixes
				elementt = deepcopy(jprefix)
				for k in l:				#go through and add this suffix list
					elementt.append(k)
				jprefixlist.append(elementt)
			#print(jprefixlist)
			for l in jprefixlist:
				alllists.append(l)
				curo -= 1       # if we append it means we found a combination so we decrement curo
				if curo == 0:
					return alllists
		if len(p) == 1:
			alllists.append(jprefix)
			curo -= 1       # if we append it means we found a combination so we decrement curo
			if curo == 0:
				return alllists
	return alllists #this cant happen with valid input, thus empty set return value means failure


def shouldcheck(b, c, i,e): #check if a parition is at the further it can go
	return (b) == (c-e+i+1)

#getsubsets takes a part, an exponent, an allowed list, an the number of combinations we still need to find
#I am not excited to see the speed of this
# Hopefully keeping track of the number of combinations that are remaining to find will cut down on this
def getsubsets(p, e, remlist, o):
	stringy = ''					#not doing anything with o right now, but one could use it as a
	for i in remlist:				#limiter if they are looking for particularly large combinations
		stringy += str(i)
	combostemp = list(combinations(stringy,p))
	combos = list() #this whole portion is probably uneeded, just converting 	
	for i in range(len(combostemp)):  #from tuples to lists
		elem = list()
		for j in range(p):
			elem.append(combostemp[i][j])
		combos.append(elem)
	subsets = list() 
	indexcount = list()		#keeps track of current index
	indexcount.append(0)
	for i in range(1,e):
		indexcount.append(i)
	while indexcount[0] < len(combos)-e+1: #go through to get all
		cur = list()			#possible combinations
		for j in range(e):
			cur.append(combos[indexcount[j]])
		distinct = True
		for i in range(e):
			for j in range(i+1,e):
				intersec = [val for val in cur[i] if val in cur[j]]
				if intersec != []:
					distinct = False
		if distinct == True:
			addition = list()
			for j in range(e):	#combines valid combination into a single element
				addition.append(cur[j])
			subsets.append(addition)
		pre = True
		indexcount[e-1] += 1
		for i in reversed(range(0,e)): #increment locaton to the next e tuple of p-tuples
			if pre: 
				if i > 0:
					if shouldcheck(indexcount[i], len(combos), i,e): #checks and adjusts if index is out of bounds
						indexcount[i-1] += 1  #and adjusts accordingly 
						for j in range(i,e):
							indexcount[j] = indexcount[i-1] + j-i+1
					else:
						pre = False

	return subsets

masslist = list()
for i in range(len(exps)):
	currentl = alist(nums[i],parts[i],exps[i],coeffs[i])
	for j in currentl:
		masslist.append(j)
fixedlist = list()	#will contain a reformatted list fixes all formatting issues except singletons
for i in masslist:	
	fixedsublist = list()
	for j in i:
		if len(j[0]) > len(j): #is an issue with the formatting , but this fixes that issue
			fixedsublist.append(j[0])	#issue is a single list is always double nested 
		else:
			fixedsublist.append(j)
	fixedlist.append(fixedsublist)
a = str(fixedlist)
b = a.replace("[", "{")
c = b.replace("]", "}")
d = c.replace("\'","")
e = d
for i in range(1,11):
	e = e.replace("{{"+str(i)+"}}","{"+str(i)+"}") #covers double nested singleton cases 

print(e)

code = open("mathematicalist.txt","w")
code.write(e)
code.close()