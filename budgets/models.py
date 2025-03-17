from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from transactions.models import Category

class Goal(models.Model):
    """Meta financeira do usuário"""
    name = models.CharField(_('nome'), max_length=100)
    description = models.TextField(_('descrição'), blank=True)
    target_amount = models.DecimalField(_('valor alvo'), max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(_('valor atual'), max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField(_('data de início'))
    end_date = models.DateField(_('data de conclusão'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='goals', verbose_name=_('categoria'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='goals', verbose_name=_('usuário'))
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('meta')
        verbose_name_plural = _('metas')
        ordering = ['end_date']
    
    def __str__(self):
        return self.name
    
    @property
    def progress_percentage(self):
        """Retorna o percentual de progresso da meta"""
        if self.target_amount <= 0:
            return 0
        percentage = (self.current_amount / self.target_amount) * 100
        return min(round(percentage), 100)  # Limita a 100%
    
    @property
    def is_completed(self):
        """Verifica se a meta foi atingida"""
        return self.current_amount >= self.target_amount

class Budget(models.Model):
    """Orçamento mensal ou por período"""
    name = models.CharField(_('nome'), max_length=100)
    amount = models.DecimalField(_('valor'), max_digits=10, decimal_places=2)
    start_date = models.DateField(_('data de início'))
    end_date = models.DateField(_('data de fim'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets', verbose_name=_('categoria'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='budgets', verbose_name=_('usuário'))
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('orçamento')
        verbose_name_plural = _('orçamentos')
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} - {self.start_date.strftime('%m/%Y')}"
    
    @property
    def spent_amount(self):
        """Calcula o valor gasto no período do orçamento"""
        from transactions.models import Transaction
        return Transaction.objects.filter(
            user=self.user,
            category=self.category,
            type='EXPENSE',
            transaction_date__gte=self.start_date,
            transaction_date__lte=self.end_date
        ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    @property
    def remaining_amount(self):
        """Calcula o valor restante do orçamento"""
        return self.amount - self.spent_amount
    
    @property
    def progress_percentage(self):
        """Retorna o percentual de uso do orçamento"""
        if self.amount <= 0:
            return 0
        percentage = (self.spent_amount / self.amount) * 100
        return round(percentage)
