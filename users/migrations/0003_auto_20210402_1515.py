# Generated by Django 3.1.7 on 2021-04-02 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_institute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Institute',
        ),
        migrations.AlterField(
            model_name='staff',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department'),
        ),
        migrations.AlterField(
            model_name='student',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department'),
        ),
    ]