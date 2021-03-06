from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=20)),
                ('employee_name', models.CharField(max_length=20)),
                ('mobile_number', models.PositiveIntegerField()),
                ('employee_title', models.CharField(max_length=10)),
            ],
        ),
    ]