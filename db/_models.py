from django.db import models


class Schema(models.Model):
    """
    Schema is the django model class in lorder to use it you will need to
    create the database manually.

    sqlite3 db.sqlite3
    sqlite> CREATE TABLE schema (id integer primary key, name varchar(128), desc varchar(1024));
    sqlite> insert into schema values(1, 'name01', 'desc01');
    sqlite> insert into schema values(2, 'name02', 'desc02');
    sqlite> SELECT * from schema;
    """

    name = models.CharField(unique=True, max_length=128)
    desc = models.CharField(max_length=1024, blank=True, default="")

    class Meta:
        app_label = ""
        verbose_name = "schema"
        managed = False
        db_table = "schema"

    def __unicode__(self):
        return self.name + "--" + self.desc
