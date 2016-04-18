from django.conf.urls import url

from views import HomeView, MessagesList, MessagesDetail

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^messages/$', MessagesList.as_view(), name='messages-list'),
    url(r'^messages/(?P<object_id>.*)/$', MessagesDetail.as_view(), name='messages-detail')
]
