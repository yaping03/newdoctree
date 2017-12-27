from django.shortcuts import render
from django.db.models import Count
from doctree.models import Knowledge, Chapter, Book
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def index(request):
	return render(request, 'doctree/index.html')

def doctree(request, title):
	
	level = 4
	if title=="None":
		title = None
	knowledges = Knowledge.objects.filter(level=level, title=title)[:16]
	# print(knowledges)
	parents = []
	children = []

	for knowledge in knowledges:
		knowledge.loadAll()
		# knowledge.loadChildren()
		parents.append(knowledge)
	# 	children.append(knowledge.knowledge_set.order_by('title'))

	context = { 'parents':parents }

	return render(request, 'doctree/tree1.html', context)


def docmerge(request):
	
	action = request.POST.get('action')
	
	print(action)
	if action=="合并":
		merge_ids = request.POST.getlist('merge_ids[]')
		merge_to = request.POST.get('merge_to')
		merge_to = int(merge_to)

		if merge_ids and merge_to:
			parent = Knowledge.objects.get(id=merge_to)
			for merge_id in merge_ids:
				merge_id = int(merge_id)
				if merge_id != merge_to:
					merge_from= Knowledge.objects.get(id=merge_id)
					merge_from.loadChildren()
					for child in merge_from.children:
						child.parent = parent
						child.save()
					if merge_from.content:
						merge_from.title = merge_from.title+"_合并"
						merge_from.parent = parent
						merge_from.level = parent.level+1
						merge_from.save()
					else:
						merge_from.delete()
	elif action=="删除":
		merge_ids = request.POST.getlist('merge_ids[]')
		print(merge_ids)
		if merge_ids:
			for del_id in merge_ids:
				delKw = Knowledge.objects.get(id=del_id)
				delKw.deleteAll()

	goto = request.POST.get('prev_url')

	return HttpResponseRedirect(goto)

def knowledge(request, kid):
	knowledge = Knowledge.objects.get(id=kid)
	knowledge.loadAll()

	context = { 'knowledge' : knowledge , 'start' : knowledge.level }
	
	return render(request, 'doctree/knowledge.html', context)


def kwmerge(request):
	action = request.POST.get('action')
	if action=="从属":
		merge_ids = request.POST.getlist('merge_ids[]')
		merge_to = request.POST.get('merge_to')
		merge_to = int(merge_to)

		if merge_ids :
			if merge_to>0:
				parent = Knowledge.objects.get(id=merge_to)
				toLevel = parent.level+1
			elif merge_to==0 :
				parent = None
				toLevel = 4
			elif merge_to<0:
				toLevel = 4

			for merge_id in merge_ids:
				merge_id = int(merge_id)
				if merge_id != merge_to:
					merge_from= Knowledge.objects.get(id=merge_id)
					merge_from.parent = parent
					merge_from.setLevel(toLevel)
	elif action=="删除":
		merge_ids = request.POST.getlist('merge_ids[]')
		if merge_ids:
			for del_id in merge_ids:
				delKw = Knowledge.objects.get(id=del_id)
				delKw.deleteAll()
	elif action=="通过":
		merge_ids = request.POST.getlist('merge_ids[]')
		if merge_ids:
			for action_id in merge_ids:
				kw = Knowledge.objects.get(id=action_id)
				kw.setStatus("pass")
	elif action=="未通过":
		merge_ids = request.POST.getlist('merge_ids[]')
		if merge_ids:
			for action_id in merge_ids:
				kw = Knowledge.objects.get(id=action_id)
				kw.setStatus("reject")

	goto = request.POST.get('prev_url')

	return HttpResponseRedirect(goto)

def kwlist(request):
	
	klist = Knowledge.objects.filter(level=4)
	if request.GET.get('status'):
		klist = klist.filter(status=request.GET.get('status'))
	if request.GET.get('book_id'):
		chapter_ids = Chapter.objects.filter(book_id=request.GET.get('book_id')).values_list('id',flat=True)
		klist = klist.filter(chapter_id__in=chapter_ids)
	if request.GET.get('search'):
		klist = klist.filter(title__contains=request.GET.get('search'))

	klist = klist.order_by('-modified_at')
	paginator = Paginator(klist, 25) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
	    knowledges = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    knowledges = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    knowledges = paginator.page(paginator.num_pages)

	for knowledge in knowledges:
	 	knowledge.loadBook()
	
	# print(knowledges.paginator.page_range)

	books = Book.objects.order_by('title','summarized', 'id')
	status = ["pending", "pass", "reject"]
	r = near_range(knowledges)
	search = request.GET.get('search')

	context = { 'knowledges' : knowledges, 'books' : books, 'status' : status, 'near_range' : r , 'search' : search}

	return render(request, 'doctree/kwlist.html', context)

def l5list(request):
	rlist = Knowledge.objects.filter(level=5).values('title').annotate(count=Count('id')).order_by('-count')
	paginator = Paginator(rlist, 50)
	page = request.GET.get('page')

	try:
	    relationships = paginator.page(page)
	except PageNotAnInteger:
	    relationships = paginator.page(1)
	except EmptyPage:
	    relationships = paginator.page(paginator.num_pages)

	r = near_range(relationships)

	context = { 'relationships' : relationships, 'near_range' : r }

	return render(request, 'doctree/l5list.html', context)

def show_relationship(request, title):
	klist = Knowledge.objects.filter(level=5, title = title).order_by('id')
	paginator = Paginator(klist, 25)
	page = request.GET.get('page')

	try:
	    knowledges = paginator.page(page)
	except PageNotAnInteger:
	    knowledges = paginator.page(1)
	except EmptyPage:
	    knowledges = paginator.page(paginator.num_pages)

	for knowledge in knowledges:
		knowledge.parent
		knowledge.loadAll()

	r = near_range(knowledges)

	context = { 'knowledges' : knowledges, 'near_range' : r, 'title' : title }

	return render(request, 'doctree/show_relationship.html', context)

def rejectlist(request):
	klist = Knowledge.objects.filter(status='reject').order_by('chapter_id', '-level', 'parent_id', 'id')
	paginator = Paginator(klist, 25)
	page = request.GET.get('page')

	try:
	    knowledges = paginator.page(page)
	except PageNotAnInteger:
	    knowledges = paginator.page(1)
	except EmptyPage:
	    knowledges = paginator.page(paginator.num_pages)

	r = near_range(knowledges)

	exist_ids = []

	results = []

	for knowledge in knowledges:
		if knowledge.id not in exist_ids:
			k = knowledge
			root_id = k.id
			result = []
			k.loadBook()
			# print(k.book)
			result.insert(0, k)
			exist_ids.append(k.id)
			while k.parent:
				k = k.parent
				root_id = k.id
				k.loadBook()
				result.insert(0, k)
				exist_ids.append(k.id)

			result.insert(0,root_id)
			results.append(result)

	context = { 'knowledges' : knowledges, 'near_range' : r, 'results' : results }

	return render(request, 'doctree/rejectlist.html', context)


def near_range(pagination):
	half_range = 3
	current = pagination.number
	start = current-half_range
	if start<1:
		start = 1
	end = current+half_range
	if end>pagination.paginator.num_pages:
		end = pagination.paginator.num_pages

	return range(start, end+1)
