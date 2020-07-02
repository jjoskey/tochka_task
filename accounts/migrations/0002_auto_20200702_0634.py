# Generated by Django 3.0.7 on 2020-07-02 06:34

from uuid import UUID

from django.db import migrations


def create_accounts(apps, schema):
    Account = apps.get_model(app_label='accounts', model_name='account')
    data = [
        {'uuid': UUID('26c940a1-7228-4ea2-a3bc-e6460b172040'),
         'name': 'Петров Иван Сергеевич',
         'balance': 1700,
         'hold': 300,
         'is_opened': True},
        {'uuid': UUID('7badc8f8-65bc-449a-8cde-855234ac63e1'),
         'name': 'Kazitsky Jason',
         'balance': 200,
         'hold': 200,
         'is_opened': True},
        {'uuid': UUID('5597cc3d-c948-48a0-b711-393edf20d9c0'),
         'name': 'Пархоменко Антон Александрович',
         'balance': 10,
         'hold': 300,
         'is_opened': True},
        {'uuid': UUID('867f0924-a917-4711-939b-90b179a96392'),
         'name': 'Петечкин Петр Измаилович',
         'balance': 1000000,
         'hold': 1,
         'is_opened': False}
    ]
    for instance in data:
        Account.objects.create(**instance)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_accounts,
            migrations.RunPython.noop
        )
    ]
