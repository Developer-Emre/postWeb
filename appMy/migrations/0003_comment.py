# Generated by Django 4.1.3 on 2023-04-07 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appMy', '0002_post_post_text_alter_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Yorum')),
                ('date_now', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Yorum-tarihi')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appMy.post', verbose_name='Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
        ),
    ]
