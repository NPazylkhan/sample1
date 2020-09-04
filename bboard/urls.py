from django.urls import path
from .views import BbIndexView, BbByRubricView, json, fileboot, index
from .views import BbCreateView, BbAddView, BbDetailView, BbEditView, BbDeleteView

urlpatterns = [
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('add/', BbAddView.as_view(), name='add'),
    path('add/', BbCreateView.as_view(), name='add' ), 
    path ('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path ('', BbIndexView.as_view(), name='index'),
    path ('', index, name='index'),
   
    path ('fileboot/', fileboot, name='file'), 
    path ('json/', json, name='json'),
]