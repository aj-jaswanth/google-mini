############################################################################################################################################################
#	INFORMATION:-
#		Project		: Google Mini
#		Written by	: UVJ, RGU IIIT RK Valley
#		Compatibility	: Works on all linux hosts having python 2.x
#		RAM Size	: Occupies 11.5 MB during running
#	INTRO:-
#		Using this you can run both terminal and web server interface for your mini-google search engine. This builds HTML pages automatically and #               sends it to the client.
#	CONTACT:-
#		Send your suggestions and comments to aj.jaswanth@gmail.com
import time,os
os.system('clear')
print 'Welcome to Google Search Engine'.center(150),'\v'
time.sleep(1)
os.system('clear')
#Function to build inverted index.
def crawler_initiate():
	print "Initiating Search engine Crawler....".center(150),'\v\v\v\v'
	f=open('Data/list.txt')
	w=str.split(f.read())
	f.close()
	def tor(n):
		c=''
		for x in n:
			t=ord(x)
			if t>63 and t<92 or t>96 and t<122:
				c=c+x
		return c
	def uniq_words():
		print 'Filtering unique words...'.center(150),'\v\v\v\v'
		uq={}
		for x in w:
			g=open('Data/'+x)
			r=g.read()
			for j in str.split(r):
				uq[str.lower(tor(j))]=''
			g.close()
		print 'Filtering unique words complete!'.center(150),'\v'
		print '...............Please wait...............'.center(150),'\v\v'
		return uq
	def parser():
		print 'Parsing file data...'.center(150),'\v\v\v\v'
		parsed={}
		for x in w:
			f=open('Data/'+x)
			parsed[x]=[]
			for j in f.readlines():
				s=''
				for k in str.split(j):		
					s=s+' '+str.lower(tor(k))
				if s.strip(' ')!='':
					parsed[x].append(s.strip(' '))
		print 'File data parsed successfully!'.center(150),'\v\v\v\v'
		return parsed
	parse=parser()
	def dream(li,ind):
			if ind==0:
				return li[ind],li[ind+1]
			elif ind==len(li)-1:	
				return li[ind-1],li[ind]
			else:
				return li[ind-1],li[ind],li[ind+1] 	
	def inverted_indexer():
		print 'Building inverted index....'.center(150),'\v\v\v\v'
		main={}
		for x in uniq_words():
			main[x]={'total_count':'','sen_count':{}}
			count=0
			for y in parse:
				main[x]['sen_count'][y]={}
				rt=0
				for z in parse[y]:
					freq=0
					for s in str.split(z):
						if s==x:
							freq+=1
							count+=1
					if freq!=0:
						main[x]['sen_count'][y][rt+1]=[freq,dream(parse[y],rt)]
					rt=rt+1
				main[x]['total_count']=count
		print 'Inverted index built successfully'.center(150),'\v\v\v\v'
		return main
	return inverted_indexer()
#This plays important role. This function contains all definitions for terminal and server interfaces. This also builds HTML pages according to the results.
def display(main):
	def ret(m):
		r={}
		for x in m:
			if len(m[x])!=0:
				r[x]=m[x]
		return r
	def rev(d,k):
		for x in d:
			if d[x]==k:
				del d[x]
				return x
				break
	def terminal_extract(n):
		r=main[n]
		c=r['total_count']
		sen=ret(r['sen_count'])
		sent={}
		sen_freq={}
		for x in sen.keys():
			f=sen[x].keys()
			sen_freq[x]={}
			sent[x]={}
			for j in f:
				mr=sen[x][j]
				sen_freq[x][j]=mr[0]
				sent[x][j]=mr[1]
		f=list(sen)
		g={}
		for x in f:
			g[x]=len(sen[x])
		print str('Search results for '+n).center(150,'-'),'\v'
		rank=1
		print str('Total count : '+str(c)).center(100)
		for k in list(reversed(sorted(g.values()))):
			q=rev(g,k)
			print q.center(53),'--Rank',rank
			rank+=1
			print 'line \t  frequency'.center(100)
			print ' ----     ---------'.center(100)
			for x in sen_freq[q]:
				print str(str(x)+'\t'+str(sen_freq[q][x])).center(100)	
				#print str('Sentece: \v'+str(sent[q][x],)),'\v'
	def terminal_suggest(n,main):
		print 'Suggestions : '
		for x in main:
			if len(x)>len(n):
				for j in range(len(x)):
					if x[j:len(n)+j]==n:
						print x
	def terminal():
		os.system('clear')
		print 'Welcome to Google Search Engine'.center(150)
		print '-----------------------------------'.center(150),'\v'
		#print 'Time took for building inverted index '+str(time.time()-t1)+' Seconds'
		while True:
			try:
				print 'Type q to quit the program!\n'
				n=str.lower(raw_input('Enter your search string : '))
				os.system('clear')
				if n=='q':
					break
				elif main.has_key(n):
					terminal_extract(n)
				else:
					terminal_suggest(n,main)
			except:
				print 'System error! Try again!'
	def browser():
		def server_suggest(n,main):
			f=open('HTML/sugg_temp.html')
			c=f.read()
			f.close()
			c=c+'<center><font face=waree color=blue size=5>Google Search results for<i> '+n+'</i></center>'
			c=c+"<h3><font color=red>Search string <i>"+n+"</i> not found!</font><h3><h4>Suggestions : </h4><ul>"
			for x in main:
				if len(x)>len(n):
					for j in range(len(x)):
						if x[j:len(n)+j]==n:
							c=c+'<li><a href='+x+'>'+x+'</a></li>'
			return c+'</ul></body></html>'
		def server_extract(n):
			tc=time.time()
			r=main[n]
			c=r['total_count']
			sen=ret(r['sen_count'])
			sent={}
			sen_freq={}
			for x in sen.keys():
				f=sen[x].keys()
				sen_freq[x]={}
				sent[x]={}
				for j in f:
					mr=sen[x][j]
					sen_freq[x][j]=mr[0]
					sent[x][j]=mr[1]
			f=list(sen)
			g={}
			for x in f:
				g[x]=len(sen[x])
			c=''
			f=open('HTML/res_temp.html')
			c=c+f.read()+'<center><font face=waree color=red size=4>Server time : '+time.ctime()+'</font></center>'
			c=c+'<center><font face=waree color=blue size=5>Google Search results for<i> '+n+'</i></font><font color=violet size=2>---------Time took for searching : '+str(time.time()-tc)+'</font></center>'
			rank=1
			for k in list(reversed(sorted(g.values()))):
				q=rev(g,k)
				c=c+'<h3><center><font color=red>'+q+'-----Rank---'+str(rank)+'</font></center></h3>'
				#print q.center(53),'--Rank',rank
				rank+=1
				c=c+'<center><font color=blue><b>Line___________________Frequency</b></font></center>'
				#print 'line \t  frequency'.center(100)
				#print ' ----     ---------'.center(100)
				for x in sen_freq[q]:
					c=c+'<center><font color=violet face=waree size=2>'+str(x)+'___________________________'+str(sen_freq[q][x])+'</font></center>'
					#print str(str(x)+'\t'+str(sen_freq[q][x])).center(100)
					c=c+"<h5><font color=green>"+str(sent[q][x]).strip(')(')+"</font><h5>"	
					#print str('Sentece: \v'+str(sent[q][x],)),'\v'
			return c
		def html_gen(n):
			if n in main:
				return server_extract(n)
			else:
				return server_suggest(n,main)
		def server():
			print 'Starting server..'
			import socket, random
			s=socket.socket()
			ip=raw_input("Enter your system ip : ")
			while True:
				try:
					port=input('Enter port : ')
					s.bind((ip,port))
					break
				except:
					print 'Port already in use!'	
			s.listen(50)
			def logo():
				w=os.listdir('Images/Doodles')
				f=open('Images/Doodles/'+w[random.randint(0,len(w)-1)])
				return f.read()
				f.close()
			print 'Running server on',ip,':',port
			f=open('HTML/home_page.html')
			home=f.read()
			fav=open('Images/favicon.jpeg')
			favc=fav.read()
			fav.close()
			f.close()
			f=open('Images/Background.jpg')
			bg=f.read()
			f.close()
			while True:
				try:
					c,addr=s.accept()
					print 'Got connection from : ',addr
					req=str.split(c.recv(1024))[1]
					print 'Requested : ',req[1:]
					if req[1:]=='logo.jpg':
						c.send(logo())
					elif req[1:]=='':
						c.send(home)
					elif req[1:]=='favicon.jpeg':
						c.send(favc)
					#elif req[1:]=='Background.jpg':
					#	c.send(bg)
					else:
						c.send(html_gen(req[1:]))
					c.close()
				except:
					ce=raw_input('\nWhat do you want?\n1.Change interface\n2.Quit!\n ')
					if ce=='1':
						switch()
					else:
						exit()
		server()
	def switch():
		inf=raw_input('Enter your display interface [1/2] : \n1.Terminal\n2.Start server\n3.Quit!\n')
		if inf=='1':
			print 'Starting terminal..'		
			terminal()
		elif inf=='2':
			browser()
		else:
			exit()
	switch()
t1=time.time()
display(crawler_initiate())
