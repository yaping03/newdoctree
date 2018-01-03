from django.db import models

# Create your models here.
class Book(models.Model):
	title = models.CharField(max_length=50, null=True, blank=True)
	author = models.CharField(max_length=50, null=True, blank=True)
	summarized = models.CharField(max_length=50, null=True, blank=True)
	meta = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def hasChildren(self):
		count = self.chapter_set.count()
		# print(count)
		return count>0

	def __str__(self):
		return str(self.title)


class Chapter(models.Model):
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, default=1, blank=True, null=True)
	parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=1, blank=True, null=True)
	title = models.CharField(max_length=255, null=True, blank=True)
	level = models.SmallIntegerField(default=0, blank=True) 
	meta =  models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def loadChildren(self, passon=False):
		children = self.chapter_set.order_by('title', 'id')
		if passon:
			for chapter in children:
				if chapter.id != self.id:
					chapter.loadChildren()

		self.children = children

	def hasChildren(self):
		kCount = self.knowledge_set.count()
		cCount = self.chapter_set.count()
		# print(kCount+cCount)
		return kCount+cCount>0

	def __str__(self):
		prefix = ""
		for x in range(1, self.level):
			prefix = prefix+" "
		return prefix+str(self.level)+"-"+str(self.id)+"-"+str(self.title)


class Knowledge(models.Model):
	chapter = models.ForeignKey('Chapter', on_delete=models.SET_NULL, default=1, blank=True, null=True)
	parent = models.ForeignKey('self', on_delete=models.SET_NULL, default=1, blank=True, null=True)
	title = models.TextField(null=True, blank=True)
	category = models.CharField(max_length=20, null=True, blank=True)
	level = models.SmallIntegerField(default=0, blank=True) 
	content = models.TextField(null=True, blank=True)
	status = models.CharField(max_length=20, default="pending")
	is_alone = models.BooleanField(default=False)
	meta = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def loadAll(self):
		self.loadChildren()
		self.loadBook()
		self.loadLevel()
		for child in self.children:
			if child.id != self.id:
				child.loadAll()

	def loadBook(self):
		# print(123)
		try:
			self.book = self.chapter.book
		except Exception as e:
			print("no book : "+str(self))
			self.book = None
		
		# print(self.book)

	# def loadParent(self):
	# 	self.parent = self.parent


	def loadChildren(self, passon=False):
		children = self.knowledge_set.order_by('title', 'id')
		if passon:
			for knowledge in children:
				if knowledge.id != self.id:
					knowledge.loadChildren()

		self.children = children

	def loadLevel(self, passon=False):
		self.span = 7-self.level
		self.range = range(4,self.level)
		if self.status=='pending':
			self.statusClass = "warning"
		elif self.status=='pass':
			self.statusClass = "success"
		elif self.status=='reject' or self.status=='alone':
			self.statusClass = "danger"

	def getStatusClass(self):
		if self.status=='pending':
			self.statusClass = "warning"
		elif self.status=='pass':
			self.statusClass = "success"
		elif self.status=='reject' or self.status=='alone':
			self.statusClass = "danger"

		return self.statusClass

	def setLevel(self, toLevel):
		self.level = toLevel
		self.save()
		children = self.knowledge_set.all()
		for child in children:
			child.setLevel(toLevel+1)

	def setStatus(self, status):
		self.status = status
		self.save()
		children = self.knowledge_set.all()
		for child in children:
			child.setStatus(status)

	def deleteAll(self):
		children = self.knowledge_set.all()
		for child in children:
			child.deleteAll()
		self.delete()

	def hasChildren(self):
		childrenCount = self.knowledge_set.count()
		return childrenCount>0

	def mergeFrom(self, knowledge):
		if self.id != knowledge.id and self.level == knowledge.level:
			knowledge.loadChildren()
			self.loadChildren()

			if not self.category and knowledge.category:
				self.category = knowledge.category
				self.save()

			for child in knowledge.children:
				# print(child)
				child.parent = self
				child.save()
				# print("parent"+str(child.parent))

			if not knowledge.content or self.content == knowledge.content:
				# print("delete"+str(knowledge))
				knowledge.delete()
			else:
				knowledge.title = knowledge.title+"_合并"
				knowledge.parent = self
				knowledge.level = self.level+1
				knowledge.save()
			self.reduceRedundance()

	def reduceRedundance(self):
		self.loadChildren()
		lastTitle = None
		lastKnowledge = None
		for child in self.children:
			if lastKnowledge and child.title and child.title==lastTitle:
				lastKnowledge.mergeFrom(child)
			else :
				lastKnowledge = child
				lastTitle = child.title
			


	def __str__(self):
		prefix = ""
		for x in range(1,self.level):
			prefix = prefix+" "
		return prefix+str(self.level)+"-"+str(self.id)+"-"+str(self.title)


class FileUpload(models.Model):
	title = models.CharField(max_length=50, null=True, blank=True)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, default=None, blank=True, null=True)

	def __str__(self):
		return str(self.title)+" : "+str(created_at)

