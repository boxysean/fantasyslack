from django.conf.urls import url

from views import HomeView, MessagesList, MessagesDetail, StatsList

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^messages/$', MessagesList.as_view(), name=MessagesList.url_name),
    url(r'^messages/(?P<object_id>.*)/$', MessagesDetail.as_view(), name=MessagesDetail.url_name),
    url(r'^stats/$', StatsList.as_view(), name=StatsList.url_name),
]
