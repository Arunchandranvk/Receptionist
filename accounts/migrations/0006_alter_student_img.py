# Generated by Django 5.1.5 on 2025-01-23 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_student_student_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='media/student_image'),
        ),
    ]
