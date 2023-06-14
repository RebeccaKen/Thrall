from django.shortcuts import render


# Create your views here.
def get_thrall_list(request):
    return render(request, 'thrall/thrall_list.html')
