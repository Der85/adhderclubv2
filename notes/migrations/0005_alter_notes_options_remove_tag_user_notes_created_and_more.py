# Generated by Django 4.0.6 on 2024-12-22 23:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_tag_notes_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notes',
            options={'ordering': ['due_date', '-priority', '-created']},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='user',
        ),
        migrations.AddField(
            model_name='notes',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notes',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notes',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium', max_length=10),
        ),
        migrations.AlterField(
            model_name='notes',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notes',
            name='tags',
            field=models.ManyToManyField(blank=True, to='notes.tag'),
        ),
    ]