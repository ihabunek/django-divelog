# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('divelog_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('divelog', ['Location'])

        # Adding model 'Dive'
        db.create_table('divelog_dive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fingerprint', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['divelog.Location'], null=True, blank=True)),
            ('max_depth', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_depth', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
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
        # Deleting model 'Location'
        db.delete_table('divelog_location')

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
            'avg_depth': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fingerprint': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['divelog.Location']", 'null': 'True', 'blank': 'True'}),
            'max_depth': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
        'divelog.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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