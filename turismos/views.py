from django.db.models import Count
from django.db.models.functions import TruncMonth
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


@user_passes_test(is_secretaria)
def dashboard(request):

    # 📊 KPIs
    pontos = PontoTuristico.objects.count()
    hoteis = Hotel.objects.count()
    restaurantes = Restaurante.objects.count()
    eventos = Evento.objects.count()

    total = pontos + hoteis + restaurantes + eventos

    aprovados = (
        PontoTuristico.objects.filter(aprovado=True).count() +
        Hotel.objects.filter(aprovado=True).count() +
        Restaurante.objects.filter(aprovado=True).count() +
        Evento.objects.filter(aprovado=True).count()
    )

    pendentes = total - aprovados


    # 📈 1. BUSCAR DADOS TEMPORAIS
    dados_temporais = Restaurante.objects.annotate(
        mes=TruncMonth('criado_em')
    ).values('mes').annotate(total=Count('id')).order_by('mes')


    # 🎯 2. FORMATAR PARA O GRÁFICO (AQUI 👇)
    labels = [d['mes'].strftime('%b/%Y') for d in dados_temporais]
    valores = [d['total'] for d in dados_temporais]


    # 📤 3. ENVIAR PARA O TEMPLATE
    context = {
        'total': total,
        'aprovados': aprovados,
        'pendentes': pendentes,
        'pontos': pontos,
        'hoteis': hoteis,
        'restaurantes': restaurantes,
        'eventos': eventos,

        # 👇 gráfico temporal
        'labels': labels,
        'valores': valores,
    }

    return render(request, 'dashboard.html', context)