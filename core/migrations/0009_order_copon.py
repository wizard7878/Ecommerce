# Generated by Django 3.0.2 on 2020-04-15 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_copun'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='copon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Copun'),
        ),
    ]