# Generated by Django 4.1.3 on 2023-05-29 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
        ("landing", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HeroBlock",
            new_name="HeroHeader",
        ),
        migrations.RenameModel(
            old_name="LatestNews",
            new_name="LatestPosts",
        ),
        migrations.RenameModel(
            old_name="TitleBlock",
            new_name="SectionHeader",
        ),
        migrations.RemoveField(
            model_name="processes",
            name="processes",
        ),
        migrations.RemoveField(
            model_name="processes",
            name="title_block",
        ),
        migrations.AlterModelOptions(
            name="heroheader",
            options={
                "ordering": ["id"],
                "verbose_name": "Hero Header",
                "verbose_name_plural": "Hero Headers",
            },
        ),
        migrations.AlterModelOptions(
            name="sectionheader",
            options={
                "ordering": ["name"],
                "verbose_name": "Section Header",
                "verbose_name_plural": "Section Headers",
            },
        ),
        migrations.DeleteModel(
            name="Hero",
        ),
        migrations.DeleteModel(
            name="Processes",
        ),
    ]