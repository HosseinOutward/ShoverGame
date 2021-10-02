# Generated by Django 3.2.7 on 2021-10-02 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0005_alter_lobby_last_move_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='last_move_act',
            field=models.IntegerField(choices=[(0, 'NULL'), (1, 'up'), (2, 'right'), (3, 'down'), (4, 'left')], null=True),
        ),
        migrations.AlterField(
            model_name='lobby',
            name='last_move_player',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lobby.playerinlobby'),
        ),
    ]