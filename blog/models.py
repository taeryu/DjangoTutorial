from django.db import models
from django.utils import timezone

#장고 쉘(가상환경에서 python manage.py shell)에서 from blog.Post import Post하고, obj = Post.object.get(id=1)후에 dir(obj)해서 
#파이썬 기본함수인 dir을 통해 해당 객체의 메쏘드와 어트리뷰트를 찾아보고 놀아라
#예를 들어 obj4 = Post.objects.get(pk=4)하면 Shinozaki Ai bang이 나오고 dir(obj4)하면 해당하는 메소드나 attr이 나오는데 
#그중에는 published_date가 포함되어 있다. 그걸 아래의 함수에서 사용한다

#팁 : Post라고 하지말고 Post_Model이라고 써라

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    #upload = models.FileField(null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # __str__ => 이걸 안하면 admin에서 글 목록에 Post.object라고만 나오고 글의 제목이 안보인다.
    # __str__는 object 자체의 제목값을 문자열로 return하게 하는 것

    def __str__(self):
        return self.title

class Search(models.Model):
    search = models.CharField(max_length=30)


#Search모델을 만들긴 했지만 http의 request method가 GET이므로 Search.objects.all()로 검색해도 안나옴
#모델을 만든건 Form을 생성하기 위함이었으나 실제로 DB에 저장은 안됨. I got exactly what I want!!

#클래스는 빵틀같은거 - 상속이 가능하고, 인스턴스를 만들어낸다. Post클래스는 장고의 Model클래스를 상속받아서,
#Post인스턴스를 만드는데 author, title, text, created_date, published_date 등의 속성을 미리 정한 인스턴스를 만들어낸다.
#publish는 클래스 내의 함수이므로 메써드이다. 메써드의 인수는 self이고, self.속성/함수로 적는다. 자기 스스로가 인수이므로
#__str__는 특수 메써드인데, str형태로 바꿔준다. 근데 왜 타이틀만 string으로 바꾸지??

#얘네는 뭘까...??? Post클래스에서 만든 함수이므로 published_date의 속성을 상속받는다. 장고의 DateTimeField의 속성을 물려받은 인스턴스를 만드나?
#dir(obj)해보면 title, published_date랑 publish가 나옴. 즉 해당 함수를 사용해서 개시할 수 있다는 것
#obj = Post.objects.all() -> type(obj)결과는 쿼리셋 리스트인 반면
#obj4 = Post.objects.get(pk=4) -> type(obj4)의 결과는 blog.models.Post이므로 Post클래스가 만든 인스턴스(객체)다!!!!!! 와~~~
#얘도 마찬가지??