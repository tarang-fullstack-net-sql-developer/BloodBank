# Generated by Django 2.1.5 on 2019-02-05 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppComponent', '0007_userroles'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailSent',
            fields=[
                ('PkId', models.AutoField(primary_key=True, serialize=False)),
                ('SentTo', models.CharField(max_length=20)),
                ('Subject', models.CharField(max_length=20)),
                ('Message', models.TextField()),
                ('From', models.CharField(max_length=20)),
                ('SentOn', models.CharField(max_length=20)),
                ('isDelivered', models.BooleanField()),
                ('CreatedOn', models.CharField(max_length=20)),
                ('CreatedBy', models.CharField(max_length=20)),
                ('ModifiedOn', models.CharField(max_length=20)),
                ('ModifiedBy', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tbl_MailSent',
            },
        ),
    ]
