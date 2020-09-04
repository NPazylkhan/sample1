from django.shortcuts import render
from .models import Bb
from .models import Rubric
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .forms import BbForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, Http404, FileResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView
from django.core.paginator import Paginator



def fileboot(request):
    f = r'c:/images/bg.jpg'
    return FileResponse(open(f, 'rb')) # for install as_attachment=True

def json(request):
    data = {'title': 'Motorcycle','content': 'Old','price': 1000.0}
    return JsonResponse(data, safe=True)

def index(request):
    bbs = Bb.objects.all()
    rubrics = Bb.objects.all()        
    paginator = Paginator(bbs,5)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = request.GET['page']
    page = paginator.get_page(page_num)
    context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list} 
    return render(request, 'bboard/index.html', context)

# def by_rubric(request, rubric_id):
#     bbs = Bb.objects.filter(rubric=rubric_id)
#     rubrics = Rubric.objects.all()
#     current_rubric = Rubric.objects.get(pk=rubric_id)
#     context = {'bbs':bbs, 'rubrics':rubrics, 'current_rubric':current_rubric}
#     return render(request, 'bboard/by_rubric.html',context)

# def detail(request, bb_id):
#     try:
#         bb=Bb.objects.get(pk=bb_id)
#     except Bb.DoesNotExist:
#         raise Http404('That announcement does not exist')
#     return HttpResponse()

class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data( self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.all()
        return context

        
class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'


    def get_queryset(self):
        return Bb.objects.filter(rubric = self.kwargs['rubric_id'])

    def get_context_data( self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubrics'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context



class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

# def add_and_save(request):
#     if request.method == 'POST':
#         bbf = BbForm(request.POST)
#         if bbf.is_valid():
#            bbf.save()
#            return HttpResponseRedirect(reverse('by_rubric',
#            kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
#         else:
#            context = {'form':bbf}
#            return render(request,'bboard/create.html',context)
#     else:
#         bbf = BbForm()
#         context = {'form':bbf}
#         return render(request,'bboard/create.html',context)

class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data( self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric', kwargs={'rubric_id':self.object.cleaned_data['rubric'].pk})


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data( self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data( self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
