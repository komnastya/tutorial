import unittest


class Owner:
    def __init__(self, name):
        self.person_name = name
        self._adopted_pets = []

    def adopt(self, pet):
        if self.owns(pet):
            return False
        if pet._pet_owner != None:
            pet._pet_owner.abandon(pet)
        self._adopted_pets.append(pet)
        pet._pet_owner = self
        return True

    def abandon(self, pet):
        if not self.owns(pet):
            return False
        self._adopted_pets.remove(pet)
        pet._pet_owner = None
        return True

    def owns(self, pet):
        return pet in self._adopted_pets and pet._pet_owner is self

    def _is_consistent(self):
        for pet in self._adopted_pets:
            assert pet._pet_owner is self


class Pet:
    def __init__(self, name):
        self.pet_name = name
        self._pet_owner = None

    def get_owner(self):
        return self._pet_owner

    def set_owner(self, owner):
        if self._pet_owner == owner:
            return False
        if self._pet_owner is not None:
            self._pet_owner._adopted_pets.remove(self)
        self._pet_owner = owner
        if self._pet_owner is not None:
            self._pet_owner._adopted_pets.append(self)
        return True

    def _is_consistent(self):
        assert self._pet_owner.owns(self)


class TestPets(unittest.TestCase):
    def test_initially_not_onwed(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        self.assertFalse(owner.owns(pet))
        self.assertIsNone(pet.get_owner())

    def test_owner_adopts_an_orphat_pet(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        self.assertTrue(owner.adopt(pet))
        self.assertTrue(owner.owns(pet))
        self.assertIs(pet.get_owner(), owner)

    def test_owner_adopts_a_pet_it_already_owns(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        self.assertTrue(owner.adopt(pet))
        self.assertFalse(owner.adopt(pet))
        self.assertTrue(owner.owns(pet))
        self.assertIs(pet.get_owner(), owner)

    def test_owner_adopts_a_pet_owned_by_someone(self):
        alice = Owner("Alice")
        bob = Owner("Bob")
        pet = Pet("Tom")

        self.assertTrue(alice.adopt(pet))
        self.assertTrue(bob.adopt(pet))

        self.assertFalse(alice.owns(pet))
        self.assertTrue(bob.owns(pet))
        self.assertIs(pet.get_owner(), bob)

    def test_owner_abandon_pet_it_owns(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        self.assertTrue(owner.adopt(pet))
        self.assertTrue(owner.abandon(pet))

        self.assertFalse(owner.owns(pet))
        self.assertIsNone(pet.get_owner())

    def test_owner_abandon_pet_it_does_not_own(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        self.assertFalse(owner.abandon(pet))

    def test_pet_gets_an_owner(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        pet.set_owner(owner)

        self.assertTrue(owner.owns(pet))
        self.assertIs(pet.get_owner(), owner)

    def test_pet_changes_an_owner(self):
        alice = Owner("Alice")
        bob = Owner("Bob")
        pet = Pet("Tom")

        pet.set_owner(alice)

        self.assertTrue(alice.owns(pet))
        self.assertFalse(bob.owns(pet))
        self.assertIs(pet.get_owner(), alice)

        pet.set_owner(bob)

        self.assertFalse(alice.owns(pet))
        self.assertTrue(bob.owns(pet))
        self.assertIs(pet.get_owner(), bob)

    def test_pet_loses_an_owner(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        pet.set_owner(owner)

        self.assertTrue(owner.owns(pet))
        self.assertIs(pet.get_owner(), owner)

        pet.set_owner(None)

        self.assertFalse(owner.owns(pet))
        self.assertIsNone(pet.get_owner())

    def test_pet_changes_its_owner_to_the_same_owner(self):
        owner = Owner("Alice")
        pet = Pet("Tom")

        self.assertTrue(pet.set_owner(owner))
        self.assertFalse(pet.set_owner(owner))

        self.assertTrue(owner.owns(pet))
        self.assertIs(pet.get_owner(), owner)


unittest.main(exit=False, verbosity=2)
