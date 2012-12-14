import webapp2
import random
import cgi
from google.appengine.ext import db
surl=[]
class url_obj(db.Model):
	url=db.StringProperty(multiline=True)
	s_1=db.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')
		self.response.out.write("""<form>URL Shortener<br><Textarea name='content'rows="3" cols="60"></Textarea><div><input type="submit" value="Shorten"></div></div>
				</form>""")
		url=self.request.get('content')
        	for i in range(len(url)):
			if i%20==0:
				surl.append(url[i])
		s_1=''.join(surl)
		if url != "":
			obj=url_obj(parent=db.Key.from_path('URL LIST',url))
			obj.url=url
			obj.s_1=s_1
			a=db.GqlQuery("SELECT * FROM url_obj WHERE ANCESTOR IS :c",c=db.Key.from_path('URL LIST',url))
			count =0
			for i in a:
				count=count+1
			if count==0:
				obj.put()
			b=db.GqlQuery("SELECT * FROM url_obj WHERE ANCESTOR IS :c",c=db.Key.from_path('URL LIST',url))

			for i in b:
				self.response.out.write("sreedathurlshorten.appspot.com/")
				self.response.out.write(i.s_1)
				self.response.out.write("""<br>""")
			self.response.out.write("""</body></html>""")
		if self.request.path[1:]!="":
			u=url_obj.all()
			res = u.filter("s_1 =",self.request.path[1:]).get()
			self.redirect(str(res.url))			

app=webapp2.WSGIApplication([('/.*',MainPage)],debug=True)
