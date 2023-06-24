from django.shortcuts import render


# Create your views here.
def get_thrall_list(request):
    return render(request, 'thrall/thrall_list.html')


def index(request):
    """ A view to return the index page """

    return render(request, 'thrall/index.html')