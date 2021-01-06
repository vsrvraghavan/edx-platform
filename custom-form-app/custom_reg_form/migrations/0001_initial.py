# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileExtraInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('favorite_language', models.CharField(max_length=100, verbose_name=b'Favorite Programming Language', error_messages={b'required': 'Please tell us your programming language.', b'invalid': "It's an invalid entry."})),
                ('favorite_editor', models.CharField(blank=True, max_length=5, verbose_name=b'Favorite Editor', choices=[(b'vim', b'Vim'), (b'emacs', b'Emacs'), (b'bbedit', b'BBEdit'), (b'np', b'Notepad'), (b'cat', b'cat > filename')])),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ]
        ),
    ]
