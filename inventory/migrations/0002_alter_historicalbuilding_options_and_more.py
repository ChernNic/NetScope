# Generated by Django 5.2 on 2025-04-07 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalbuilding',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical здания'},
        ),
        migrations.AlterModelOptions(
            name='historicalconnection',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical соединения'},
        ),
        migrations.AlterModelOptions(
            name='historicaldevice',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical устройства'},
        ),
        migrations.AlterModelOptions(
            name='historicaldevicerole',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical роли устройств'},
        ),
        migrations.AlterModelOptions(
            name='historicaldevicetype',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical модели устройств'},
        ),
        migrations.AlterModelOptions(
            name='historicalinterface',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical интерфейсы'},
        ),
        migrations.AlterModelOptions(
            name='historicallocation',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical локации'},
        ),
        migrations.AlterModelOptions(
            name='historicalmanufacturer',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical производители'},
        ),
        migrations.AlterModelOptions(
            name='historicalorganization',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'История', 'verbose_name_plural': 'historical организации'},
        ),
        migrations.AlterField(
            model_name='building',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='inventory.organization', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='connection',
            name='interface1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections1', to='inventory.interface', verbose_name='Интерфейс 1'),
        ),
        migrations.AlterField(
            model_name='connection',
            name='interface2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections2', to='inventory.interface', verbose_name='Интерфейс 2'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='inventory.devicetype', verbose_name='Модель устройства'),
        ),
        migrations.AlterField(
            model_name='device',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='inventory.location', verbose_name='Локация'),
        ),
        migrations.AlterField(
            model_name='device',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='inventory.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='device',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='inventory.devicerole', verbose_name='Роль устройства'),
        ),
        migrations.AlterField(
            model_name='historicalbuilding',
            name='organization',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.organization', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='historicalconnection',
            name='interface1',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.interface', verbose_name='Интерфейс 1'),
        ),
        migrations.AlterField(
            model_name='historicalconnection',
            name='interface2',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.interface', verbose_name='Интерфейс 2'),
        ),
        migrations.AlterField(
            model_name='historicaldevice',
            name='device_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.devicetype', verbose_name='Модель устройства'),
        ),
        migrations.AlterField(
            model_name='historicaldevice',
            name='location',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.location', verbose_name='Локация'),
        ),
        migrations.AlterField(
            model_name='historicaldevice',
            name='manufacturer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='historicaldevice',
            name='role',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.devicerole', verbose_name='Роль устройства'),
        ),
        migrations.AlterField(
            model_name='historicalinterface',
            name='device',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.device', verbose_name='Устройство'),
        ),
        migrations.AlterField(
            model_name='historicallocation',
            name='building',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.building', verbose_name='Здание'),
        ),
        migrations.AlterField(
            model_name='interface',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='inventory.device', verbose_name='Устройство'),
        ),
        migrations.AlterField(
            model_name='location',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='inventory.building', verbose_name='Здание'),
        ),
    ]
