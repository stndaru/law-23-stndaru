# Generated by Django 4.1.7 on 2023-03-31 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audcentral', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranscriptResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcribe_result', models.TextField()),
                ('translate_result', models.TextField()),
                ('sentiment_result', models.CharField(max_length=500)),
            ],
        ),
    ]