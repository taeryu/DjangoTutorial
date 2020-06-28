from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post
from .forms import PostForm, NamuForm
from django.shortcuts import redirect
import csv
from django.http import HttpResponse
from .resources import PostResource
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tablib import Dataset

#views에 있는 함수는 다음의 둘중 하나를 한다. 요청된 페이지를 담고 있는 HttpResponse객체를 반환하거나, Http404같은 예외를 발생시키거나
#그래서 return render(request, '특정html파일', optional=context)이라고 반환하는것, 즉 특정html모양으로 그려라(render)
#def 함수이름(request): return HttpResponse("<h1>hello world</h1>") 기본 모양
#꿀팁 : 헷갈리니까 함수명 자체를 _view라고 붙여라

def post_list(request):
    querry_set = Post.objects.all()                                         #1)qs(쿼리셋) = Post.objecs.all()이라고 ORM 명령어를 이용해서 DB에서 가져온 Post 클래스로 만든 데이터를 리스트 형태로 qs라는 변수에 저장함
    querry_set = querry_set.filter(published_date__lte=timezone.now())     #2)앞에서 가져온 리스트에 필터를 걸어서 현재 시각 이전에 작성된 것만 리스트를 추림
    querry_set = querry_set.order_by('-published_date')                    #3)마지막으로 정렬방식을 개시일을 기준으로 최신순으로 오름차순 정렬한 것을 qs라는 변수에 넣어줌

                         #models에서 만든 Post 클래스를 불러오고 해당 클래스가 만든 모든 객체중에 필터를 걸고 정렬
                                                           #위의 qs(쿼리셋)는 이거를 쪼갠거  Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request = request, template_name = 'blog/post_list.html', context = {'post_list' : querry_set,})

#***context의 목적*****
#여기서 request를 넣고, html주소를 넣고 마지막으로 post_list는 앞에서 정의한 쿼리셋이다 라고 딕셔너리를 만들었음
#이 딕셔너리 혹은 context를 활용해서 blog/post_list.html에서 for루프로 render(화면에 띄워줄)하려는 목적으로, 이제 좀 감이 잡힘
#중요!!!! : {key:value}로 딕셔너리 형태로 만든걸 context라고 함. html에서도 사용한바 있음. 즉 {{ request.user }}에서 문맥에 따라 내용이 바뀜
#그래서 위의 함수에서 {'post_list' : qs,}라고 써놓고, blog/post_list.html에서 {{ post_list }}라고 context를 넣어준것. 
#정확하게는 그 이후에 {{ for post in post_list }}라고 넣어줌.즉 포스트 리스트가 list type이므로 for문으로 하나씩 꺼내준 것. 
#이걸 왜 아무도 안 가르쳐줌...

def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)    #ORM으로 pk를 get했음.,,,, 보통 함수의 괄호 안에 aa=bb라고 쓰는건 해당 함수에서 쓰는 타입을 정하는거(commit=false)처럼
    except Post.DoesNotExist:
        raise Http404                 # 위의 내용을 단축해서 쓰면 post = get_object_or_404(Post, pk=pk) ==> 다이내믹 url
    return render(request = request, template_name= 'blog/post_detail.html',context= {'post' : post,})

#여기서 id로 바꾸고 템플릿에서도 id로 바꿔서 돌려봐도 동일하게 작동함
#위에서 post 변수에 Post.objects.get(pk=pk)라고 정의 했으므로 
#밑의 context에서 'post'를 템플릿에 {{ post }}로 띄울때 각 페이지의 고유 포스트를 띄울 수 있게 된다!!!! 
#즉, detali 템플릿에 가면 {% url "post_detail" post.pk %}이라고 써있다. 여기서 장고가 자동으로 만든 pk라는 고유값(id같은것)으로 불러온다는 의미
#id는 파이썬이 만든거고 pk는 장고가 만든건데 그냥 pk써라라고 스택오버플로우에서 알랴줌 https://stackoverflow.com/questions/2165865/django-queries-id-vs-pk
#장고걸스 중 "pk = post.pk이란 무엇일까요? pk는 "데이터베이스의 각 레코드를 식별"하는 기본키(Prmiary Key)의 줄임말 입니다. 
#Post 모델에서 기본키를 지정하지 않았기 때문에 장고는 pk라는 필드를 추가해 새로운 블로그 게시물이 추가될 때마다 그 값이 1,2,3 등으로 증가하게 됩니다.
#Post 객체의 다른 필드 (제목, 작성자 등)에 액세스하는 것과 같은 방식으로 post.pk를 작성하여 기본 키에 액세스합니다 
#post.pk를 써서 기본키에 접근할 수 있고 같은 방법으로 Post객체내 다른 필드(title, author)에도 접근할 수 있습니다!""

#render는 django.shortcuts 패키지에 있는 함수로서 첫번째 파라미터로 request를, 그리고 두번째 파라미터로 템플릿을,
#세번째로 context를 받는다. 말 그대로 문맥에 맞게 보여주겠다는 뜻.... 이걸 왜 아무도 안 가르쳐주지??

def post_new(request):
    if request.method == "POST":
        my_form = PostForm(request.POST)         
        if my_form.is_valid():
            print(my_form.cleaned_data)
            post = my_form.save(commit=False)       # DB에 바로 저장은 하지 않고 post변수에만 저장한 후에, post를 나중에 저장
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        my_form = PostForm()                             #request의 method가 POST가 아니면 my_form에 빈PostForm을 넣어라, 즉 비워라
    return render(request = request, template_name= 'blog/post_edit.html', context = {'my_form': my_form})

#{'앞의 form은 html에 있는 값':뒤에 my_form은 변수 } 다이내믹하게 보여주려고

#r여기서 save는 post.objects.create와 동일함.


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)         #수정하는 기능이니까 처음부터 특정글의 정보인 pk가 필요함/이른바 다이내믹 url이라서 get_object_or_404
    if request.method == "POST":
        my_form = PostForm(request.POST, instance=post)
# instance=post를 넣으면 기존 instace를 업데이트하고, 저걸 안 쓰면 새로 instance를 하나 만든다 그래서 post_new에는 없다
        if my_form.is_valid():
            post = my_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        my_form = PostForm(instance=post)
    return render(request = request, template_name= 'blog/post_edit.html', context={'my_form' : my_form,}) #다이내믹!!!

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)   #다이내믹 url
    post.delete()                           #if request.method == "POST":를 쓰고 싶은데 안 지워짐. post.delete() 하는건 GET리퀘스트라고 하네? 다음 기회에.... 
    return redirect('post_list')


def export_posts_excel(request):
    post_resource = PostResource()
    dataset = post_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response.write(u'\ufeff'.encode('utf8'))
    response['Content-Disposition'] = 'attachment; filename="posts_all.xls"'
    return response



def post_import(request):
    if request.method == 'POST':
        post_resource = PostResource()
        dataset = Dataset()
        new_posts = request.FILES['myfile']
        imported_data = dataset.load(new_posts.read())
        result = post_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            post_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'blog/post_import.html')



#NamuForm은 장고의 models.Form 클래스를 상속받은 클래스이므로 장고 Form클래스가 받는 인수인 request.GET을 받아서 부모클래스의 특성대로 인스턴스를 만들어
#search라는 인스턴스를 생성함

def namu_search_view(request):
    search = NamuForm(request.GET)
    if search.is_valid():
            url = 'https://www.namu.wiki/w/' + str(search.cleaned_data.get('search'))
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            wikiLinkInt = soup.select('.wiki-link-internal')
            search = []
            for link in wikiLinkInt: 
                thTitle = link.get('title')
                thRef = 'http://namu.wiki' + link.get('href') #주소가 특수문자로 나오는데 한글로 하면 오류남
                hyperlink = '<a href="' + thRef + '" target="_blank">' + thTitle + '</a>'
                search.append( hyperlink )
    return render(request = request, template_name= 'blog/namu_search.html', context= { 'search' : search })


#requests모듈로 스크래핑을 하면서 parameter를 넣어서 GET메소드로 보내보고 
#params = {'param1': 'value1', 'param2': 'value'} res = requests.get(URL, params=params)
#res.url명령어를 넣어보면 https://www.tistory.com/?param1=value1&param2=value 검색어를 url주소에 넣어서 같이 보내는것
#https://dgkim5360.tistory.com/entry/python-requests 이 사이트에서 설명해줌
#이제 되냐....???
#search = myNamuLink라고 해야됨!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


'''
cfe에서는 view에 있는 함수들을 아래와 같이 통일함. 깔끔해짐
def 함수이름_view(request, id(필요할경우))
    변수명 = 함수 or 쿼리셋
    context = {
        "html에서 쓸 이름" : 변수명
    }
#return render(request, "이동할주소.html", context)
'''