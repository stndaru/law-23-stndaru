# Generated by Django 4.1.7 on 2023-04-01 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audcentral', '0003_transcriptresult_audio_info_transcriptresult_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryAudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='audio/')),
            ],
        ),
    ]