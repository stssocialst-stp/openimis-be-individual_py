from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('individual', '0019_merge_20250526_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='nib',
            field=models.CharField(blank=True, db_column='NIB', max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='historicalindividual',
            name='nib',
            field=models.CharField(blank=True, db_column='NIB', max_length=25, null=True),
        ),
    ]
