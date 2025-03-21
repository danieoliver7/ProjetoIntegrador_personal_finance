# Generated by Django 5.1.6 on 2025-03-17 14:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='valor')),
                ('date', models.DateField(verbose_name='data')),
                ('notes', models.TextField(blank=True, verbose_name='observações')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'saldo',
                'verbose_name_plural': 'saldos',
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('type', models.CharField(choices=[('INCOME', 'Receita'), ('EXPENSE', 'Despesa'), ('BOTH', 'Ambos')], max_length=20, verbose_name='tipo')),
                ('color', models.CharField(blank=True, help_text='Código de cor em formato hex, ex: #FF5733', max_length=7, verbose_name='cor')),
                ('icon', models.CharField(blank=True, max_length=50, verbose_name='ícone')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
                'ordering': ['name'],
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'método de pagamento',
                'verbose_name_plural': 'métodos de pagamento',
                'ordering': ['name'],
                'unique_together': {('name', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='valor')),
                ('description', models.CharField(max_length=255, verbose_name='descrição')),
                ('transaction_date', models.DateField(verbose_name='data da transação')),
                ('type', models.CharField(choices=[('INCOME', 'Receita'), ('EXPENSE', 'Despesa')], max_length=20, verbose_name='tipo')),
                ('is_paid', models.BooleanField(default=False, verbose_name='está pago')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='data de vencimento')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='transactions.category', verbose_name='categoria')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='transactions.paymentmethod', verbose_name='método de pagamento')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'transação',
                'verbose_name_plural': 'transações',
                'ordering': ['-transaction_date'],
            },
        ),
    ]
