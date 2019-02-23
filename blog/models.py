from django.db import models
from django.utils import timezone

#어떻게 데이터를 저장할 것이라고 정의한 것 db를 sqllite3로 만드는 중
#아래의 클래스에서 작성자, 제목, 내용, 작성일, 발행일의 "속성"그 밑에 함수로 "메서드를 만듦"
#즉 해당 클래스의 특성은 author~published_date에서 정의했고, '행동'은 그 밑의 def에서 정의함.
#publish함수는 '현재의 타임존'을 published_date 변수에 넣고 저장하는 행동이고,
#__str__는 제목값을 반환하는 행동을 하도록 함
#클래스에는 속성과 행동을 둘다 넣을 수 있다? 객체 지향?


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