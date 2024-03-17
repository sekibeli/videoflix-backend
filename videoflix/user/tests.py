from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core import mail
from django.contrib.auth.tokens import default_token_generator

from videoflixbackend.models import Video
from user.models import CustomUser

from django.core.files.base import ContentFile


# class LoginTest(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
#         self.user.is_verified = True
#         self.user.save()

#     def test_successful_login(self):
#         url = reverse('login')
#         data = {'username': 'testuser', 'password': 'testpassword'}
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('token' in response.data)
    
#     def test_login_wrong_password(self):
#         url = reverse('login')
#         data = {'username': 'testuser', 'password': 'wrongpassword'}
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertTrue('error' in response.data)

#     def test_login_wrong_username(self):
#         url = reverse('login')
#         data = {'username': 'wrongusername', 'password': 'testpassword'}
#         response = self.client.post(url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertTrue('error' in response.data)


# class SignupTests(APITestCase):
#     def setUp(self):
#         self.signup_url = reverse('signup')  

#     def test_successful_signup(self):
#         data = {
#             'username': 'neuerbenutzer',
#             'email': 'neu@example.com',
#             'password': 'testpassword123'
#         }
#         response = self.client.post(self.signup_url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(CustomUser.objects.filter(email='neu@example.com').exists())
#         self.assertEqual(len(mail.outbox), 1) 
#         self.assertIn('Please confirm your email', mail.outbox[0].subject)

#     def test_signup_existing_email(self):
#         CustomUser.objects.create_user(username='existinguser', email='existing@example.com', password='testpassword123')

#         data = {
#         'username': 'newuser',
#         'email': 'existing@example.com',  # Gleiche E-Mail wie oben
#         'password': 'testpassword123'
#         }
#         response = self.client.post(self.signup_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertContains(response, "An error occured", status_code=status.HTTP_400_BAD_REQUEST)


#     def test_signup_short_password(self):
#         data = {
#             'username': 'userwithshortpass',
#             'email': 'shortpass@example.com',
#             'password': 'short'  # Passwort ist zu kurz
#         }
#         response = self.client.post(self.signup_url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertContains(response, "This password is too short", status_code=status.HTTP_400_BAD_REQUEST)


# class GuestLoginTests(APITestCase):
#     def setUp(self):
#         self.guest_login_url = reverse('guest-login') 

#     def test_guest_login_creates_user_and_token(self):
#         response = self.client.post(self.guest_login_url, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)
#         self.assertIn('user_id', response.data)
#         self.assertIn('email', response.data)  

#         self.assertTrue(CustomUser.objects.filter(pk=response.data['user_id']).exists())

#         user = CustomUser.objects.get(pk=response.data['user_id'])
#         token = Token.objects.get(user=user)
#         self.assertEqual(response.data['token'], token.key)


# class LoggedUserViewTests(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

#         self.logged_user_url = reverse('edit-user') 

#     def test_get_logged_user_data(self):
#         response = self.client.get(self.logged_user_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['username'], self.user.username)

#     def test_update_logged_user_data(self):
#         new_email = 'newemail@example.com'
#         response = self.client.patch(self.logged_user_url, {'email': new_email}, format='json')
#         self.user.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(self.user.email, new_email)


# class UserDeletionTests(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

#         self.delete_url = reverse('delete-user')

#     def test_user_deletion(self):
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         user_exists = CustomUser.objects.filter(username='testuser').exists()
#         self.assertFalse(user_exists)


# class ResetPasswordViewTests(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='oldpassword')
#         self.url = '/api/password_reset/'

#         self.token = default_token_generator.make_token(self.user)

#     def test_reset_password_success(self):
#         data = {
#             'email': 'test@example.com',
#             'token': self.token,
#             'password': 'newpassword123'
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('newpassword123'))


# class ToggleLikeTests(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        
#         dummy_video_file = ContentFile(b"dummy video data", name='dummy_video.mp4')
        
#         self.video = Video.objects.create(title='Test Video', video_file=dummy_video_file)  # Füge das Dummy-Dateiobjekt hinzu
        
#         self.token, _ = Token.objects.get_or_create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.toggle_like_url = reverse('toggle-like', kwargs={'videoId': self.video.pk})  

#     def test_like_video(self):
#         self.assertFalse(self.user in self.video.likes.all())

#         response = self.client.post(self.toggle_like_url)
#         self.video.refresh_from_db() 

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(self.user in self.video.likes.all())
#         self.assertEqual(response.data['liked'], True)

#     def test_unlike_video(self):
#         self.video.likes.add(self.user)
#         self.assertTrue(self.user in self.video.likes.all())

#         response = self.client.post(self.toggle_like_url)
#         self.video.refresh_from_db()  

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(self.user in self.video.likes.all())
#         self.assertEqual(response.data['liked'], False)