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
        return f"{self.id}"

# Define model for publications
class Publication(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField(default="https://www.clipartmax.com/png/middle/265-2655834_work-in-progress-icon.png")
    image_file = models.CharField(max_length=20, default="wip.jpg") # file name of the image file held in staticfiles/img
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id}"

# Lookup table to identify the stories to include in a publication
class Publication_Stories(models.Model):
    readonly_fields = ('id',)
    publication_id = models.ForeignKey(Publication,
    models.SET_NULL,
        blank=True,
        null=True,
        )
    news_item_id = models.ForeignKey(NewsItem,
    models.SET_NULL,
        blank=True,
        null=True,
        )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Publication_Stories'

    def __str__(self) -> str:
        return f" Pub ID: {self.publication_id} News ID: {self.news_item_id}"