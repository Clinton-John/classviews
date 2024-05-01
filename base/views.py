from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from base.models import Post
from django.shortcuts import get_object_or_404
from django.db.models import F
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

class ChatApp(TemplateView):
    #the below are the attributes that you can pass into this class to overwrite those in the initial class
    template_name = 'base/chat.html'
    # template_engine = default is DTL but you can change to allow for other features such as jinja2 and Mako
    # response_class
    # content_type

    ## to add or return some context, you can overwrite the get_context_data function from the TemplateResponseMixin and retrieve data that you want to pass to the user/frontend

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.get(id=2)
        context['data'] = "This is an example data passed"
        #these function gets the context passed and passes them to the defined template above that is the chat.html
        return context



#---------------------------Admin and Admins Page Functions ------------------------------
@login_required(login_url="login")
# @allowed_users(allowed_roles=['super_admin'])
def adminsPage(request):
    group = Group.objects.get(name='super_admin')
    group_users = group.user_set.all()

    admin_group = Group.objects.get(name='Admins')
    admin_group_users = admin_group.user_set.all()

    sports_admins = Group.objects.get(name='sports_admins')
    sports_admins_users = sports_admins.user_set.all()

    context = {'group_users':group_users, 'sports_admins_users':sports_admins_users, 'admin_group_users':admin_group_users}
    return render(request , 'base/admins_page.html' , context)

@login_required(login_url="login")
# @allowed_users(allowed_roles=['super_admin'])
def changeRole(request):
   #  message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            HttpResponse("User with the provided email doesnt exist")
            # message = "User with the provided email doesnt exist"
            # return redirect('change_role')
    
        users_group = Group.objects.get(name='Students')
        if users_group not in user.groups.all():
            return HttpResponse("The user isnt registered in the website")
            
        user.groups.remove(users_group)

        admin_group = Group.objects.get(name='Admins')
        user.groups.add(admin_group)

        return redirect('admins_page')

    context = {}
    return render(request , 'base/change_role.html' , context)

@login_required(login_url="login")
# @allowed_users(allowed_roles=['super_admin'])
def addSportsAdmin(request):
   # message = None
   if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            
            return HttpResponse("The user isnt registered in the website")
            message = "The user with the registered email doesnt exist"
            return redirect('add_sports_admin')
    
        users_group = Group.objects.get(name='Students')
        if users_group not in user.groups.all():
            return HttpResponse("The user isnt registered in the website")
            
        user.groups.remove(users_group)

        sports_admin_group = Group.objects.get(name='sports_admins')
        user.groups.add(sports_admin_group)

        return redirect('admins_page')

   context = {}
   return render(request , 'base/change_role.html' , context)




class AllTeams(RedirectView):
    #url = ''
    pattern_name = 'redirect_single_team' #this defines the pattern that you want to pass
    #in this section, we override the get_redirect_url to set up the specific url we want
    def get_redirect_url(self, *args, **kwargs):

        # post = get_object_or_404(post, pk=kwargs['pk']) #find an instance of the model Post with the id pk, which is retrieved from the url
        # post.count = F(count) + 1 #get the post with the id and then increment the count field by 1
        # post.save()
        ## this is an alternative way to redirect
        post = Post.objects.filter(pk=kwargs['pk'])
        post.update(count=F('count') + 1)
        ## no need to use the post.save because we already used the update
        return super().get_redirect_url(*args, **kwargs)
       

class SingleTeam(TemplateView):
    template_name = 'base/post.html'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_object_or_404(Post, pk= self.kwargs.get('pk'))
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['posts'] = get_object_or_404(Post, pk= self.kwargs.get('pk'))
    #     return context