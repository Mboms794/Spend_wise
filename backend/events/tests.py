
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from events.models import Event
from transactions.models import Transaction


class EventAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='event_user',
            email='event@example.com',
            password='TestPassword123!'
        )

        self.client.force_authenticate(user=self.user)

        self.url = reverse('event-list-create')

    def create_event(self, **overrides):
        data = {
            'name': 'Company Seminar',
            'description': 'Annual company seminar',
            'budget': '100000.00',
            'event_date': '2026-12-15',
        }

        data.update(overrides)

        return Event.objects.create(
            user=self.user,
            **data
        )

    def test_user_can_create_event(self):
        data = {
            'name': 'Company Seminar',
            'description': 'Annual company seminar',
            'budget': '100000.00',
            'event_date': '2026-12-15',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

        event = Event.objects.first()
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.name, 'Company Seminar')

    def test_unauthenticated_user_cannot_access_events(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_event_rejects_zero_and_negative_budgets(self):
        for amount in ['0.00', '-100.00']:
            with self.subTest(amount=amount):
                data = {
                    'name': 'Invalid Event',
                    'description': 'Testing invalid budget',
                    'budget': amount,
                    'event_date': '2026-12-15',
                }

                response = self.client.post(
                    self.url,
                    data,
                    format='json'
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST
                )

        self.assertEqual(Event.objects.count(), 0)

    def test_user_can_only_see_own_events(self):
        self.create_event()

        another_user = User.objects.create_user(
            username='another_event_user',
            email='another_event@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_access_another_users_event(self):
        event = self.create_event()

        another_user = User.objects.create_user(
            username='another_event_user',
            email='another_event@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        detail_url = reverse(
            'event-detail',
            kwargs={'pk': event.pk}
        )

        response = self.client.get(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_user_can_retrieve_own_event(self):
        event = self.create_event()

        detail_url = reverse(
            'event-detail',
            kwargs={'pk': event.pk}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Company Seminar')

    def test_user_can_update_own_event(self):
        event = self.create_event()

        detail_url = reverse(
            'event-detail',
            kwargs={'pk': event.pk}
        )

        response = self.client.patch(
            detail_url,
            {'name': 'Updated Seminar'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event.refresh_from_db()
        self.assertEqual(event.name, 'Updated Seminar')

    def test_user_can_delete_own_event(self):
        event = self.create_event()

        detail_url = reverse(
            'event-detail',
            kwargs={'pk': event.pk}
        )

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Event.objects.filter(pk=event.pk).exists()
        )

    def test_user_cannot_update_or_delete_another_users_event(self):
        event = self.create_event()

        another_user = User.objects.create_user(
            username='another_event_user',
            email='another_event@example.com',
            password='AnotherPassword123!'
        )

        self.client.force_authenticate(user=another_user)

        detail_url = reverse(
            'event-detail',
            kwargs={'pk': event.pk}
        )

        update_response = self.client.patch(
            detail_url,
            {'name': 'Unauthorized Update'},
            format='json'
        )

        delete_response = self.client.delete(detail_url)

        self.assertEqual(
            update_response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            delete_response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertTrue(
            Event.objects.filter(pk=event.pk).exists()
        )

    def test_event_spending_calculations(self):
        event = self.create_event()

        Transaction.objects.create(
            user=self.user,
            event=event,
            title='Venue Payment',
            amount=Decimal('30000.00'),
            transaction_type='expense',
            category='business',
            date='2026-12-10'
        )

        Transaction.objects.create(
            user=self.user,
            event=event,
            title='Catering Payment',
            amount=Decimal('20000.00'),
            transaction_type='expense',
            category='food',
            date='2026-12-11'
        )

        # Income should not count as event spending.
        Transaction.objects.create(
            user=self.user,
            event=event,
            title='Event Sponsorship',
            amount=Decimal('10000.00'),
            transaction_type='income',
            category='business',
            date='2026-12-12'
        )

        detail_url = reverse(
            'event-detail',
            kwargs={'pk': event.pk}
        )

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            Decimal(str(response.data['total_spent'])),
            Decimal('50000.00')
        )

        self.assertEqual(
            Decimal(str(response.data['remaining_budget'])),
            Decimal('50000.00')
        )

