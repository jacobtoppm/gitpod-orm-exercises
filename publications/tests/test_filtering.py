from django.test import TestCase

from datetime import date

from publications import models, basic_queries


class TestFiltering(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.living_author_1 = models.Author.objects.create(
            name="Sarah Stillalive",
            date_of_birth=date.fromisoformat('2000-12-04')
        )
        cls.living_author_2 = models.Author.objects.create(
            name="Steve Swearshesnotavampire",
            date_of_birth=date.fromisoformat('1888-11-08')
        )
        cls.dead_author_1 = models.Author.objects.create(
            name="Michael Kickbucket",
            date_of_birth=date.fromisoformat('1835-11-22'),
            date_of_death=date.fromisoformat('1886-11-11'),
        )
        models.Publication.objects.create(
            name="Revolutionary Roundabouts: Marxist Thought in Swindon",
            author=cls.living_author_1,
            first_published=date.fromisoformat('2018-04-13')
        )
        models.Publication.objects.create(
            name="Swings and Roundabouts: the Highs and Lows of a Swindonian Childhood",
            author=cls.living_author_1,
            first_published=date.fromisoformat('2021-05-18')
        )
        cls.youth_critique_publication = models.Publication.objects.create(
            name="The Youth of the Twenty-First Century: An In Depth Critique",
            author=cls.living_author_2,
            first_published=date.fromisoformat('2016-02-11')
        )
        cls.cigar_publication = models.Publication.objects.create(
            name="The Healthful Benefits of the Cigar",
            author=cls.dead_author_1,
            first_published=date.fromisoformat('1886-12-12')
        )
    
    def test_get_all_authors(self):
        authors = basic_queries.get_all_authors()
        self.assertEqual(set(authors), set([self.living_author_1, self.living_author_2, self.dead_author_1]))

    def test_get_authors_ordered_by_date_of_birth(self):
        authors = basic_queries.get_all_authors_ordered_by_date_of_birth()
        self.assertQuerysetEqual(authors, [self.dead_author_1, self.living_author_2, self.living_author_1])

    def test_get_authors_by_name(self):
        self.assertQuerysetEqual(basic_queries.get_authors_by_name("Michael Kickbucket"), [self.dead_author_1])
        self.assertQuerysetEqual(basic_queries.get_authors_by_name("Tanja the Nonexistent"), [])
    
    def test_get_authors_born_after(self):
        self.assertQuerysetEqual(basic_queries.get_authors_born_after(date.fromisoformat('1888-11-08')), [self.living_author_1])
    
    def test_get_authors_with_publications_published_before(self):
        self.assertQuerysetEqual(basic_queries.get_authors_with_publications_published_before(date.fromisoformat('2017-02-11')), [self.dead_author_1, self.living_author_2])