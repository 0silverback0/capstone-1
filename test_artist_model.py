import os
from unittest import TestCase
from models import db, Artist

os.environ['DATABASE_URL'] = "postgresql:///testting-hiphop"

from app import app

db.create_all()

class TestArtistModel(TestCase):
    """ test the artist model """

    def setUp(self):
        """ set up model to be tested """

        db.drop_all()
        db.create_all()

        test_artist = Artist(name='test artist', artist_id=8732, img_url='test artist img')
        art_id = 67
        test_artist.id = art_id

        db.session.commit()

        self.artist = Artist.query.get(art_id)
        self.a_id = art_id

    def test_artist(self):
        """ test creation of new artist """

        test_artist = Artist(name='test artist', artist_id=8732, img_url='test artist img')
        db.session.commit()

        self.assertEqual(test_artist.name, 'test artist')
        self.assertEqual(test_artist.artist_id, 8732)
        self.assertEqual(test_artist.img_url, 'test artist img')
        