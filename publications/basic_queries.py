from publications import models

def get_all_authors():
    return models.Author.objects.all()

def get_all_authors_ordered_by_date_of_birth():
    return models.Author.objects.order_by("date_of_birth")

def get_authors_by_name(name):
    return models.Author.objects.filter(name=name)

def get_authors_born_after(date):
    return models.Author.objects.filter(date_of_birth__gt=date)

def get_authors_with_publications_published_before(date):
    return models.Author.objects.filter(publication__first_published__lt=date)