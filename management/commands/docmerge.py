from django.core.management.base import BaseCommand
from doctree.models import Book, Chapter, Knowledge, FileUpload
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Command(BaseCommand):

	# def add_arguments(self, parser):
	# 	parser.add_argument('level', nargs='+', type=int)
		# print(parser)

	def handle(self, *args, **options):
		lastId = 0
		length = 20

		knowledges = Knowledge.objects.filter(level=4, id__gt=lastId).order_by('id')[:length]
		while knowledges.count()>0:
			for knowledge in knowledges:
				self.merge(knowledge.title)
				if knowledge.id>lastId:
					lastId = knowledge.id
					print("lastId"+str(lastId))
			knowledges = Knowledge.objects.filter(level=4, id__gt=lastId).order_by('id')[:length]

	def merge(self, title):
		knowledges = Knowledge.objects.filter(level=4, title=title)
		
		childrenCount = {} #l4id : l5count
		bookChildren = {} #bookid : l4count+l5count
		bookCount = {} #l4id : bookid

		for knowledge in knowledges:
			knowledge.loadChildren()
			knowledge.loadBook()
			childrenCount[knowledge.id] = knowledge.children.count()
			bookCount[knowledge.id] = knowledge.book.id

		# print(childrenCount)
		for kid, children in childrenCount.items():
			bookid = bookCount[kid]
			count = bookChildren.get(bookid,0)
			cnt = count+children
			bookChildren[bookid] = cnt

		maxCount = 0
		maxBook = 0

		for bookid, children in bookChildren.items():
			if children>maxCount:
				maxCount = children
				maxBook = bookid

		# print(childrenCount)
		maxCount = 0
		maxKnowledge = 0
		for kid, children in childrenCount.items():
			# print(kid, children)
			if bookCount[kid] == maxBook and children>=maxCount:
				maxCount = children
				maxKnowledge = kid

		# print(maxKnowledge)
		mertoTo = None
		try:
			mertoTo = Knowledge.objects.get(id=maxKnowledge)
		except Exception as e:
			mergeTo = None
		
		if mertoTo:
			for knowledge in knowledges:
				# print(knowledge)
				mertoTo.mergeFrom(knowledge)


