from django.urls import path

from .views import BadgeRuleView

urlpatterns = [
    path('badger/<int:dkbfile_id>/', BadgeRuleView.as_view()),
]
