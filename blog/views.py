from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post
#view가 장고에서 사용자의 url요청을 받아서 해당하는 페이지를 보내는 함수 부분

def post_list(request):
    qs = Post.objects.all()
    qs = qs.filter(published_date__lte=timezone.now())
    qs = qs.order_by('published_date')
    
#위의 qs는 이거를 쪼갠거  Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {
        'post_list' : qs,

})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
#    try:
#        post = Post.objects.get(pk=pk) #앞의 pk는 필드명을 뜻하고 뒤의 pk는 인자로 받은 pk 변수이다!!!!!!!! 얼마나 쉬운가ㅜㅜㅜㅜ 이게 뭔소리야
#    except Post.DoesNotExist:
#        raise Http404
    return render(request, 'blog/post_detail.html', {
        'post' : post,

    })

# render는 django.shortcuts 패키지에 있는 함수로서 첫번째 파라미터로 request를, 그리고 두번째 파라미터로 템플릿을 받아들인다. 

# 'post' : post dlrp anjdla