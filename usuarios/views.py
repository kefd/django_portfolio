from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Usuario
import hashlib

def cadastro(request):
  status = request.GET.get('status')
  return render(request, 'cadastro.html', {
    'status': status
  })

def login(request): 
  return render(request, 'login.html')

def valida_cadastro(request):
  nome = request.POST.get('nome')
  email = request.POST.get('email')
  senha = request.POST.get('senha')
  usuario_existe = Usuario.objects.filter(email=email)

  if len(senha) < 8 or len(senha) > 12:
    return redirect('/auth/cadastro?status=1')
  if len(nome.strip()) == 0 or len(email.strip()) == 0:
    return redirect('/auth/cadastro?status=2')
  if len(usuario_existe) > 0:
    return redirect('/auth/cadastro?status=3')
  
  senha = hashlib.sha256(senha.encode()).hexdigest()
  try:
    usuario = Usuario(
      nome=nome,
      senha=senha, email=email
    )
    usuario.save()
    return redirect('/auth/cadastro?status=0')
  except:
    return HttpResponse('ERRO INTERNO DO SISTEMA. TENTE NOVAMENTE EM INSTANTES')
