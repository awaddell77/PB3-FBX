#verifies upc-13
#btest = '036000291452' #valid
#btest = '088109110642'#invalid
def verify_bcode(bcode):
	bcode = str(bcode).zfill(12)
	ch_dig = int(bcode[11])
	odd_sum =0
	even_sum = 0
	for i in range(0,11,2):
		#print(bcode[i],'+', end=' ')
		odd_sum += int(bcode[i])
	res = odd_sum*3
	#print(res)

	for i in range(1, 11,2):
		#print(bcode[i], ' ', end=' ')
		even_sum += int(bcode[i])
	res += even_sum
	end_res = res % 10 
	if end_res != 0: end_res = 10 - end_res
	if end_res == ch_dig: return 1
	return 0
#verify_bcode(btest)


def expand_bcode(bcode):
	#fills it to 12 characters, takes only 8
	ch_dig = str(bcode)[-1]
	bcode = str(bcode).zfill(12)[:11]
	s_bcode = bcode[4:]
	lst=[]

	for s in s_bcode: lst.extend(s) 
	print(lst)
	print(s_bcode)
	bcode1, bcode2 = s_bcode[:4], s_bcode[4:]
	temp1 = bcode1[-1]

	temp2, temp3 = bcode2[0], bcode2[2]

	t = lst[6]
	t1 = lst[4]
	t2 = lst[3]
	t3 = lst[5]
	lst[3] = t1
	lst[4] = t2
	lst[5] = t
	lst[6] = t3
	print(lst[:4]) #should be 0282
	print(lst[4:])
	lst = lst[:4] + ['0', '0', '0', '0'] + lst[4:]
	lst.extend(str(ch_dig))
	
	#print(bcode1)
	#print(bcode2)
	#print(bcode1[-1])
	#print(bcode2[0], ' ', bcode2[2])
	#end1, end2 = bcode1[-1], bcode2[-1]
	#n_bcode = s_bcode[:3] + end2 + '0'*4 + end1 + s_bcode[5:]
	return ''.join(lst)


