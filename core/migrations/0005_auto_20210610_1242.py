# Generated by Django 3.1.2 on 2021-06-10 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_medicaltestrecord_medical_test_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicaltestrecord',
            name='age',
        ),
        migrations.RemoveField(
            model_name='medicaltestrecord',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='medicaltestrecord',
            name='medical_test_id',
        ),
        migrations.RemoveField(
            model_name='medicaltestrecord',
            name='name',
        ),
        migrations.RemoveField(
            model_name='medicaltestrecord',
            name='patient_id',
        ),
        migrations.RemoveField(
            model_name='medicaltestrecord',
            name='report_date',
        ),
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=50)),
                ('report_date', models.DateField()),
                ('medical_test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.medicaltest')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.patient')),
            ],
            options={
                'db_table': 'PersonalInfo',
            },
        ),
        migrations.AddField(
            model_name='medicaltestrecord',
            name='personal_info_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.personalinfo'),
            preserve_default=False,
        ),
    ]
