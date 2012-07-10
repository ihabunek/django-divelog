# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dive'
        db.create_table('divelog_dive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('fingerprint', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('max_depth', self.gf('django.db.models.fields.FloatField')()),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('divelog', ['Dive'])

        # Adding model 'Sample'
        db.create_table('divelog_sample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['divelog.Dive'])),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
            ('depth', self.gf('django.db.models.fields.FloatField')()),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('divelog', ['Sample'])

        # Adding model 'Event'
        db.create_table('divelog_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['divelog.Dive'])),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('divelog', ['Event'])

        # Adding model 'DiveUpload'
        db.create_table('divelog_diveupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('data', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('divelog', ['DiveUpload'])


    def backwards(self, orm):
        # Deleting model 'Dive'
        db.delete_table('divelog_dive')

        # Deleting model 'Sample'
        db.delete_table('divelog_sample')

        # Deleting model 'Event'
        db.delete_table('divelog_event')

        # Deleting model 'DiveUpload'
        db.delete_table('divelog_diveupload')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'divelog.dive': {
            'Meta': {'object_name': 'Dive'},
            'comment': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'fingerprint': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_depth': ('django.db.models.fields.FloatField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'divelog.diveupload': {
            'Meta': {'object_name': 'DiveUpload'},
            'data': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'divelog.event': {
            'Meta': {'object_name': 'Event'},
            'dive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['divelog.Dive']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'time': ('django.db.models.fields.IntegerField', [], {})
        },
        'divelog.sample': {
            'Meta': {'object_name': 'Sample'},
            'depth': ('django.db.models.fields.FloatField', [], {}),
            'dive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['divelog.Dive']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['divelog']