# Generated by Django 3.0.1 on 2019-12-27 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('namespace', models.CharField(max_length=200)),
                ('confirmation_hash', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField()),
                ('target_id', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('updated_at', models.DateTimeField()),
                ('access_token', models.CharField(max_length=200)),
                ('client_id', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
                ('endpoints_http', models.CharField(max_length=200)),
                ('endpoints_mqtt', models.CharField(max_length=200)),
                ('endpoints_uploader', models.CharField(max_length=200)),
                ('expires_at', models.DateTimeField(blank=True)),
                ('grant_type', models.CharField(max_length=200)),
                ('href', models.CharField(max_length=200)),
                ('owner_id', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('scope_1', models.CharField(max_length=200)),
                ('scope_2', models.CharField(max_length=200)),
            ],
        ),
    ]
