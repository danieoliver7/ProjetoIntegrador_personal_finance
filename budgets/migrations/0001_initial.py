# Generated by Django 5.1.6 on 2025-03-17 14:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='valor')),
                ('start_date', models.DateField(verbose_name='data de início')),
                ('end_date', models.DateField(verbose_name='data de fim')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='transactions.category', verbose_name='categoria')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'orçamento',
                'verbose_name_plural': 'orçamentos',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('description', models.TextField(blank=True, verbose_name='descrição')),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='valor alvo')),
                ('current_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='valor atual')),
                ('start_date', models.DateField(verbose_name='data de início')),
                ('end_date', models.DateField(verbose_name='data de conclusão')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='goals', to='transactions.category', verbose_name='categoria')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'meta',
                'verbose_name_plural': 'metas',
                'ordering': ['end_date'],
            },
        ),
    ]
