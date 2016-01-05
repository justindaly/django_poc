# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversate', '0002_auto_20151227_0311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_message', models.ForeignKey(to='conversate.Message')),
                ('partner', models.ForeignKey(related_name='partner', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='conversation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
