
from django.urls import path
from api.views import DrainageSystemListCreateView

urlpatterns = [
    path('drainage-systems/', DrainageSystemListCreateView.as_view(), name='drainage-system-list-create'),
]
