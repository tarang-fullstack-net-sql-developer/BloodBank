# Generated by Django 2.1.5 on 2019-03-09 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppComponent', '0015_auto_20190308_0045'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveMailMaster',
            fields=[
                ('PkId', models.AutoField(primary_key=True, serialize=False)),
                ('SentTo', models.CharField(max_length=20)),
                ('CcAcnt', models.TextField()),
                ('BccAcnt', models.TextField()),
                ('Subject', models.TextField()),
                ('Message', models.TextField()),
                ('From', models.CharField(max_length=20)),
                ('UserId', models.TextField()),
                ('CreatedOn', models.CharField(default='2019-03-10', max_length=20)),
                ('CreatedBy', models.CharField(max_length=20)),
                ('ModifiedOn', models.CharField(default='2019-03-10', max_length=20)),
                ('ModifiedBy', models.CharField(max_length=20)),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tbl_SaveMailMaster',
            },
        ),
        migrations.AlterField(
            model_name='bloodrquestmaster',
            name='CreatedOn',
            field=models.CharField(default='2019-03-10', max_length=20),
        ),
        migrations.AlterField(
            model_name='bloodrquestmaster',
            name='ModifiedOn',
            field=models.CharField(default='2019-03-10', max_length=20),
        ),
    ]