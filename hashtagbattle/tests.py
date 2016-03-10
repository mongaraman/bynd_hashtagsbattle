from django.test import TestCase

from django.test import TestCase
from .models import Battle

class BattleTestCase(TestCase):
    def setUp(self):
        Battle.objects.create(battle_name="Test Battle1",
        hashtag1="VSSwimSpecial", hashtag2="PURPOSETOUR")
        Battle.objects.create(battle_name="Test Battle2",
        hashtag1="GetElectedIn3Words", hashtag2="Mahashivratri")

    def test_battle_create(self):
        """Battles created and tested"""
        bat1 = Battle.objects.get(battle_name="Test Battle1")
        self.assertEqual(bat1.hashtag1, 'VSSwimSpecial')
        self.assertEqual(bat1.hashtag2, 'PURPOSETOUR')
        bat2 = Battle.objects.get(battle_name="Test Battle2")
        self.assertEqual(bat1.hashtag1, 'GetElectedIn3Words')
        self.assertEqual(bat1.hashtag2, 'Mahashivratri')
         
