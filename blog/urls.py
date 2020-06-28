from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),                        
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^export/excel/$', views.export_posts_excel, name='export_posts_excel'),
    url(r'^import/$', views.post_import, name='post_import'),
    url(r'^namu_search/$', views.namu_search_view, name='namu_search_view'),
]

#post/(?P<pk>\d+) 여기 있는 pk가 글번호니까 이게 바로 다이내믹 유아렐이고 이거를 위해서 get_object_or_404가 필요하다. 그래서 
#get_object_or_404는 edit, remove,그리고 detail에만 필요하다. new나 list에서는 불필요

#(r'^$')니까 도메인뒤에 아무것도 없는 것. 즉, 홈페이지

#url(r'^post/패턴1, views.함수1, name='이름1'),
#url(r'^post/패턴2, views.함수2, name='이름2'),
#url(r'^post/패턴3, views.함수3, name='이름3'),

#위와 같이 되어있으면 url디스패처가 해당 url의 패턴을 맨 위에서부터 비교해봐서 
#매칭되는 첫번째 패턴에 있는 views.함수를 불러와준다 - 공식문서