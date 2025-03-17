from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Balance, Transaction, Category, PaymentMethod
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

# Create your views here.

# Removido o LoginRequiredMixin para permitir acesso sem autenticação
class BalanceCreateView(View):
    template_name = 'transactions/balance_form.html'
    
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
                # Em caso de erro, cria um objeto fictício para testes
                from types import SimpleNamespace
                user = SimpleNamespace(id=1, email='teste@example.com', name='Usuário de Teste')
        else:
            user = request.user
            
        # Verificar se já existe um saldo para o usuário
        try:
            current_balance = Balance.get_current_balance(user)
        except:
            current_balance = None
            
        context = {
            'current_balance': current_balance
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        amount = request.POST.get('amount')
        notes = request.POST.get('notes', '')
        
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
                # Em caso de erro, redireciona para o dashboard
                messages.error(request, "Erro ao criar usuário de teste.")
                return redirect('dashboard')
        else:
            user = request.user
        
        try:
            amount = float(amount)
            
            # Criar novo registro de saldo
            balance = Balance.objects.create(
                user=user,
                amount=amount,
                date=timezone.now().date(),
                notes=notes
            )
            
            messages.success(request, f"Saldo de R$ {amount:.2f} adicionado com sucesso!")
            return redirect('dashboard')
        except ValueError:
            messages.error(request, "Valor inválido. Por favor, informe um número válido.")
            return redirect('balance_create')

# Removido o LoginRequiredMixin para permitir acesso sem autenticação
class TransactionListView(View):
    template_name = 'transactions/transaction_list.html'
    
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
                transactions = []
                income_total = 0
                expense_total = 0
                balance = 0
                
                context = {
                    'transactions': transactions,
                    'income_total': income_total,
                    'expense_total': expense_total,
                    'balance': balance
                }
                return render(request, self.template_name, context)
        else:
            user = request.user
        
        try:
            # Buscar transações do usuário
            transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')
            
            # Calcular totais
            income_total = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
            expense_total = transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
            balance = income_total - expense_total
        except:
            # Em caso de erro, usamos valores padrão
            transactions = []
            income_total = 0
            expense_total = 0
            balance = 0
        
        context = {
            'transactions': transactions,
            'income_total': income_total,
            'expense_total': expense_total,
            'balance': balance
        }
        return render(request, self.template_name, context)
