# Generated by Django 5.0.7 on 2024-07-15 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anticipos', '0003_anticipo_created_at_anticipo_foto_producto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anticipo',
            name='iva',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='anticipo',
            name='retencion',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='anticipo',
            name='subtotal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='anticipo',
            name='total_pagar',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='anticipo',
            name='vlr_unitario',
            field=models.IntegerField(),
        ),
    ]
