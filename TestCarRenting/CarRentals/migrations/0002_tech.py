# Generated by Django 3.0.1 on 2019-12-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarRentals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tech',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
