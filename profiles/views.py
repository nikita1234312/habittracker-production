from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from .models import ProfileModel


@login_required
def profileView(request):
    profile, created = ProfileModel.objects.get_or_create(user=request.user)
    profile.refresh_from_db()
    return render(request, 'profiles/profile.html', {'profile': profile})

@login_required
def profile_edit_view(request):
    profile, created = ProfileModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Перенаправляем на страницу профиля
            return redirect('profile')  # ← Это вызовет profileView с обновленными данными
    
    form = ProfileEditForm(instance=profile)

    context = {
        'profile': profile,
        'user': request.user,
        'form': form,
        'request': request
    }

    return render(request, 'profiles/profile.html', context)