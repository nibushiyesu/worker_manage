from django.core.validators import RegexValidator
from django.shortcuts import render, redirect

# Create your views here.

from app01 import models


def depart_list(req):
    # models.Department.objects.create(title='宣传部')
    # models.Department.objects.create(title='实践部')
    # models.Department.objects.create(title='秘书处')
    depart = models.Department.objects.all()
    return render(req, 'depart_list.html', {'depart': depart})


def depart_add(req):
    if req.method == 'GET':
        return render(req, 'depart_add.html')

    dep = req.POST.get("dep")
    models.Department.objects.create(title=dep)
    return redirect("/depart/list/")


def depart_delete(req):
    nid = req.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def depart_edit(req, nid):
    if req.method == 'GET':
        depart = models.Department.objects.filter(id=nid).first()
        print(depart.id, depart.title)
        return render(req, 'depart_edit.html', {"depart": depart})

    title = req.POST.get('title')
    print(title)
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')


def user_list(req):
    # models.UserInfo.objects.create(name='zkm', password='123', age='20', account='120', create_time='2022-11-11',
    #                                gender='1', depart_id=1)
    user = models.UserInfo.objects.all()
    # for u in user:
    #     print(u.id, u.get_gender_display(), u.depart.title)
    return render(req, 'user_list.html', {'user_list': user})


from django import forms


class UserModelForm(forms.ModelForm):
    # name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'gender', 'depart', 'create_time']

        # widgets = {
        #     'name': forms.TextInput(attrs={"class": "form-control"})
        #     'password': forms.TextInput(attrs={"class": "form-control"})
        #     'age': forms.TextInput(attrs={"class": "form-control"})
        # }

    # 与mata类是同级的
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环所有插件，添加class属性
        for name, field in self.fields.items():
            # print(name, field)
            # widget 没有s
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}


def user_add(req):
    """ 添加用户 """
    if req.method == "GET":
        form = UserModelForm
        return render(req, 'user_add.html', {'form': form})

    form = UserModelForm(data=req.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 保存到数据库
        form.save()
        return redirect('/user/list/')

    # 校验失败，返回错误信息， 此时的form不同于get时的form
    return render(req, 'user_add.html', {'form': form})


def user_edit(req, nid):
    # 获取输入框显示数据
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    if req.method == 'GET':
        # 获取当前的修改信息

        form = UserModelForm(instance=row_obj)
        return render(req, 'user_edit.html', {'form': form})

    # 添加instance, 变成更新数据，而不是添加数据

    form = UserModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        # 额外添加点
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')

    # 校验失败
    return render(req, 'user_add.html', {'form': form})


def user_delete(req, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(req):
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18736826584")
    data_dict = {}
    # get请求
    search_data = req.GET.get("q", "")
    if search_data:
        data_dict["mobile__contains"] = search_data
    # 分页显示
    page = int(req.GET.get("page", "1"))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[start:end]
    return render(req, 'pretty_list.html', {"queryset": queryset, "search_data": search_data})


from django import forms
from django.core.exceptions import ValidationError


class PrettyModelForm(forms.ModelForm):
    # disabled = True,
    # mobile = forms.CharField(label='手机号',validators=[RegexValidator(r'^1[3-9\d{9}$', '手机号格式错误'), ], )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

        # fields = "__all__"

        # 排除字段
        # exclude = ['status']

    # 定义input样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环所有插件，添加class属性
        for name, field in self.fields.items():
            # print(name, field)
            # widget 没有s
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}

    # 验证方式2： 钩子方法 校验信息
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exist = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()

        if exist:
            raise ValidationError("手机号已存在")

        # if len(txt_mobile) != 11:
        #     raise ValidationError("格式错误")

        # 如果验证通过,返回填写的的手机号
        return txt_mobile


def pretty_add(req):
    if req.method == 'GET':
        form = PrettyModelForm()
        return render(req, 'pretty_add.html', {'form': form})

    # 获取post数据
    form = PrettyModelForm(data=req.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 保存到数据库
        form.save()
        return redirect('/pretty/list/')

    # 校验失败
    return render(req, 'pretty_add.html', {'form': form})


class PrettyEditModelForm(forms.ModelForm):
    # 格式校验 disabled=True,
    # mobile = forms.CharField(label='手机号',
    #                          validators=[RegexValidator(r'^1[3-9\d{9}$', '手机号格式错误'), ], )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

        # fields = "__all__"
        # 排除字段
        # exclude = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环所有插件，添加class属性
        for name, field in self.fields.items():
            # print(name, field)
            # widget 没有s
            # 给输入框添加样式
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}

    # 编辑手机号的验证规则
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # primaryKey
        exist = models.PrettyNum.objects.exclude(self.instance.pk).filter(mobile=txt_mobile).exists()

        if exist:
            raise ValidationError("手机号已存在")
        # if len(txt_mobile) != 11:
        #     raise ValidationError("格式错误")
        # 返回修改过后的手机号
        return txt_mobile


def pretty_edit(req, nid):
    """# 修改靓号"""
    # 填充当前修改的信息
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if req.method == 'GET':
        form = PrettyEditModelForm(instance=row_obj)
        return render(req, 'pretty_edit.html', {'form': form})
    # 提交的时候不是新增一条数据，而是修改数据
    form = PrettyEditModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    # 返回错误页面
    return render(req, 'pretty_edit.html', {'form': form})


def pretty_delete(req, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')


def user_login(req):
    if req.method == 'GET':
        return render(req, 'user_login.html')

    return redirect('/user/list')


def recharge_list(req):
    return render(req, 'user_recharge_list.html')


# class UserRechargeModelForm(forms.ModelForm):
#     # name = forms.CharField(min_length=3, label="用户名")
#
#     class Meta:
#         model = models.recharge
#         fields = ['name', 'password', 'age', 'gender', 'depart', 'create_time']
#
#         # widgets = {
#         #     'name': forms.TextInput(attrs={"class": "form-control"})
#         #     'password': forms.TextInput(attrs={"class": "form-control"})
#         #     'age': forms.TextInput(attrs={"class": "form-control"})
#         # }
#
#     # 与mata类是同级的
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 循环所有插件，添加class属性
#         for name, field in self.fields.items():
#             # print(name, field)
#             # widget 没有s
#             field.widget.attrs = {"class": "form-control", 'placeholder': field.label}
#
#
# def user_recharge(req):
#     ''' 用户充值界面'''
#     if req.method == "GET":
#         form = UserRechargeModelForm
#         return render(req, 'user_recharge.html', {'form': form})
#
#     form = UserRechargeModelForm(data=req.POST)
#     if form.is_valid():
#         # print(form.cleaned_data)
#         # 保存到数据库
#         form.save()
#         return redirect('/user/recharge/list')
#
#     # 校验失败，返回错误信息， 此时的form不同于get时的form
#     return render(req, 'user_recharge.html', {'form': form})


def chart_list(req):
    return render(req, 'chart_list.html')
