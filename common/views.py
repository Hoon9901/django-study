from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm

# Create your views here.
def signup(request) :
    # 계정 생성
    if request.method == "POST": # 계정 생성
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # 회원가입 화면에서 입력한 값  얻는다.
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            # 자동 로그인
            user = authenticate(username = username , password = raw_password)
            login(request, user)
            return redirect('pybo:index')
    else :  # 회원가입 화면 반환
        form = UserForm()
    return render(request, 'common/signup.html', {'form' : form})
