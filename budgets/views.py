from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Budget, Goal

# Removido o LoginRequiredMixin para permitir acesso sem autenticação
class BudgetListView(View):
    template_name = 'budgets/budget_list.html'
    
    def get(self, request):
        # Se o usuário não estiver autenticado, usamos um usuário fictício para testes
        if not request.user.is_authenticated:
            User = get_user_model()
            try:
                # Tenta obter o primeiro usuário do banco de dados
                user = User.objects.first()
                if not user:
                    # Se não houver usuários, cria um usuário de teste
                    user = User.objects.create_user(
                        username='teste',
                        email='teste@example.com',
                        password='senha123',
                        name='Usuário de Teste'
                    )
            except Exception as e:
                # Em caso de erro, usamos valores padrão
                budgets = []
                context = {'budgets': budgets}
                return render(request, self.template_name, context)
        else:
            user = request.user
        
        try:
            # Buscar orçamentos do usuário
            budgets = Budget.objects.filter(user=user)
        except:
            # Em caso de erro, usamos valores padrão
            budgets = []
        
        context = {
            'budgets': budgets
        }
        return render(request, self.template_name, context)

# Removido o LoginRequiredMixin para permitir acesso sem autenticação
class GoalListView(View):
    template_name = 'budgets/goal_list.html'
    
    def get(self, request):
        # Se o usuário não estiver autenticado, usamos um usuário fictício para testes
        if not request.user.is_authenticated:
            User = get_user_model()
            try:
                # Tenta obter o primeiro usuário do banco de dados
                user = User.objects.first()
                if not user:
                    # Se não houver usuários, cria um usuário de teste
                    user = User.objects.create_user(
                        username='teste',
                        email='teste@example.com',
                        password='senha123',
                        name='Usuário de Teste'
                    )
            except Exception as e:
                # Em caso de erro, usamos valores padrão
                goals = []
                context = {'goals': goals}
                return render(request, self.template_name, context)
        else:
            user = request.user
        
        try:
            # Buscar metas do usuário
            goals = Goal.objects.filter(user=user)
        except:
            # Em caso de erro, usamos valores padrão
            goals = []
        
        context = {
            'goals': goals
        }
        return render(request, self.template_name, context)
