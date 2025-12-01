from django.shortcuts import render
from profiles.models import ProfileModel

def about_view(request):
    context = {}
    if request.user.is_authenticated:
        try:
            context['profile'] = ProfileModel.objects.get(user=request.user)
        except ProfileModel.DoesNotExist:
            pass
    return render(request, 'about/about.html', context)
