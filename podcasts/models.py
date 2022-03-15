from django.db import models

# Create your models here.

class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.CharField(max_length=100)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"

class Status(models.Model):
    """ The status is used to enable the news items to be reviwed and
     track the review and those item for re-publishing
     Status options are
     - New
     - Review
     - To Republish
     - Republished
     - Done
     """
    state = models.CharField(max_length=20)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'statuses'

    def __str__(self) -> str:
        return f"{self.state}"

class NewsItem(models.Model):
    source_name = models.CharField(max_length=100, default=' ')
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField(max_length = 300)
    image = models.URLField()
    podcast_name = models.CharField(max_length=100)
    guid = models.CharField(max_length=200)
    comment = models.TextField()
    status = models.ForeignKey(Status,
    models.SET_NULL,
        blank=True,
        null=True,
        )
    star_rating = models.IntegerField(default=5)

    def __str__(self) -> str:
        return f"{self.source_name}: {self.title}"

