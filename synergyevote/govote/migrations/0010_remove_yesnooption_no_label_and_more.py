# Generated by Django 5.1.7 on 2025-03-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govote', '0009_alter_candidate_options_alter_position_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yesnooption',
            name='no_label',
        ),
        migrations.RemoveField(
            model_name='yesnooption',
            name='yes_label',
        ),
        migrations.AddField(
            model_name='yesnooption',
            name='vote_yn',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3),
        ),
    ]
