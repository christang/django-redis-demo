django-redis-demo
=================

Demo of Redis' unordered collections to count memberships in large tables

Synopsis
========

Given a relatively simple model, it's not unreasonable to back the Django app with a relational database store. In doing so, however, the main issue for a naïve app needing to access a store with 1M+ rows would be database contention, and so at least some minimal care should given to properly (1) off-loading the workload, (2) partitioning the store, (3) optimizing the storage to minimize latency on operations. There are many more ways to partition the store using noSQL solutions, but their integration with Django, although interesting and worth experimenting with, do seem less mature. For the discussion at hand, we can limit ourselves to relational DBs. 

With regard to partitioning, then, this leaves us a little more limited, but it's worthwhile noting that in general, we would benefit from a master-slave configuration of the relational DB where we might expect messages to be written to the master, and requests for status or other read operation to be localized to the pool of slaves. This seems to be more operational in nature, so maybe it's worthwhile to talk about this elsewhere in the context of automation.

The work we can do programmatically then is in optimizing operations to the storage, and off-loading workload. The process for the former typically involves using Describe Analyze to figure out how the RDBS is structuring its queries, looking for bottlenecks, and alleviating them by writing custom raw SQL (if the Django ORM is not doing a good job of translating the query), or introducing indices to relevant columns. In this respect, postgres has some features that are really nice with respect to indices, including indexing concurrently, and the flexibility with types and combining. Counting unique cities and username require group by functionality so this is a natural place for indexing.

While Django has a lot of magic that allow you to create indices, taking advantage of db-specific features force you to use tools that can augment what Django provides. In particular, South is very useful migration tool, and it allows you great flexibility in writing well-managed database operations like creating indices, loading fixtures etc.

Finally, a most often used method for off-loading workload is caching. In particular, we are interested in counting distinct items, and so the data structure that comes to mind is the item-set. Basically we want to add items to a set so that the set semantics can handle duplicates for us. While memcache is an often used solution, redis actually has a natural set primitive that lets us do the work of set management handily.

Note that redis is not necessarily being used as simply a model cache. Because the update unit is so small (an item), it can be updated simultaneously with the db to store a usable result rather than just a simple image of the underlying data.

Regardless of set functionality, using a (maybe distributed) cache helps us offload RAM from the app server, while being able to scale the cache pool allows us to add instances without bottlenecking around a single resource. In particular, we might want to structure a high-load application with a couple of operational streams:

1: Django (ingest/write) ——> postgres (master)
1: Django (ingest/write) ——> redis

2: Django (manage) <—— postgres (slave)
2: Django (manage) ——> redis

3: Django (query/read) <—— redis

Some roles can be housed in the same instance (which is what we see all the time), but it's useful to think that the roles can be housed by different instances, or even pools of instances. Many small dedicated workers can potentially take the place of one particularly thick service.

Lastly, Django dynamic and static content should be served from dedicated processes. For the latter, there's a module called Cling that Heroku uses, but is not limited to their services. To minimize overhead of web application workers, one might use gunicorn, which is lightweight and has been proven production-worthy. uWSGI is another suitable option.
