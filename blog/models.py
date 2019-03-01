from django.db import models
from django.utils import timezone


#해당 클래스의 특성은 author~published_date에서 정의했고, '행동'은 그 밑의 def에서 정의함.
#publish함수는 '현재의 타임존'을 published_date 변수에 넣고 저장하는 행동이고,
#__str__는 제목값을 반환하는 행동을 하도록 함
#Django의 models 클래스를 불러왔는데 models에는 미리 정해놓은 필드타입(CharField따위)이 있다. 
#작성자(author)는 ForeignKey(ManyToOne), 제목은 CharField로 글자제한을 200개로 해놓았고, 내용은 TextField로 정했고 작성일,발행일을 현재로 정해놨다
 


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

