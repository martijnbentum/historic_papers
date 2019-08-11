from lxml import etree
import pandas as pd
import progressbar as pb

normalize_paper_name = dict([line.split(',') for line in open('paper_names.dict').read().split('\n') if line])

class Paper():
	def __init__(self,name,number,year,city):
		self.name= name
		self.number = number
		self.year = int(year)
		self.city = city
		self.identifier = '_'.join(map(str,[name.lower(),number,year]))
		self.articles = []
		self.narticles = 0


	def __repr__(self):
		m = 'paper: ' +self.name + ' ' + str(self.year) + ' ' + self.city
		return m


	def __str__(self):
		m = self.__repr__() + '\n'
		m += 'number of articles:\t' + str(self.narticles) + '\n'
		m += 'identifier:\t' + str(self.identifier) + '\n'
		return m


	def __eq__(self,other):
		if type(other) != type(self): return False
		return self.identifier == other.identifier


	def __lt__(self,other,comparison = 'year'):
		if type(other) != type(self): NotImplemented
		if comparison == 'year': return self.year < other.year
		

	def add_articles(self,articles):
		if type(articles) == Article:
			self.add_article(articles)
		elif type(articles) == list:
			for a in articles:
				self.add_article(a)
		else: raise ValueError('expected article or list of articles')


	def add_article(self,article):
		if article.paper_id != self.identifier: return
		elif article not in self.articles: 
			self.articles.append(article)
			article.city = self.city
			article.linked = True
			self.narticles = len(self.articles)
		else:print('skipping article',article,'already present')


	def xml(self, force_new=True):
		if not hasattr(self,'xml') or force_new: self.xmls = paper2xml(self)
		return self.xmls


		
class Article():
	def __init__(self,identifier,name_paper,year_id,topic):
		self.identifier = identifier
		self.name_paper = name_paper
		self.year_id = year_id
		self.topic = topic
		self.year,self.number= year_id.split(':')
		self.year = int(self.year)
		self.number = int(self.number)
		if name_paper.lower() in normalize_paper_name.keys(): 
			name_paper = normalize_paper_name[name_paper.lower()]
		else: name_paper = name_paper.lower()
		self.paper_id = '_'.join(map(str,[name_paper,self.number,self.year]))
		self.linked = False
		self.city = ''


	def __repr__(self):
		m = 'article: ' +self.topic+ ' ' + str(self.year) + ' ' + self.name_paper
		return m
	

	def __str__(self):
		return self.__repr__()


	def __eq__(self,other):
		if type(other) != type(self): return False
		return type(other) == type(self) and self.identifier == other.identifier


	def __lt__(self,other):
		if type(other) != type(self): NotImplemented
		if comparison == 'year': return self.year < other.year


	def xml(self):
		if not hasattr(self,'xml') or force_new: self.xmls = article2xml(self)
		return self.xmls



class Papers():
	def __init__(self):
		self._load_papers()
		self.problem_articles = []


	def __repr__(self):
		m = 'papers: ' + str(self.npapers)
		return m


	def _load_papers(self):
		self.papers = []
		papers = load_papers()
		cities,names = [],[]
		self.identifier2index = {}
		for i, line in enumerate(papers.values):
			name, number, year, city = line
			self.papers.append(Paper(name,number,year,city))
			cities.append(city)
			names.append(name)
			self.identifier2index[self.papers[-1].identifier] = i
		self.npapers = len(self.papers)
		self.cities = list(set(cities))
		self.names = list(set(names))


	def add_articles(self,articles):
		if type(articles) == Article: add_article(articles)
		bar = pb.ProgressBar()
		bar(range(len(self.papers)))
		for i,p in enumerate(self.papers):
			bar.update(i)
			# temp = []
			# for j,a in enumerate(articles):
			# if a.paper_id == p.identifier: temp.append(articles.pop(j))
			# temp = [a for a in articles if a.paper_id == p.identifier]
			# if temp == []:continue
			# p.add_articles(temp)
			p.add_articles(articles)

	def add_article(self, article):
			index = self.identifier2index[article.paper_id]
			self.papers[index].add_article(article)


	def reload(self):
		self.load_papers(self)


	def xml(self, force_new = True):
		if not hasattr(self,'xml') or force_new: self.xmls = papers2xml(self)
		return self.xmls
	

	def save(self,name= 'papers.xml'):
		save_xml(self.xmls,name)



class Articles():
	def __init__(self):
		self._load_articles()
	

	def _load_articles(self):
		self.articles = []
		articles = load_articles()
		for line in articles.values:
			identifier, name_paper, year_id, topic = line
			self.articles.append(Article(identifier,name_paper,year_id,topic))
		self.topics = list(set([a.topic for a in self.articles]))
		self.narticles = len(self.articles)
			
	def xml(self,force_new = True):
		if not hasattr(self,'xmls') or force_new: self.xmls = articles2xml(self)
		return self.xmls
	
	def save(self,name= 'articles.xml'):
		save_xml(self.xmls,name)

		

class Database():
	def __init__(self, save = False):
		print('loading papers')
		self.p = Papers()
		print('loading articles')
		self.a = Articles()
		print('linking papers with articles')
		self.p.add_articles(self.a.articles)
		self.a.xml()
		self.p.xml()
		if save: self.save()

	def save(self):
		self.a.save()
		self.p.save()
	
		

def article2xml(a,goal = None):
	if goal == None: o = etree.Element('article', id = str(a.identifier))
	else: o = etree.SubElement(goal,'article', id = str(a.identifier))
	return dict2info(a.__dict__,a.__dict__.keys(),o)

def paper2xml(p,goal = None):
	if goal == None: o = etree.Element('paper', id = str(p.identifier))
	else: o = etree.SubElement(goal,'paper', id = str(p.identifier))
	article_ids = ','.join([str(article.identifier) for article in p.articles])
	names = 'name,number,year,city,identifier,article_ids'.split(',')
	values = [p.name,p.number,p.year,p.city,p.identifier,article_ids]
	d = make_dict(names,values)
	return dict2info(d,names,o)

def articles2xml(a,goal = None):
	if goal == None: o = etree.Element('articles')
	else: o = etree.SubElement(goal,'articles')
	[article2xml(article,o) for article in a.articles]
	topics = ','.join(list(set([article.topic for article in a.articles])))
	names = ['topics','narticles']
	values = [topics,a.narticles]
	d = make_dict(names,values)
	return dict2info(d,names,o)

def papers2xml(p,goal = None):
	if goal == None: o = etree.Element('papers')
	else: o = etree.SubElement(goal,'papers')
	[paper2xml(paper,o) for paper in p.papers]
	paper_names = ','.join(p.names)
	cities= ','.join(p.cities)
	orphan_articles = ','.join([article.identifier for article in p.problem_articles])
	names = 'npapers,cities,paper_names,orphan_articles'.split(',')
	values = [p.npapers,cities,paper_names,orphan_articles]
	d = make_dict(names,values)
	return dict2info(d,names,o)

def load_papers():
	return load_xlsx('papers.xlsx')

def load_articles():
	return load_xlsx('articles.xlsx')

def load_xlsx(filename):
	return pd.read_excel(filename,header = None)

def make_dict(names,values):
	return dict([[n,v] for n,v in zip(names,values)])

def dict2info(d,names,goal):
	for name in names:
		e = etree.SubElement(goal,name)
		e.text = str(d[name])
	return goal

def pxml(xml):
	print(etree.tostring(xml,encoding = 'utf8',pretty_print=True).decode())

def save_xml(xml,name):
	t = etree.tostring(xml,encoding = 'utf8',pretty_print=True)
	with open(name,'wb') as fout:
		fout.write(t)
	print('saved:',name)

		
		

	

