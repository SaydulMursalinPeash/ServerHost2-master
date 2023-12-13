# Generated by Django 4.2.2 on 2023-06-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=500, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('subject', models.TextField(blank=True, max_length=500, null=True)),
                ('message', models.TextField(max_length=2000, null=True)),
            ],
        ),
    ]
