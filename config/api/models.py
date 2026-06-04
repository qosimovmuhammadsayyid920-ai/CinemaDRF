from django.db import models

class Genre(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title
    
class Rejissior(models.Model):
    name = models.CharField(max_length=150)
    birth_year = models.IntegerField()
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=150)
    birth_year = models.IntegerField()
    avatar = models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    release_year = models.IntegerField()
    poster = models.ImageField(upload_to='movie_images/')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    rejissior = models.ForeignKey(Rejissior, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

