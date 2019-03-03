from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text']

#다시 보니까 "model = Post"이부분을 보면 PostFrom은 modle의 Post클래스를 만드는 클래스가 됨 즉, 메타클래스 그래서 class Meta가 된듯


'''
model = Post => import해온 models.py에 있는 Post모델을 사용하겠다
fields = ['모델의 데이터필드 중에 필요한 것 1','2']
마지막 줄을 fields = '__all__' 로 하면 모델이 모든 필드를 사용
여기서 만들어진 PostForm을 Post_edit.html에서 가져다가 화면에 보여주며,
views에서도 Post_new와 Post_edit 함수에서 불러다가 사용함. 존나 물고 물리네
If you’re building a database-driven app, chances are you’ll have forms that map closely to Django models. 
데이터베이스에 기반한 응용프로그램에서의 form은 장고의 models와 밀접한 관계일 수 밖에 없다
For instance, you might have a BlogComment model, and you want to create a form that lets people submit comments. 
In this case, it would be redundant to define the field types in your form, 
because you’ve already defined the fields in your model.
For this reason, Django provides a helper class that lets you create a Form class from a Django model
이미 모델 안에 필드를 정의해놓았을 것이다. 이런 연유로 장고는 모델로부터 form클래스를 불러와서 만들 수 있게 해준다.
여기서는 PostForm을 만들기 위헤 models에서 Post를 import했음
'''