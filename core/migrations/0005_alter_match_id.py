# Generated by Django 4.1.2 on 2023-05-30 17:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_match_id_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]