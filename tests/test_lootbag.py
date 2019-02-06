import unittest
import sys
import random
import string
sys.path.append('../')
from lootbag import LootBag

def string_generator():
    '''Generates a random string for testing new entries in db.'''
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(7))

class TestLootBag(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("Set up class")
        self.lootbag = LootBag()

    def test_find_child(self):
        """Finds a child that already exists in the database """

        child = "Sebastian"
        self.assertEqual(self.lootbag.find_child(child), 1)

    def test_find_add_child(self):
        """Attempts to find a child that already exists in the database, when that fails it creates a new child and returns the id """

        new_name = string_generator()
        self.assertIsInstance(self.lootbag.find_child(new_name), int)

    def test_add_toy_existing_child(self):
        """Adds a new toy with an existing child. Also calls find_child method """

        child = "Sebastian"
        toy = string_generator()
        self.assertIsInstance(self.lootbag.add_toy(child, toy), int)

    def test_add_toy_add_child(self):
        """Creates a new child and then adds a toy associated with that child to the database """

        child = string_generator()
        toy = "Video Game"
        self.assertIsInstance(self.lootbag.add_toy(child, toy), int)

    def test_remove_toy(self):
        """Creates a new toy to assign to an existing child and then removes the toy from the database"""

        child = "Sebastian"
        toy = string_generator()
        self.lootbag.add_toy(toy, child)
        self.lootbag.remove_toy(child, toy)
        self.assertIsNone(self.lootbag.find_toy(child, toy))

    def test_find_toy(self):
        """Creates a new toy and a new child and then finds the toy. Then removes that toy and child from the datbase."""

        child = string_generator()
        toy = string_generator()
        self.lootbag.add_toy(toy, child)
        self.assertIsInstance(self.lootbag.find_toy(child, toy), tuple)
        self.lootbag.remove_toy(child, toy)
        self.assertIsNone(self.lootbag.find_toy(child, toy))

if __name__ == '__main__':
    unittest.main()
