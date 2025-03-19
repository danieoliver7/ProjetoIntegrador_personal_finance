from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Balance, Transaction, Category, PaymentMethod
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from users.models import CustomUser
from django.http import JsonResponse
import json

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
class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    
    def get_queryset(self):
        # Verificar se o usuário está autenticado
        if self.request.user.is_authenticated:
            return Transaction.objects.filter(user=self.request.user).order_by('-transaction_date')
        else:
            # Para usuários não autenticados
            from users.models import CustomUser
            test_user = CustomUser.objects.first()
            if test_user:
                return Transaction.objects.filter(user=test_user).order_by('-transaction_date')
            else:
                return Transaction.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Verificar se o usuário está autenticado antes de buscar categorias e métodos de pagamento
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            # Usar usuário de teste para contexto
            from users.models import CustomUser
            user = CustomUser.objects.first() or None
        
        if user:
            from django.db.models import Sum
            from .models import Category, PaymentMethod
            
            # Adicionar categorias e métodos de pagamento ao contexto
            context['categories'] = Category.objects.filter(user=user)
            context['payment_methods'] = PaymentMethod.objects.filter(user=user)
            
            # Calcular totais para o resumo financeiro
            income = Transaction.objects.filter(
                user=user, 
                type='income',
                is_paid=True  # Presumindo que is_paid é o campo correto, não status
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            expense = Transaction.objects.filter(
                user=user, 
                type='expense',
                is_paid=True
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            context['total_income'] = income
            context['total_expense'] = expense
            context['balance'] = income - expense
        else:
            # Valores padrão se não houver usuário
            context['categories'] = []
            context['payment_methods'] = []
            context['total_income'] = 0
            context['total_expense'] = 0
            context['balance'] = 0
        
        return context

def create_default_categories(user):
    Category.objects.get_or_create(name="Entrada", user=user)
    Category.objects.get_or_create(name="Saída", user=user)

def create_transaction(request):
    try:
        data = json.loads(request.body)
        
        # Obter os dados do formulário
        transaction_type = data.get('type')
        amount = float(data.get('amount', 0))
        date_str = data.get('date')
        description = data.get('description')
        payment_method_id = data.get('payment_method')
        status = data.get('status', 'paid')
        notes = data.get('notes', '')
        
        # Validar dados obrigatórios
        if not all([transaction_type, amount, description, payment_method_id]):
            return JsonResponse({'error': 'Campos obrigatórios não preenchidos'}, status=400)
        
        # Processar a data
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = datetime.now().date()
        
        # Buscar método de pagamento
        try:
            payment_method = PaymentMethod.objects.get(id=payment_method_id, user=request.user)
        except PaymentMethod.DoesNotExist:
            return JsonResponse({'error': 'Método de pagamento inválido'}, status=400)
        
        # Criar a transação (sem vincular a uma categoria)
        transaction = Transaction.objects.create(
            user=request.user,
            type=transaction_type,
            amount=amount,
            transaction_date=date,
            description=description,
            payment_method=payment_method,
            is_paid=(status == 'paid'),
            notes=notes
        )
        
        # Atualizar o saldo da carteira se a transação for paga
        if status == 'paid':
            update_balance(request.user, transaction_type, amount)
        
        return JsonResponse({
            'success': True,
            'message': 'Transação cadastrada com sucesso',
            'transaction_id': transaction.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
