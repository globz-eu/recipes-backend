import os
from django.db import migrations
from django.conf import settings


def create_data(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    user = User(pk=1, username=os.environ['AUTH0_USERNAME'], is_active=True , email=os.environ['AUTH0_EMAIL'])
    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20191112_2234'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
