# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.db import transaction


index = "counts_messages_username_idx"


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Messages', fields ['state']
        try:
            db.commit_transaction()
        except transaction.TransactionManagementError as e:
            print "Silently ignorng"
            print e
        db.execute("CREATE INDEX CONCURRENTLY %s ON counts_messages (username)" % (index,))
        db.start_transaction()

    def backwards(self, orm):
        # Removing index on 'Messages', fields ['state']
        try:
            db.commit_transaction()
        except transaction.TransactionManagementError as e:
            print "Silently ignorng"
            print e
        db.execute("DROP INDEX %s" % (index,))
        db.start_transaction()

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
