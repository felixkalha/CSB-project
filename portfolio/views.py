from django.shortcuts import get_object_or_404, redirect, render
#from django.contrib.auth.decorators import login_required #Add for 1. Broken access control flaw.

from django.contrib.auth.hashers import check_password #Fix for weak password in 2. Cryptographic failure.
from django.contrib.auth.hashers import make_password #same as above

from .models import Project
from .forms import CommentForm
from .models import Comment, Project

#We include the following two for flaw 5:
import logging
logger = logging.getLogger(__name__)

def index(request):
    latest_project_list = Project.objects.order_by('-pub_date')
    context = {'latest_project_list': latest_project_list}
    return render(request, 'portfolio/index.html', context)


def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    session_key = f'unlocked_project_{project.id}'
    unlocked = request.session.get(session_key, False)
    error_message = None
    
    if project.is_private and not unlocked:
        if request.method == 'POST':
            submitted_password = request.POST.get('draft_password','')
            #hashedpassword = make_password(project.draft_password) #include this with the other fix in models.py for flaw 2. cyrptgraphic failure.
            
            #2. Cryptographic Failures flaw: Before. I use here a weak == comparison against a text stored password and no hashing.
            if submitted_password == project.draft_password:

            #For fix instead here we will remove above and change with below:
            #if check_password(submitted_password, hashedpassword):
                request.session[session_key] = True
                unlocked = True
            else:
                error_message = 'wrong lol'

    comments = project.comment_set.order_by('pub_date')
    form = CommentForm()
    context = {'project': project, 'comments': comments, 'form': form, 'unlocked': unlocked, 'error_message': error_message,}
    return render(request, 'portfolio/detail.html', context)

def add_comment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.save()
    return redirect('portfolio:detail', project_id=project.id)

def delete_comment(request, comment_id): #delete this for fix mentioned under.
#@login_required
#def delete_comment(request, comment_id):
#    if not request.user.is_staff:
#        return HttpResponseForbidden()
#The above replaces the delete comment function to disable any random's ability to simply delete comments.
    comment = get_object_or_404(Comment, pk=comment_id)
    project_id = comment.project.id
    comment_text = comment.text
    #The following line is then implemented for flaw 5, in order to get information of what was deleted.
    #logger.warning("Comment %s ('%s') on project %s was deleted by %s", comment_id, comment_text, project_id, request.user)

    comment.delete()
    return redirect('portfolio:detail', project_id=project_id)

#Broken access control: Somone with above could delete a comment if they were logged in as admin somehow (or by guessing the commentid and using an injection perhaps?)