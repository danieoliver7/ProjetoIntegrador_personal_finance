from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from datetime import datetime
from .models import Transaction, Category, PaymentMethod, Balance
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
@csrf_exempt
def create_transaction(request):
    try:
        data = json.loads(request.body)
        
        # Obter os dados do formulário
        transaction_type = data.get('type')
        amount = float(data.get('amount', 0))
        date_str = data.get('date')
        description = data.get('description')
        category_id = data.get('category')
        payment_method_id = data.get('payment_method')
        status = data.get('status', 'paid')
        notes = data.get('notes', '')
        
        # Validar dados obrigatórios
        if not all([transaction_type, amount, description, category_id, payment_method_id]):
            return JsonResponse({'error': 'Campos obrigatórios não preenchidos'}, status=400)
        
        # Processar a data
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = datetime.now().date()
        
        # Buscar objetos relacionados
        try:
            category = Category.objects.get(id=category_id, user=request.user)
            payment_method = PaymentMethod.objects.get(id=payment_method_id, user=request.user)
        except (Category.DoesNotExist, PaymentMethod.DoesNotExist):
            return JsonResponse({'error': 'Categoria ou método de pagamento inválido'}, status=400)
        
        # Criar a transação
        transaction = Transaction.objects.create(
            user=request.user,
            type=transaction_type,
            amount=amount,
            date=date,
            description=description,
            category=category,
            payment_method=payment_method,
            status=status,
            notes=notes
        )
        
        # Atualizar o saldo da carteira (se a transação for marcada como paga)
        if status == 'paid':
            update_balance(request.user, transaction_type, amount)
        
        return JsonResponse({
            'success': True,
            'message': 'Transação cadastrada com sucesso',
            'transaction_id': transaction.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def update_balance(user, transaction_type, amount):
    """Atualiza o saldo do usuário com base na transação"""
    # Obter o saldo atual
    current_balance = Balance.get_current_balance(user)
    
    # Calcular o novo saldo
    if transaction_type == 'income':
        new_balance = current_balance + amount
    else:  # expense
        new_balance = current_balance - amount
    
    # Criar um novo registro de saldo
    Balance.objects.create(
        user=user,
        amount=new_balance,
        date=datetime.now().date()
    ) 