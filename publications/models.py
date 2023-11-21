from django.db import models

class Publication(models.Model):
   name = models.CharField(max_length=255, blank=False)
   author = models.ForeignKey("demo.author", null=False, on_delete=models.CASCADE)
   first_published = models.DateField()

   objects = PublicationManager()

   def __str__(self):
       return f"{self.name} - {self.first_published}"

   class Meta:
       ordering = ["-first_published"]
       constraints = [
           models.UniqueConstraint(
               fields=["name", "author", "first_published"], name="unique_publication"
           )
       ]


class Author(models.Model):
   name = models.CharField(max_length=255, blank=False)
   date_of_birth = models.DateField()
   date_of_death = models.DateField(null=True)

   def __str__(self):
       return self.name


class Review(models.Model):
   publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
   reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
   score = models.PositiveSmallIntegerField(
       default=3, validators=[MinValueValidator(1), MaxValueValidator(5)]
   )

   def __str__(self):
       return f"Review by {self.reviewer.get_username()}: {self.score}/5 for {self.publication.name}"