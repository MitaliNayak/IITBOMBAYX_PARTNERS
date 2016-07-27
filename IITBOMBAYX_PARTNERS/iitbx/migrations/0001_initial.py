# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SIP', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='gen_evaluations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sectionid', models.CharField(max_length=250)),
                ('sec_name', models.CharField(max_length=250)),
                ('subsec_id', models.CharField(max_length=250)),
                ('subsec_name', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=150)),
                ('release_date', models.DateTimeField()),
                ('due_date', models.DateTimeField()),
                ('total_weight', models.FloatField()),
                ('grade_weight', models.FloatField()),
                ('total_marks', models.IntegerField(null=True)),
                ('course', models.ForeignKey(to='SIP.edxcourses')),
            ],
        ),
        migrations.CreateModel(
            name='gen_gradestable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edxuserid', models.IntegerField()),
                ('course', models.CharField(max_length=250)),
                ('grade', models.CharField(max_length=25)),
                ('eval', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='gen_headings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section', models.CharField(max_length=200)),
                ('heading', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='gen_markstable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edxuserid', models.IntegerField()),
                ('section', models.CharField(max_length=250)),
                ('total', models.CharField(max_length=25)),
                ('eval', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='gen_questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qid', models.CharField(max_length=250)),
                ('q_name', models.CharField(max_length=250)),
                ('q_weight', models.FloatField()),
                ('prob_count', models.IntegerField()),
                ('course', models.ForeignKey(to='SIP.edxcourses')),
                ('eval', models.ForeignKey(to='iitbx.gen_evaluations')),
            ],
        ),
        migrations.CreateModel(
            name='gen_repout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reportid', models.IntegerField()),
                ('num_cols', models.IntegerField()),
                ('A', models.TextField()),
                ('B', models.TextField()),
                ('C', models.TextField()),
                ('D', models.TextField()),
                ('E', models.TextField()),
                ('F', models.TextField()),
                ('G', models.TextField()),
                ('H', models.TextField()),
                ('I', models.TextField()),
                ('J', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='gen_temp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edxuserid', models.IntegerField(max_length=200)),
                ('section', models.CharField(max_length=200)),
                ('total', models.CharField(max_length=200)),
                ('eval', models.TextField(max_length=200)),
            ],
        ),
    ]
