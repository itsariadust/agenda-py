import unittest
from datetime import datetime
from src.main import Agenda, Event
import random
import string


class TestAgendaSystem(unittest.TestCase):

    def setUp(self):
        self.agenda = Agenda()  # Create an instance of your Agenda class

        # Create a few test events
        self.event_id1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.event1 = Event(
            uid = self.event_id1,
            name = "Test Event 1",
            description = "Description for event 1",
            all_day = "no",
            start_date = datetime(2024, 9, 10, 9, 0).date(),
            end_date = datetime(2024, 9, 10, 10, 0).date(),
            start_time=datetime(2024, 9, 10, 9, 0).time(),
            end_time=datetime(2024, 9, 10, 10, 0).time()
        )

        self.event_id2 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.event2 = Event(
            uid = self.event_id2,
            name = "Test Event 2",
            description = "Description for event 2",
            all_day = "yes",
            start_date = datetime(2024, 9, 11, 0, 0).date(),
            end_date = datetime(2024, 9, 11, 23, 59).date(),
            start_time=datetime(2024, 9, 11, 0, 0).time(),
            end_time=datetime(2024, 9, 11, 23, 59).time(),
        )

    def tearDown(self):
        self.agenda = None  # Clean up the agenda instance

    # Test adding an event
    def test_add_event(self):
        self.agenda.add_event(self.event1)
        self.assertIn(self.event_id1, self.agenda.events)
        self.assertEqual(self.agenda.events[self.event_id1].name, "Test Event 1")

    # Test editing an event
    def test_edit_event(self):
        self.agenda.add_event(self.event1)
        self.agenda.edit_event(uid=self.event_id1, name="Updated Event 1", description="Updated description")
        self.assertEqual(self.agenda.events[self.event_id1].name, "Updated Event 1")
        self.assertEqual(self.agenda.events[self.event_id1].description, "Updated description")

    # Test removing an event
    def test_remove_event(self):
        self.agenda.add_event(self.event1)
        self.agenda.remove_event(self.event_id1)
        self.assertNotIn(self.event_id1, self.agenda.events)

    # Test searching by event ID
    def test_search_event_by_id(self):
        self.agenda.add_event(self.event1)
        result = self.agenda.get_event_by_id(self.event_id1)
        self.assertEqual(result.name, "Test Event 1")

    # Test printing events within 7 days
    def test_print_events_within_7_days(self):
        self.agenda.add_event(self.event1)
        self.agenda.add_event(self.event2)

        events_within_7_days = self.agenda.get_events_within_7_days()
        self.assertEqual(len(events_within_7_days), 2)

    # Test adding all-day event
    def test_all_day_event(self):
        self.agenda.add_event(self.event2)
        self.assertEqual(self.agenda.events[self.event_id2].all_day, "yes")


# Run the tests
if __name__ == '__main__':
    unittest.main()
