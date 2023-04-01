# Generated by Django 4.1.7 on 2023-04-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audcentral', '0002_transcriptresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcriptresult',
            name='audio_info',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=24),
        ),
        migrations.AddField(
            model_name='transcriptresult',
            name='status',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='transcriptresult',
            name='sentiment_result',
            field=models.CharField(default='None', max_length=500),
        ),
        migrations.AlterField(
            model_name='transcriptresult',
            name='transcribe_result',
            field=models.TextField(default='None'),
        ),
        migrations.AlterField(
            model_name='transcriptresult',
            name='translate_result',
            field=models.TextField(default='None'),
        ),
    ]
