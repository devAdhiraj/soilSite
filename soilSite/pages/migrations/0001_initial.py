# Generated by Django 3.1.7 on 2021-04-11 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('imageFile', models.FileField(null=True, upload_to='images/', verbose_name='')),
            ],
        ),
    ]
