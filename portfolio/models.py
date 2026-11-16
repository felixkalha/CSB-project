from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(upload_to='portfolio_images/', blank=True)
    video_url = models.URLField('YouTube embed URL', blank=True)
    is_private = models.BooleanField(default=False)
    draft_password = models.CharField(max_length=128, blank=True) #blank=False, validators=[MinLengthValidator(8)])
    #Above you can see the fix to be included for 4. Auhentications flaws.
    
    #Here this save() below is included then to hash the password for flaw 2. cryptographic failure.
    #def save(self, *args, **kwargs):
    #    self.draft_password = make_password(self.draft_password)
    #    super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author_name} on {self.project}'
    

