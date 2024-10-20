# Generated by Django 5.1.2 on 2024-10-20 19:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostelapp20', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproperty',
            name='free_beds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='addproperty',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='property_images/'),
        ),
        migrations.AddField(
            model_name='addproperty',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='addproperty',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='addproperty',
            name='occupied_beds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='addproperty',
            name='total_rooms',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ManagementPin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
