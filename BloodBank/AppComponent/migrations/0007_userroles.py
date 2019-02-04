# Generated by Django 2.1.5 on 2019-02-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppComponent', '0006_delete_userroles'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('RolePkId', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=20)),
                ('Description', models.CharField(max_length=20)),
                ('isActive', models.BooleanField(default=0)),
                ('CreatedOn', models.CharField(max_length=20)),
                ('CreatedBy', models.CharField(max_length=20)),
                ('ModifiedOn', models.CharField(max_length=20)),
                ('ModifiedBy', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tbl_UserRole',
            },
        ),
    ]