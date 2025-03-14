from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views import View
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model

def profile_view(request):
    return render(request, 'users/profile.html')

class RegisterView(View):
    template_name = 'users/register.html'
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        # Imprimindo dados recebidos do formulário
        print("="*50)
        print("DADOS RECEBIDOS DO FORMULÁRIO:")
        print(f"Método da requisição: {request.method}")
        print(f"Dados POST: {request.POST}")
        
        if 'username' in request.POST:
            print(f"Email digitado: {request.POST['username']}")
        else:
            print("Campo 'username' não foi recebido!")
            
        if 'password' in request.POST:
            print(f"Senha foi recebida (não mostrada por segurança)")
        else:
            print("Campo 'password' não foi recebido!")
        print("="*50)
        
        # Processamento normal do formulário
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Formulário é válido!")
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Log para verificar usuário no banco
            User = get_user_model()
            try:
                user_obj = User.objects.get(email=email)
                print(f"Usuário existe no banco: {user_obj.email}")
                print(f"Username no banco: {user_obj.username}")
                
                # Verifique se o usuário pode fazer login
                if not user_obj.is_active:
                    print("ALERTA: Usuário está inativo!")
            except User.DoesNotExist:
                print(f"ERRO: Usuário com email {email} não existe no banco!")
            
            # Tente autenticar
            user = authenticate(username=email, password=password)
            print(f"Autenticação retornou: {user}")
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo de volta!")
                return redirect('dashboard')
            else:
                messages.error(request, "Email ou senha inválidos.")
        else:
            print(f"Formulário inválido. Erros: {form.errors}")
            
        return render(request, self.template_name, {'form': form})

class DashboardView(View):
    template_name = 'users/dashboard.html'
    
    def get(self, request):
        # Dados de exemplo para o dashboard
        context = {
            'value': {'amount': 30000, 'percent': 4.6},
            'users': {'amount': 50021, 'percent': 2.5},
            'orders': {'amount': 45021, 'percent': 3.1},
            'tickets': {'amount': 20516, 'percent': 3.1},
            'active_users': 81
        }
        return render(request, self.template_name, context)

