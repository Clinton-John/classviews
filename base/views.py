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