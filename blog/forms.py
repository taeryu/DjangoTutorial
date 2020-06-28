from django import forms
from .models import Post, Search

#PostForm클래스에서 forms와 ModelForm이라는 두개의 클래스를 매개변수로 받고, 그 안에서 Meta라는 클래스를 다시 만들었으므로 내가 이해 못하는게 당연함.
#파이썬은 함수의 인자로 함수를 받고 클래스의 인자로 클래스를 받고 뭐 그럼. 함수안에서 다시 함수를 정의하고 클래스 안에서 다시 클래스를 정의하고 막 그럼.
#이해못하는게 맞음

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text']


class NamuForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = ['search']


#메타클래스 : 파이썬에서는 클래스도 객체니까 클래스에서 클래스를 받아올 수 있다.
# PostForm(forms.ModelForm) 이런 식으로 클래스 자체가 객체이므로 함수의 인수로 쓰이고 변수에 할당하고 클래스의 인수로도 쓰고 다 한다
#따라서 클래스의 클래스인 메타클래스란, 클래스를 만드는 클래스다. 클래스가 만든 인스턴스가 또다른 클래스인 것.
#ModelForm을 쓰면 무지껀 class Meta: 로 써야됨. 커스텀 폼은 바로 name = 뭐뭐뭐 이렇게 가능

'''
model = Post => import해온 models.py에 있는 Post모델을 model이라는 변수에 할당하겠다.
fields = ['모델의 데이터필드 중에 필요한 것 1','2']
마지막 줄을 fields = '__all__' 로 하면 모델이 모든 필드를 사용

이미 모델 안에 필드를 정의해놓았을 것이다. 이런 연유로 장고는 모델로부터 form클래스를 불러와서 만들 수 있게 해준다.
여기서는 PostForm을 만들기 위헤 models에서 Post를 import했음
'''