import pandas as pd

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
			article.linked = True
			self.narticles = len(self.articles)
		else:print('skipping article',article,'already present')


	def xml(self):
		pass
	


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


	def __repr__(self):
		m = 'article: ' +self.topic+ ' ' + str(self.year) + ' ' + self.name_paper
		return m
	

	def __str__(self):
		return self.__repr__()


	def __eq__(self,other):
		return type(other) == type(self) and self.identifier == other.identifier


	def xml(self):
		pass



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
		for i,p in enumerate(self.papers):
			temp = [a for a in articles if a.paper_id == p.identifier]
			if temp == []:continue
			p.add_articles(temp)
		

	def add_article(self, article):
			index = self.identifier2index[article.paper_id]
			self.papers[index].add_article(article)


	def reload(self):
		self.load_papers(self)



class Articles():
	def __init__(self):
		self._load_articles()
	

	def _load_articles(self):
		self.articles = []
		articles = load_articles()
		for line in articles.values:
			identifier, name_paper, year_id, topic = line
			self.articles.append(Article(identifier,name_paper,year_id,topic))
			
			


		

def database():
	pass


def load_papers():
	return load_xlsx('papers.xlsx')

def load_articles():
	return load_xlsx('articles.xlsx')

def load_xlsx(filename):
	return pd.read_excel(filename,header = None)
	




		
		

	

