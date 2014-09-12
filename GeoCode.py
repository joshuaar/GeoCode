import urllib2, urllib, json, time, argparse
import os, sys

def readResultJSON(handle):
	return [json.loads(i) for i in handle]
	

class BatchGeoCode(object):

	def __init__(self,ghlist,jsondump,limit=2500,skipfile=".skip.txt"):
		self.count = 0
		self.limit = limit
		self.__SKIPFILE = skipfile
		self.ghlist = open(ghlist)
		self.jsondump = jsondump
		if os.path.exists(self.__SKIPFILE):
			with open(self.__SKIPFILE,"r") as f:
				self.SKIP = int(f.read())
		else:
			with open(self.__SKIPFILE,"w") as f:
				f.write(str(0))
				self.SKIP = 0
		for i in range(self.SKIP):
			self.ghlist.next()

	def dumpjson(self,dct):
		jsondump = open(self.jsondump,"a")
		res_str = json.dumps(dct,jsondump)
		jsondump.write(res_str+"\n")
		jsondump.close()
		

	def request10(self):
		"next 10 addresses for google"
		#dont exceed the daily limit
		if self.count + 10 > self.limit:
			self.count += 10
			return
		#else get next 10 geocodes and write them out
		next10_res = []
		for i in range(10):
			try:
				nxt = self.ghlist.next().replace("\n","")
				nxt_encoded = self.qsEncode(nxt)
				nxt_res=json.load(urllib2.urlopen(nxt_encoded))
				nxt_res["query"] = nxt
				next10_res.append(nxt_res)
			except StopIteration:
				pass
		#incriment place-counters
		self.SKIP += len(next10_res)
		self.count += len(next10_res)

		self.writeSkip()	
		return next10_res

	def get10(self):
		next10_res = self.request10()		
		for i in next10_res:
			self.dumpjson(i)

	def getlimit(self):
		while self.count < self.limit:
			print "getting {0}".format(self.SKIP)
			self.get10()
			time.sleep(2)
			
	def writeSkip(self):
		with open(self.__SKIPFILE,"w") as f:
			f.write(str(self.SKIP))

	def setSkip(self,value):
		self.SKIP = value

	def qsEncode(self,address):
		return "https://maps.googleapis.com/maps/api/geocode/json?"+urllib.urlencode({"address":address})

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("ghlist", type = str)
	parser.add_argument("-j","--jsdump", type = str, required=True)
	parser.add_argument("-l","--limit", type = int)
	parser.add_argument("-p","--parse", action="store_true")
	parser.add_argument("-s","--skip", type = str, default=".skip.txt")
	args = parser.parse_args()
	if args.parse:
		with open(args.jsdump) as f:
			for j in readResultJSON(f):
				print j
		sys.exit(0)
	ghGrabber = BatchGeoCode(args.ghlist,args.jsdump,args.skip)
	if args.limit:
		ghGrabber.limit = args.limit
	ghGrabber.getlimit()
