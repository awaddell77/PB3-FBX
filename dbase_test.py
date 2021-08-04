from Dbase_man import *
from Dictify import *
from Dict_lst import *
from loadJson import *
from verify_bcode import *
import time
'''
conn_str = (
    r'Driver={ODBC Driver 17 for SQL Server};'  # Just an Example (SQL2008-2018)
    r'Server=localhost;' # Here you insert you servername
    r'Database=master;' # Here you insert your db Name
    r'Trusted_Connection=yes;' # This flag enables windows authentication
    )
    '''
creds = loadJson('credentials.json')

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"  # Just an Example (SQL2008-2018)
    +"Server={0};".format(creds['server']) # Here you insert you servername
    +"Database={0};".format(creds['database']) # Here you insert your db Name
    +"UID={0};".format(creds['username']) # Here you insert the SQL User to auth
    +"PWD={0};".format(creds['password']) # Here you insert the User's password
    )



m_test = Dbase_man(conn_str)
##res = m_test.exec_query("SELECT @@VERSION;")
#print(res)
fname = 'walmart final.csv'
data_res = Dictify(fname).main()
vtab = Dict_lst(data_res)

#print(data_res);

def check_prices_by_barcode(v_data, dlist, dbconn):
	b_count, match_cnt, vmatch_cnt = 0, 0,0
	ItemPckCrit = 'No. Pckg Matches'
	ItemPckName = 'Item Package Name'
	VendorMtch = 'No. Vendor Matches'
	VendorName = 'Vendor Name'
	VendorItemName = 'Vendor Item Name'
	ValidBcode	 = 'Valid Barcode?'


	dlist.add_crit(ItemPckCrit, 0)
	dlist.add_crit(VendorMtch, 0)
	dlist.add_crit(ItemPckName, '')
	dlist.add_crit(VendorName, '')
	dlist.add_crit(VendorItemName, '')
	dlist.add_crit(ValidBcode, 0)

	for i in range(0, len(vtab)):
		trow = vtab.get_index(i)
		bcode = trow['UPC (12 digits) or PLU'].replace('-','')
		trow[ValidBcode] = verify_bcode(bcode.zfill(12))	
		#bcode = vtab.get_index(i)['UPC (12 digits) or PLU']
		vres = dbconn.exec_query("SELECT a.Name, a.OrderNumber , (SELECT b.Name FROM Vendor b WHERE b.VendorID = a.VendorID) FROM VendorItem a WHERE OrderNumber = '{0}'".format(trow['Vendor Order Number']))
		res = dbconn.exec_query("SELECT Name, ItemPkgID, ItemID, Barcode FROM dbo.ItemPkg WHERE Barcode = '{0}' ;".format(bcode.zfill(12)))
		trow['UPC (12 digits) or PLU'] = "|" + bcode.zfill(12)
		vmatch_cnt += len(vres)
		trow[VendorMtch] = len(vres)
		#need to add the name
		if res:
			print("{0} matches {1} item packages".format(bcode, len(res)))
			trow[ItemPckName] = res[0][0]
			trow[ItemPckCrit] += len(res)
			match_cnt += 1

		else: print("{0} matches 0 item packages".format(bcode))
		if vres: trow[VendorName], trow[VendorItemName] = vres[0][2], vres[0][0]


		#print(bcode)
		b_count += 1
	print(b_count)
	print("matches: ", match_cnt)
	print("vmatches: ", vmatch_cnt)
	dbconn.close_conn()


check_prices_by_barcode(vtab, vtab, m_test)
vtab.export([], 'results '+ fname)
#time.sleep(5)