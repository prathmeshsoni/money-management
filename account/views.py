from django.shortcuts import render, redirect
from .forms import AccountForm
from .models import AccountModel
from management.models import ManageModel
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import AccountSerialize
from django.http import JsonResponse
from management.views import check_avil
from django.contrib import messages
from django.contrib.auth.models import User


def cat_page(request):
    user2 = request.session.get('private_admin')
    user_obj = User.objects.get(username=user2)
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            jj = AccountModel.objects.get(id=id)
            d = AccountForm(request.POST or None, request.FILES or None, instance=jj)
            check = 1
        except:
            d = AccountForm(request.POST or None, request.FILES or None)
            check = 0
        if d.is_valid():
            unique_field_value = d.cleaned_data['account_name'].lower()
            existing_records = AccountModel.objects.filter(account_name__iexact=unique_field_value, user=user_obj)

            if check == 1:
                if existing_records.exists() and int(id) != int(existing_records[0].id):
                    messages.error(request, 'Account Already Exists. ❌')
                    return redirect('/account/')
                else:
                    d.save()
                    messages.warning(request, 'Data Updated Successfully ✔')
                    return redirect('/account/')
            else:
                if existing_records.exists():
                    messages.error(request, 'Account Already Exists. ❌')
                    return redirect('/account/')
                else:

                    private_data = d.save(commit=False)
                    private_data.user = user_obj
                    private_data.save()
                    messages.success(request, 'Data Saved Successfully ✔')
                    return redirect('/account/')
        else:
            messages.error(request, "Account Already Exists.")
            return redirect('/account/')
    else:
        d = AccountForm()
        b = AccountModel.objects.filter(user=user_obj)
        data_list = []
        for i in b:
            c = check_avil(user_obj, i.account_name)
            data_list.append(c[0])
        x = {
            'm': d,
            'list': data_list,
            'cat_master': 'master',
            'cat_active': 'account_master',
            'category': 'Account',
            'type_nam': 'account_name'
        }
        return render(request, "admin/filter.html", x)


@api_view(['POST'])
def updateCat(request):
    id = request.POST.get('id')
    get_data = AccountModel.objects.get(id=id)
    serializer = AccountSerialize(get_data)
    return Response(serializer.data)


def remove_cat(request):
    if request.method == 'POST':
        try:
            hid = request.POST.get('id')
            obj = AccountModel.objects.get(id=hid)
            name = obj.account_name
            aa = ManageModel.objects.filter(account=hid)
            aa_count = aa.count()
            if int(aa_count) == 0:
                confirm_delete = request.POST.get('confirm_delete')
                if int(confirm_delete) == 0:
                    obj.delete()
                    a = {'status': True, 'exists': 'done', 'name': name}
                    return JsonResponse(a)
                # messages.success(request,"Delete successfully ✔")
                a = {'status': True, 'exists': 'confirmdelete', 'name': name}
                return JsonResponse(a)
            else:
                a = {'status': True, 'exists': 'orderexist', 'name': name}
                return JsonResponse(a)
        except:
            a = {'status': True, 'exists': 'error'}
            return JsonResponse(a)
    else:
        return redirect('/account/')