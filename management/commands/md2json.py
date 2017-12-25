import doctree.md_2_json as mdjson
from django.core.management.base import BaseCommand
import os, json

class Command(BaseCommand):


	def handle(self, *args, **options):
		mdFolderPath = os.path.dirname(os.path.dirname(__file__))+"/MD"
		jsonFolderPath = os.path.dirname(os.path.dirname(__file__))+"/JSON"

		for mdFile in os.listdir(mdFolderPath):
			if mdFile[0] != ".":
				mdPath = mdFolderPath+"/"+mdFile
				
				jsonFile = mdFile+".json"
				jsonPath = jsonFolderPath+"/"+jsonFile

				print("parsing: "+mdFile)

				mdjson.parse(mdPath, jsonPath)
		
