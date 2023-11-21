from mysite.publications import models

def get_all_authors():
    return models.Author.objects.all()