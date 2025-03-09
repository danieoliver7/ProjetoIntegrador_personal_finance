from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views import View
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

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
        # Adicione logs para depuração
        print("POST data:", request.POST)
        
        form = CustomAuthenticationForm(request, data=request.POST)
        
        # Verifique se o formulário é válido e por que não é
        if not form.is_valid():
            print("Form errors:", form.errors)
        
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            
            # Debug authentication
            print("Authenticate result:", user)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo de volta!")
                return redirect('dashboard')
            else:
                messages.error(request, "Email ou senha inválidos.")
        return render(request, self.template_name, {'form': form})

class DashboardView(LoginRequiredMixin, View):
    template_name = 'users/dashboard.html'
    login_url = 'login'  # Redireciona para login se o usuário não estiver autenticado
    
    def get(self, request):
        # Aqui você pode adicionar contexto adicional se necessário
        return render(request, self.template_name)

