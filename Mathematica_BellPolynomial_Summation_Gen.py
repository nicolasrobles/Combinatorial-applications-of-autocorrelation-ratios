from copy import deepcopy 
#This generates mathematica code to produce the bell polynomial product sum as shown on page 15

K = input("Input k value:")	#With respect to the paper, this value represents k
d = input("Input d value:")	# With respect to the paper this value is d
K = int(K)
d = int(d)
megalist = list()
def getexplist(k, lis):#builds us all weak k composition with d parts
	if k == K:
		for i in range(d):
			lis.append(0)
	if k == 0:
		if lis not in megalist:
			megalist.append(lis)
		return []
	for i in range(d):
		l = deepcopy(lis)
		l[i] += 1
		getexplist((k-1), l)		
	return []



getexplist(K, [])

print(megalist)
filling = list()	#
terms = list()
filling.append("x[1]")
code = ''
for i in range(1,d):	#prints out the Mathematica code to obtain the polynomial. Plugging this into mathematica gives 
	addition = filling[i-1] + ", " + "x[" + str((i+1)) + "]" #the desired polynomial
	filling.append(addition)
for i in range(d):
	terms.append("(\!\(\n\*UnderoverscriptBox[\(\[Sum]\), \(k = 1\), \("+str((i+1))+"\)]\(BellY["+str((i+1))+", k, {"+filling[i]+"}]\)\))") #need to add x[1]+...
outp = "Expand[ " + str(K) + "! * Expand[ "
for i in range(len(megalist)):
	thisone = ""
	if i != 0:
		thisone = "+ "
	for j in range(d):
		thisone += terms[j] + "^" + str((megalist[i])[j]) +"/" + str((megalist[i])[j]) + "! "
	outp += thisone
outp += "] ]"
print(outp)

code = open("mathematicamollificationpoly.txt","w") #writes the polynomial to specified text file.
code.write(outp)
code.close()