from django.core.management.base import BaseCommand
from doctree.models import Book, Chapter, Knowledge, FileUpload
import os, json

class Command(BaseCommand):

	def add_arguments(self, parser):
		parser.add_argument('bookid', nargs='+', type=int)
		# print(parser)

	def handle(self, *args, **options):
		bookid = options['bookid'][0]
		
		book = Book.objects.get(id=bookid)

		for upload in book.fileupload_set.order_by('id'):
			upload.delete()

		chapters = book.chapter_set.order_by('id')
		for chapter in chapters:
			knowledges = chapter.knowledge_set.order_by('id')
			for knowledge in knowledges:
				knowledge.delete()
			chapters.delete

		book.delete()




	


