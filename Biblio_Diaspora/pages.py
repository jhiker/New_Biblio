import time, re, calendar

months = tuple([calendar.month_name[m] for m in range(12)])

institutions= ['Publisher','Lending Library (Public)','Lending Library (Private)','Bookdealer','Private Collection','Museum Collection','Prison Camp','Displaced Persons Camp','Research or University Library','Other']
fates=['Dissolved', 'Liquidated', 'Sold at Auction', 'Still Active' , 'Unknown']
 


def clearimg(self):
    #Clears the temporary database of images
    guestbook_name=self.request.get('guestbook_name')
    greetings_query = tempimg.all().ancestor(
                                              guestbook_key(guestbook_name)).order('-date')
    results = greetings_query.fetch(100)
    for result in results:
        if result.author == users.get_current_user().nickname():
            result.delete()
    return
class Image(BaseHandler):
    #Creates url host for image 
    def get(self):
        greeting = db.get(self.request.get('img_id'))
        if greeting.img:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(greeting.img)
        else:
            self.error(404)
class MainPage(BaseHandler):
    #Serves for the bairbones main page
    def get(self):
        clearimg(self)
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = Provenancia.all().ancestor(
                                                  guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_query.fetch(1000)
        namelist=[]
        self.session['provenances']=[]
        self.session['book']={}
        linklist=[]
        for greeting in greetings:
            if greeting.longitude and greeting.latitude:
                id= greeting.key().id()
                namelist.append({'name':str(greeting.name_I), 'lat':greeting.latitude, 'lng':greeting.longitude, 'url':"/place?id="+str(id), 'pinvar':len(greeting.books_I)) })
        namelist = sorted(namelist, key=lambda k: k['pinvar'], reverse=True)
        oneval=namelist[0]['pinvar']
        for item in namelist:
            item['pinvar']=float(item['pinvar']/oneval)
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            Loggedin=True
            maplist=json.dumps(namelist)
            template_values = {
                'loggedin':Loggedin,
                'maplist':maplist,
                'user': users.get_current_user().nickname(),
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            Loggedin=False    
            template_values = {
                'loggedin':Loggedin,
                'greetings': '',
                'user': users.get_current_user(),
                'url': url,
                'url_linktext': url_linktext,
                }
        
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))

class ProvData(BaseHandler):
    
    def get(self):
        
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = Provenancia.all().ancestor(
                                                  guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_query.fetch(10)
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            Loggedin=True
            
            template_values = {
                'loggedin':Loggedin,
                'institutions': globalvars(True),
                'fates': globalvars(False),
                'greetings': greetings,
                'user': users.get_current_user().nickname(),
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('Provenance.html')
            self.response.write(template.render(template_values))
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            Loggedin=False
            
            template_values = {
                'loggedin':Loggedin,
                'greetings': '',
                'user': users.get_current_user(),
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('Provenance.html')
            self.response.write(template.render(template_values))
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        dataexport = Provenancia( )
                    
        try:
            dataexport.author = users.get_current_user().nickname()
        except:
            self.redirect('/?')
        dataexport.name_I = self.request.get('name_I')
        dataexport.type_I = globalvars(True).index(self.request.get('type_I'))
        dataexport.location_I = self.request.get('location_I')
        try:
            dataexport.longitude = float(self.request.get('longitude'))
            dataexport.latitude = float(self.request.get('latitude'))
            dataexport.yearsActive_I= int(self.request.get('yearsActive_I'))
        except:
            self.redirect('/enterprovdata')
        
        dataexport.owner_I = self.request.get('owner_I')
        dataexport.description_I= self.request.get('description_I')
        dataexport.fate_I= globalvars(False).index(self.request.get('fate_I'))
        
        
        dataexport.put()
        query_params = {'guestbook_name': guestbook_name}
        self.session['provenances']=[False,]
                    
        self.redirect('/?' + urllib.urlencode(query_params))

class ProvPoint(BaseHandler):
    def get(self):
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = Provenancia.all().ancestor().order('-date')
        greetings = greetings_query.fetch(1000)
        publist=[]
        namelist={}
        tablebool=False
        self.session['author']=users.get_current_user().nickname()
        if 'provenances' in self.session:
            tablebool=True

        try:
            bookinfo=self.session['book']
        except:
            self.redirect('/enterbookdata')
        for greeting in greetings:
            namelist[greeting.name_I]=greeting.key().id()
        url = users.create_logout_url(self.request.uri)

        provenances=self.session['provenances']
        provindex=self.request.get('Indexvalue')
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = tempimg.all().ancestor()).order('-date')
        results = greetings_query.fetch(100)
        for provenance in provenances:
            ind=item['provindex']
            (provenance[ind])['imgbool']=False
            for result in results:
                if result.indexkey==ind and result.img:
                    (provenances[ind])['imgbool']=True
                    break
        self.session['provenances']=templist

        template_values = {
            'loggedin':bool(users.get_current_user()),
            'tablebool':tablebool,
            'months': months,
            'bookinfo':self.session['book'],
            'provenanceEntered':self.session['provenances'],
            'templist':namelist,
            'user': users.get_current_user().nickname(),
            'url': url,
            'url_linktext': "Logout",
                }
        template = JINJA_ENVIRONMENT.get_template('Provpoints.html')
        self.response.write(template.render(template_values))


    def post(self):

        self.redirect('/finalBook')

class finalBook(BaseHandler):

    def get(self):
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = tempimg.all().ancestor().order('-date')
        results = greetings_query.fetch(100)
        for result in results:
            for item in templist:
                if item['provindex']==result.indexkey:
                    item['imgkey']=str(result.key())
                elif int(result.indexkey)==101:
                    coverimgkey = str(result.key())

        
        self.session['provenances']=templist
        bookinfo[publisherurl]="/place?id="+str((self.session['book'])['publisherkey'])
        template_values = {
            'bookinfo':self.session['book'],
            'provs':self.session['provenances'],
            'user': users.get_current_user().nickname(),
            'coverkey': coverimgkey,
            }

        template = JINJA_ENVIRONMENT.get_template('review.html')
        self.response.write(template.render(template_values))
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        dataexport = Libro()
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = tempimg.all().ancestor(
                                                 guestbook_key(guestbook_name)).order('-date')
        results = greetings_query.fetch(100)
        try:
            dataexport.author = users.get_current_user().nickname()
        except:
            self.redirect('/?')
        ts=time.time()
        provlist=[str(ts),]
        intprovlist=[]
        bookdict=self.session['book']
        for row in self.session['provenances']:
            stamp= Stamps( )
            stamp.provname=row['provenances']
            stamp.provnotes=row['provenances']
            for result in results:
                if result.indexkey==row['provindex']:
                    try:
                        stamp.img=result.img
                    except:
                        pass
                elif int(result.indexkey)==101:
                    coverimg=result.img
            stamp.provkey=int(row['provkey'])
            stamp.bookkey=str(bookdict['title_B'])
            stamp.timefloat= ts

            stamp.put()


        stamps = db.GqlQuery('SELECT * '
                                        'FROM Stamps '
                                        'WHERE ANCESTOR IS :1 '
                                        'ORDER BY timefloat DESC LIMIT 100',
                                        guestbook_key(guestbook_name))
        for stamp in stamps:
            if stamp.timefloat==ts:
                ids=stamp.key().id()
                intprovlist.append(ids)
                provlist.append(stamp.provname)
        dataexport.provenance_B=provlist
        dataexport.stamplist=intprovlist
        dataexport.author_B = bookdict['author_B']
        dataexport.authorfirst_B = bookdict['authorfirst_B']
        dataexport.title_B = bookdict['title_B']
        if dataexport.author_B=='' or dataexport.title_B=='':
            self.redirect('/enterbookdata')
        dataexport.series_B = bookdict['series_B']
        dataexport.edition_B= int(bookdict['edition_B'])
        dataexport.language_B = bookdict['language_B']
        dataexport.publishedwhere_B = bookdict['publishedwhere_B']
        dataexport.publishedyear_B = bookdict['publishedyear_B']
        dataexport.publisher_B = bookdict['publisher_B']
        dataexport.publisherkey = int(bookdict['publisherkey'])
        dataexport.img=coverimg
        dataexport.put()
        query_params = {'guestbook_name': guestbook_name}
        books = db.GqlQuery('SELECT * '
                                     'FROM Libro '
                                     'WHERE ANCESTOR IS :1 '
                                     'ORDER BY date DESC LIMIT 100',
                                     guestbook_key(guestbook_name))
        
        for row in self.session['provenances']:
            id = int(row['provkey'])
            item = Provenancia.get_by_id(id, parent=guestbook_key())
            for book in books:
                if book.provenance_B[0]==str(ts):
                    templist= item.books_I
                    templist.append(int(book.key().id()))
                    item.books_I=templist
                    item.put()
                    break
        self.session['provenances']=[]
        self.session['book']={}
        clearimg(self)

        self.redirect('/?' + urllib.urlencode(query_params))


class BookData(BaseHandler):
    def get(self):
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = Provenancia.all().ancestor(
                                                  guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_query.fetch(1000)
        
        publist={}
        for greeting in greetings:
          if greeting.type_I==0:
              publist[greeting.name_I]=greeting.key().id()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        if users.get_current_user():
            Loggedin=True
        else:
            Loggedin=False
        editionlist=[]
        editionlist=range(1, 15)
        template_values = {
            'loggedin':Loggedin,
            'editionlist':editionlist,
            'publist': publist,
            'months': ,
            'user': users.get_current_user().nickname(),
            'url': url,
            'url_linktext': url_linktext,
        }
        
        template = JINJA_ENVIRONMENT.get_template('book.html')
        self.response.write(template.render(template_values))
    def post(self):
        book = self.request.get('guestbook_name')
        book_cover = tempimg( )
        avatar = self.request.get('img')
        try:
            greeting.img = db.Blob(avatar)
        except:
            pass
        greeting.indexkey = False
        dataexport = {}
        
        try:
            dataexport['author'] = users.get_current_user().nickname()
            book.author= users.get_current_user().nickname()
        except:
            self.redirect('/?')
        for arg in self.request.arguments():
            if arg=='publisher_B':
                namesplit=re.split('\|', self.request.get(arg))
                dataexport['publisher_B']=namesplit[0]
                dataexport['publisherkey']=namesplit[1]
                continue
            elif arg!="img": 
                dataexport[item]=self.request.get(item)
        if not( dataexport['author_B'] or dataexport['title_B']):
            self.redirect('/enterbookdata')
        book_cover.put()
        self.session['book']=dataexport
        self.redirect('/provpoints')
class Provenance(BaseHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        greeting = tempimg()
        avatar = self.request.get('img')
        try:
            greeting.img = db.Blob(avatar)
        except:
            pass
        provenancein={}
        for item in self.request.arguments():
            if item=='img':
                continue
            elif item=='provenances':
                namesplit=re.split('\|', self.request.get(item))
                provenancein['provenances']=namesplit[0]
                provenancein['provkey']=namesplit[1]
                continue
            provenancein[item]=self.request.get(item)
        if provenancein['provenances']=='':
            self.redirect('/provpoints')
        if provenancein['provyear']!='':
            try:
                provyear=int(provenancein['provyear'])
            except:
                self.redirect('/provpoints')
        templist=self.session['provenances']
        provenancein['provindex']=len(self.session['provenances'])
        greeting.indexkey = provenancein['provindex']
        greeting.author= self.session['author']
        greeting.put()
        templist.append(provenancein)
        self.session['provenances']=templist
        self.redirect('/provpoints')


class DeleteProv(BaseHandler):
    def post(self):
        provindex=self.request.get('Indexvalue')
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = tempimg.all().ancestor(
                                                     guestbook_key(guestbook_name)).order('-date')
        results = greetings_query.fetch(100)
        for count, result in enumerate(results):
            if int(result.indexkey)==101:
                continue
            if int(result.indexkey)==int(provindex):
                result.delete()
            else:
                result.indexkey=count+1
                result.put()
        templist= self.session['provenances']
        del templist[int(provindex)]

        for count, inst in self.session['provenances']:
            templist[i]['provindex']=count+1
        self.session['provenances']=templist
        self.redirect('/provpoints')

class DisplayInst(BaseHandler):
    def get(self):
        idProv = int(self.request.get('id'))
        item = Provenancia.get_by_id(idProv, parent=guestbook_key())
        types=[]
        for ind in item.type_I:
            types.append(globalvars(True)[ind])
        fate=globalvars(True)[fate_I])
        booklister=[]
        for book in item.book_I:
            templib=Libro.get_by_id(int(book), parent=guestbook_key())
            for stamp in templib.stamplist:
                tempstamp=Stamps.get_by_id(int(stamp), parent=guestbook_key())
                if int(tempstamp.provkey)==idProv:
                    booklist{}
                    booklist[title]=templib.title_B
                    booklist[author]=  templib.author_B+", "+templist.authorfirst_B
                    booklist[edition]=templib.edition_B
                    booklist[id]=book
                    booklist[subject]=templib.subject_B
                    booklist[year]=timestamp.year
                    booklist[month]=timestamp.month
                    booklist[dte]=str(booklist[month])+"/"+str(booklist[year])
                    booklister.append(booklist)
                    
            booklister = sorted(booklister, key=lambda k: k['year'])
            #booklister = sorted(booklister, key=lambda k: k['month'])
            
        template_values = {
            'item':item,
            'booklist':booklister,
            'id':id,
            'types':types,
            'fate': fate

        }
        
        
        template = JINJA_ENVIRONMENT.get_template('place.html')
        self.response.write(template.render(template_values))
    def post(self):
                
        template = JINJA_ENVIRONMENT.get_template('place.html')
        self.response.write(template.render(template_values))
        
class BkDisplay(BaseHander):
    def get(self):
        idBook = int(self.request.get('id'))
        item = Libro.get_by_id(idBook, parent=guestbook_key())
        provs=[]
        for stampid in item.stamplist:
            stamp=Stamps.get_by_id(int(stampid), parent=guestbook_key())
            prov={}
            prov[provenance]=stamp.provname
            prov[provmonth]=stamp.provmonth
            prov[provyear]=stamp.provyear
            prov[provnotes]=stamp.provnotes
            prov[imgurl]="img?img_id="+str(stamp.key())
            provs.append(prov)
        provs = sorted(provs, key=lambda k: k['provyear'])
        bookinfo[author_B]=item.author_B
        bookinfo[authorfirst_B]=item.authorfirst_B
        bookinfo[edition_B]=item.edition_B
        bookinfo[publishedwhere_B]=item.publishedwhere_B
        bookinfo[subject_B]=item.subject_B
        bookinfo[description_B]=item.description_B
        bookinfo[series_B]=item.series_B
        bookinfo[publishedyear_B]=item.publishedyear_B
        bookinfo[publisher_B]=item.publisher_B
        bookinfo[publisherurl]="/place?id="+str(item.publisherkey)
        bookinfo[title_B]=item.title_B
        coverkey=str(item.key())
        template_values = {
        'bookinfo':bookinfo,
        'provs':provs,
        'coverkey':coverkey
    
            }
    
    
        template = JINJA_ENVIRONMENT.get_template('biblio.html')
        self.response.write(template.render(template_values))
    def post(self)
        pass
