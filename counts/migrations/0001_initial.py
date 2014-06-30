# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Messages'
        db.create_table(u'counts_messages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'counts', ['Messages'])


    def backwards(self, orm):
        # Deleting model 'Messages'
        db.delete_table(u'counts_messages')


    models = {
        u'counts.messages': {
            'Meta': {'ordering': "['state', 'city', 'create_time']", 'object_name': 'Messages'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['counts']