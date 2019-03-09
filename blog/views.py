from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post
from .forms import PostForm, NamuForm
from django.shortcuts import redirect
import csv
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd

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

#여기서 request를 넣고, html주소를 넣고 마지막으로 post_list는 앞에서 정의한 qs다 라고 딕셔너리를 만들었음
#이 딕셔너리 혹은 context를 활용해서 blog/post_list.html에서 for루프로 render(화면에 띄워줄)하려는 목적으로!!! 이제 좀 감이 잡힘
#중요!!!! : {key:value}로 딕셔너리 형태로 만든걸 context라고 함. html에서도 사용한바 있음. 즉 {{ request.user }}에서 문맥에 따라 내용이 바뀜
#그래서 위의 함수에서 {'post_list' : qs,}라고 써놓고, blog/post_list.html에서 {{ post_list }}라고 context를 넣어준것. 
#정확하게는 그 이후에 {{ for post in post_list }}라고 넣어줌.즉 포스트 리스트가 list type이므로 for문으로 하나씩 꺼내준 것. 
#이걸 왜 아무도 안 가르쳐줌...

def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)    #ORM으로 pk를 get했음.,,,,
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
#commit=false는 공식문서에는 바로 저장하지 않고 나중에 한다는 뜻이라고 써있다고 한다 
#데이터베이스에서 커밋은 아직 메모리나 큐에만 머물러 있는 수정된 내용을 "데이터베이스에 저장한"다는 의미입니다.

def post_new(request):
    if request.method == "POST":
        my_form = PostForm(request.POST)         
        if my_form.is_valid():
            print(my_form.cleaned_data)             #이렇게 하고 글을 쓰면 서버 커맨드 창에 글이 나타남
            post = my_form.save(commit=False)      #아 그니까 이러면 DB에 저장은 하지 않고 post변수에만 저장한 후에, post를 나중에 저장한다는 것
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)    #그냥 이렇게 쓰는듯 왜 두번 저장하는지 아무도 안 가르쳐줌 그냥 외워
    else:                                                #form은 장고의 화면에 보이는 form이고 이거를 다시 post로 받아서 저장하는건가?
        my_form = PostForm()                             #request의 method가 POST가 아니면 my_form에 빈PostForm을 넣어라, 즉 비워라
    return render(request = request, template_name= 'blog/post_edit.html', context = {'form': my_form})
#{'앞의 form은 html에 있는 값':뒤에 my_form은 변수 } 다이내믹하게 보여주려고

#왜 저장을 두번하고 commit=false냐면
#https://stackoverflow.com/questions/12848605/django-modelform-what-is-savecommit-false-used-for 얘네도 잘모르는듯.....
#https://wayhome25.github.io/django/2017/05/06/django-model-form/ 유저네임과 발행일을 모아서 한꺼번에 저장하려고 지연시킨다!!!!
#왜냐면 비주얼스튜디오코드에도 그냥 이렇게 써있음
#def log_message(request):
#    form = LogMessageForm(request.POST or None)
#
#   if request.method == "POST":
#        if form.is_valid():
#            message = form.save(commit=False)
#            message.log_date = datetime.now()
#            message.save()
#            return redirect("home")
#    else:
#        return render(request, "hello/log_message.html", {"form": form})


#request.POST를 저장하는게 대부분의 글 작성 views의 메인 목적인듯. 여기서 save는 post.objects.create와 동일함.
#다시 말해서 PostForm의 폼 클래스에다가 request.POST인수를 넣으면 만들어지는 my_form이라는 인스턴스를 만들어서,
#이걸 post라는 object에 넣는다. 그러면 그 object의 attr. 예를들어 author는 request의 attr.중 user를 저장하고
#post.의 published_date에는 현재 시각을 저장해서, 
#다시 그 post 오브젝트 자체를 저장함. 오브젝트를 저장하는 것과 데이터를 db에 저장하는 것의 차이?? 왜 두번함????

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)         #수정하는 기능이니까 처음부터 특정글의 정보인 pk가 필요/이른바 다이내믹 url이라서 get_object_or_404
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
    return render(request = request, template_name= 'blog/post_edit.html', context={'form' : my_form,}) #다이내믹!!!

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)  #다이내믹 url
    post.delete()                           #if request.method == "POST":를 쓰고 싶은데 안 지워짐. post.delete() 하는건 GET리퀘스트라고 하네? 다음 기회에.... 
    return redirect('post_list')

#csv파일로 전체 글목록 출력하기

def export_posts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'

    writer = csv.writer(response)
    writer.writerow(['author', 'title', 'created_date', 'published_date'])

    posts = Post.objects.all().values_list('author', 'title', 'created_date', 'published_date')
    for post in posts:
        writer.writerow(post)
    return response

#NamuForm은 클래스임, 그러면 search는 인스턴스임
 
def namu_search_view(request):
    search = NamuForm(request.GET)                             
    if search.is_valid():
            url = 'https://www.namu.wiki/w/' + str(search.cleaned_data.get('search'))
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            wikiLinkInt = soup.select('.wiki-link-internal')
            myNamuLink = []
            for link in wikiLinkInt: 
                thTitle = link.get('title')
                #thRef_ko = 'http://namu.wiki/w' + thTitle
                thRef = 'http://namu.wiki' + link.get('href') #이렇게 하면 주소가 특수문자로 나오는데 위와 같이 하면 한글로 표기됨
                myNamuLink.append((thTitle,thRef))
            print(myNamuLink)
    return render(request = request, template_name= 'blog/namu_search.html', context= { 'search' : myNamuLink })  #여기서 search는 건들지마라


'''
    if request.method == "POST":
        my_form = NamuForm(request.POST)
        print(my_form.cleaned_data)
        search = my_form.save(commit=False)
        return redirect('post_detail', pk=post.pk)    
    return render(request, 'blog/post_edit.html', {'form': my_form})
#{'앞의 form은 html에 있는 값':뒤에 my_form은 변수 } 다이내믹하게 보여주려고
'''

'''
cfe에서는 view에 있는 함수들을 아래와 같이 통일함. 깔끔해짐
def 함수이름_view(request, id(필요할경우))
    변수명 = 함수 or 쿼리셋
    context = {
        "html에서 쓸 이름" : 변수명
    }
#return render(request, "이동할주소.html", context)
'''