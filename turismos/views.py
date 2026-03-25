from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


@login_required
def cadastrar_restaurante(request):
    if request.method == 'POST':
        form = RestauranteForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.criado_por = request.user
            obj.save()
            return redirect('home')
    else:
        form = RestauranteForm()

    return render(request, 'form.html', {'form': form})