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
