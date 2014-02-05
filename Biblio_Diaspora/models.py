import webapp2



class Provenancia(db.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    def __init__(self, **entries):
        '''initializes from dict used in controller'''
        floatables = ("longitude", "latitude")
        intables = ("fate_I" "yearsActive_I"):
        for entry in entries:
            forcetype = (str, float, int) [(entry in flotable) + (entry in intable)* 2]
            entries[entry]=forcetype(entries)
        self.__dict__.update(entries)
    author = db.StringProperty()
    name_I = db.StringProperty()
    type_I = db.ListProperty(int,indexed=True, default=[])
    location_I=db.StringProperty()
    longitude = db.FloatProperty()
    latitude = db.FloatProperty()
    yearsActive_I=db.IntegerProperty()
    owner_I=db.StringProperty()
    description_I=db.StringProperty(multiline=True)
    fate_I=db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    books_I=db.ListProperty(int,indexed=True, default=[])


class Libro(db.Model):
    ''"Books Model"

    def __init__(self, **entries):
        '''initializes from dict used in controller'''
        for intable in "edition", "publisherkey":
            if intable in entries: 
                #assures typing
                entries[intable ]=int(entries[intable])
        self.__dict__.update(entries)

    author = db.StringProperty()
    author_B= db.StringProperty()
    authorfirst_B = db.StringProperty()
    title_B= db.StringProperty()
    series_B = db.StringProperty()
    publishedwhere_B =db.StringProperty()
    edition= db.IntegerProperty()
    publishedyear_B=db.StringProperty()
    publisher_B= db.StringProperty()
    publisherkey = db.IntegerProperty()
    language_B=db.StringProperty()
    subject=db.StringProperty()
    description_B=db.StringProperty(multiline=True)
    provenance_B = db.ListProperty(str,indexed=True, default=[])
    stamplist = db.ListProperty(int,indexed=True, default=[])
    date = db.DateTimeProperty(auto_now_add=True)
    img=db.BlobProperty()

class Stamps(db.Model):
    def __init__(self, **entries):
        self.__dict__.update(entries)
    author = db.StringProperty()
    timefloat = db.FloatProperty()
    provname = db.StringProperty()
    provkey =db.IntegerProperty()
    provyear = db.IntegerProperty()
    provmonth= db.StringProperty()
    provnotes= db.StringProperty()
    img = db.BlobProperty()

class tempimg(db.Model):
    #temporary image before entered in permanant database
    indexkey = db.IntegerProperty()
    author = db.StringProperty()
    img = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)