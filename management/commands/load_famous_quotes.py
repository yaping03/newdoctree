import doctree.models as models
from django.core.management.base import BaseCommand
import xlrd
class Command(BaseCommand):
    '''
    python manage.py load_famous_quotes --file [file_name]
    '''
    def add_arguments(self, parser):
        parser.add_argument('--file', dest='file',nargs='+', type=str)
    def handle(self, *args, **options):
        file = options['file'][0]
        data = xlrd.open_workbook(file)
        quotes = data.sheet_by_name("名言")
        famous = data.sheet_by_name("人物")

        creates = []
        for row in range(famous.nrows):
            if famous.row_values(row)[0]:
                new = models.Celebrity(name=famous.row_values(row)[0],describe=famous.row_values(row)[2],introduction=famous.row_values(row)[3])
            creates.append(new)
        models.Celebrity.objects.bulk_create(creates)
        creates = []
        for row in range(quotes.nrows):
            if quotes.row_values(row)[3]:
                if quotes.row_values(row)[1]:
                    celebry = models.Celebrity.objects.filter(name=quotes.row_values(row)[1]).first()
                    if not celebry:
                        celebry = models.Celebrity.objects.create(name=quotes.row_values(row)[1])
                else:
                    celebry = models.Celebrity.objects.filter(name='None').first()
                new = models.Quote(famous=celebry, content=quotes.row_values(row)[3], tag=quotes.row_values(row)[2])
                creates.append(new)
        models.Quote.objects.bulk_create(creates)
