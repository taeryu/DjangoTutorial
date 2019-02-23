from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
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

# 'post' : post dlrp anjdla ㅇㅣ게 뭐임??

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {
        'form' : form,

    })