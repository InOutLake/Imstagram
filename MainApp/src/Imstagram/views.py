from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Image
from os import path
from .forms import AddImageForm

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            user = authenticate(username="test_user", password="test_password")
            login(request, user)
        images = Image.objects.filter(image_owner=request.user)
        return render(request, 'profile.html', {'images': images})
    
    def post(self, request):
        pass

class AddNewImage(View):
    def get(self, request):
        form = AddImageForm()
        return render(request, "AddNewImage.html", { 'form': form })
    
    def post(self, request):
        form = AddImageForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "AddNewImage.html", { 'form': form })
        image = form.save(commit=False)
        image.image_owner = request.user
        image.save()
        return redirect('imstagram:profile')
        