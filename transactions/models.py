from django.db import models, connection
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from django.db.models import Max
from django.db import transaction as db_transaction

class Category(models.Model):
    """Categoria para classificar transações (receitas ou despesas)"""
    TYPE_CHOICES = (
        ('INCOME', _('Receita')),
        ('EXPENSE', _('Despesa')),
        ('BOTH', _('Ambos')),
    )
    
    name = models.CharField(_('nome'), max_length=100)
    type = models.CharField(_('tipo'), max_length=20, choices=TYPE_CHOICES)
    color = models.CharField(_('cor'), max_length=7, blank=True, help_text=_('Código de cor em formato hex, ex: #FF5733'))
    icon = models.CharField(_('ícone'), max_length=50, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories', verbose_name=_('usuário'))
    
    class Meta:
        verbose_name = _('categoria')
        verbose_name_plural = _('categorias')
        ordering = ['name']
        unique_together = ['name', 'user']
    
    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    """Método de pagamento para transações"""
    name = models.CharField(_('nome'), max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payment_methods', verbose_name=_('usuário'))
    
    class Meta:
        verbose_name = _('método de pagamento')
        verbose_name_plural = _('métodos de pagamento')
        ordering = ['name']
        unique_together = ['name', 'user']
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Transação financeira (receita ou despesa)"""
    TYPE_CHOICES = (
        ('INCOME', _('Receita')),
        ('EXPENSE', _('Despesa')),
    )
    
    amount = models.DecimalField(_('valor'), max_digits=10, decimal_places=2)
    description = models.CharField(_('descrição'), max_length=255)
    transaction_date = models.DateField(_('data da transação'))
    type = models.CharField(_('tipo'), max_length=20, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', verbose_name=_('categoria'))
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', verbose_name=_('método de pagamento'))
    is_paid = models.BooleanField(_('está pago'), default=False)
    due_date = models.DateField(_('data de vencimento'), null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions', verbose_name=_('usuário'))
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('transação')
        verbose_name_plural = _('transações')
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.description} - R$ {self.amount} ({self.get_type_display()})"
    
    @property
    def is_income(self):
        return self.type == 'INCOME'
    
    @property
    def is_expense(self):
        return self.type == 'EXPENSE'

class Balance(models.Model):
    """Saldo da carteira do usuário"""
    amount = models.DecimalField(_('valor'), max_digits=10, decimal_places=2)
    date = models.DateField(_('data'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='balances', verbose_name=_('usuário'))
    notes = models.TextField(_('observações'), blank=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True, null=True)
    
    class Meta:
        verbose_name = _('saldo')
        verbose_name_plural = _('saldos')
        ordering = ['-date', '-id']  # Ordena por data e depois por ID, ambos decrescentes
        get_latest_by = ['date', 'id']  # Considera data e ID para determinar o mais recente
    
    def __str__(self):
        return f"Saldo de {self.user.name} em {self.date}: R$ {self.amount}"
    
    @classmethod
    def get_current_balance(cls, user):
        """
        Retorna o valor do saldo atual do usuário.
        Busca o registro mais recente por data e, em caso de empate, pelo ID mais alto.
        """
        try:
            # Busca o objeto Balance mais recente
            balance = cls.objects.filter(user=user).order_by('-date', '-id').first()
            
            # Retorna o valor do saldo se existir, senão retorna 0
            return balance.amount if balance else 0
        except Exception:
            # Em caso de erro, retorna 0
            return 0
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que o ID seja sempre 
        o máximo existente + 1, evitando conflitos de ID.
        """
        # Use transação para evitar condições de corrida
        with db_transaction.atomic():
            # Se este é um novo objeto (não tem ID)
            if not self.pk:
                # Obter o ID máximo da tabela
                max_id = Balance.objects.aggregate(Max('id'))['id__max']
                # Se existe algum registro, defina o ID como max + 1
                if max_id is not None:
                    self.id = max_id + 1
                # Caso contrário, use ID=1 (tabela vazia)
                else:
                    self.id = 1
                
                # Após a inserção, atualize a sequência para o próximo ID
                result = super().save(*args, **kwargs)
                
                # Atualiza a sequência do PostgreSQL para evitar futuros conflitos
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT setval(pg_get_serial_sequence('transactions_balance', 'id'), %s);",
                        [self.id]
                    )
                return result
            else:
                # Para objetos existentes, use o comportamento padrão
                return super().save(*args, **kwargs)
