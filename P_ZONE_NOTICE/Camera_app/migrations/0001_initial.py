# Generated by Django 4.1.5 on 2023-01-15 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=40, null=True)),
                ('imgfile', models.ImageField(blank=True, null=True, upload_to='')),
                ('content', models.TextField()),
            ],
        ),
    ]
