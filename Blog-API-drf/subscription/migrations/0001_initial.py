# Generated by Django 4.2 on 2024-12-16 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveBigIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('time_unit', models.CharField(choices=[('D', 'Day'), ('W', 'Week'), ('M', 'Month'), ('Y', 'Year')], max_length=1)),
                ('time_value', models.PositiveSmallIntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
