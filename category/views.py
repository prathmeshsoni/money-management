from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import CategoryModel
from management.models import ManageModel
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import CategorySerialize
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User


def cat_page(request):
    user = request.session.get('private_admin')
    user_obj = User.objects.get(username=user)
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            jj = CategoryModel.objects.get(id=id)
            d = CategoryForm(request.POST or None, request.FILES or None, instance=jj)
            check = 1
        except:
            d = CategoryForm(request.POST or None, request.FILES or None)
            check = 0
        print(d)
        if d.is_valid():
            unique_field_value = d.cleaned_data['cat_name'].lower()
            existing_records = CategoryModel.objects.filter(cat_name__iexact=unique_field_value, user=user_obj)
            if check == 1:
                if existing_records.exists() and int(id) != int(existing_records[0].id):
                    messages.error(request, 'Category Already Exists. ❌')
                    return redirect('/category/')
                else:
                    d.save()
                    messages.warning(request, 'Data Updated Successfully ✔')
                    return redirect('/category/')
            else:
                if existing_records.exists():
                    messages.error(request, 'Category Already Exists. ❌')
                    return redirect('/category/')
                else:
                    private_data = d.save(commit=False)
                    private_data.user = user_obj
                    private_data.save()
                    messages.success(request, 'Data Saved Successfully ✔')
                    return redirect('/category/')

        else:
            messages.error(request, "Category Already Exists. ❌")
            return redirect('/category/')

    else:
        d = CategoryForm()
        b = CategoryModel.objects.filter(user=user_obj)
        x = {
            'm': d,
            'list': b,
            'cat_master': 'master',
            'cat_active': 'cat_master',
            'category': 'Category',
            'type_nam': 'cat_name'

        }
        return render(request, "admin/filter.html",x)


@api_view(['POST'])
def updateCat(request):
    id = request.POST.get('id')
    get_data = CategoryModel.objects.get(id=id)
    serializer = CategorySerialize(get_data)
    return Response(serializer.data)


def remove_cat(request):
    if request.method == 'POST':
        try:
            hid = request.POST.get('id')
            obj = CategoryModel.objects.get(id = hid)
            name = obj.cat_name
            aa = ManageModel.objects.filter(category=hid)
            aa_count = aa.count()
            if int(aa_count) == 0:
                confirm_delete = request.POST.get('confirm_delete')
                if int(confirm_delete) == 0:
                    obj.delete()
                    a = {'status': True,'exists':'done', 'name':name}
                    return JsonResponse(a)
                # messages.success(request,"Delete successfully ✔")
                a = {'status': True,'exists':'confirmdelete', 'name': name}
                return JsonResponse(a)
                # return redirect('/user/address/')
            else:
                a = {'status': True,'exists':'orderexist', 'name': name}
                return JsonResponse(a)
        except:
            a = {'status': True,'exists':'error'}
            return JsonResponse(a)
    else:
        return redirect('/category/')