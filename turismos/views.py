from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.decorators import user_passes_test

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


def is_secretaria(user):
    return user.tipo == 'SECRETARIA'


@user_passes_test(is_secretaria)
def aprovar_restaurante(request, id):
    restaurante = Restaurante.objects.get(id=id)
    restaurante.aprovado = True
    restaurante.save()
    return redirect('painel_secretaria')

def lista_restaurantes(request):
    restaurantes = Restaurante.objects.filter(aprovado=True)
    return render(request, 'lista.html', {'restaurantes': restaurantes})


def home(request):
    pontos = PontoTuristico.objects.filter(aprovado=True)
    return render(request, 'home.html', {'pontos': pontos})


def mapa(request):
    restaurantes = Restaurante.objects.filter(aprovado=True)
    return render(request, 'mapa.html', {'restaurantes': restaurantes})


@login_required
def painel_comerciante(request):
    meus = Restaurante.objects.filter(criado_por=request.user)
    return render(request, 'painel_comerciante.html', {'meus': meus})


@user_passes_test(is_secretaria)
def painel_secretaria(request):
    pendentes = Restaurante.objects.filter(aprovado=False)
    return render(request, 'painel_secretaria.html', {'pendentes': pendentes})