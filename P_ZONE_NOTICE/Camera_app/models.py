from django.db import models

# Create your models here.
class FileUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    imgfile = models.ImageField(null=False, upload_to="", blank=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.title