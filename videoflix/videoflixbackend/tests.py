# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Video
# from django.contrib.auth.models import User

# class VideoViewSetTestCase(APITestCase):
#     def setUp(self):
#         #Video-Instanzen für Testzwecke
#         Video.objects.create(title="Video 1", description="Wichtiger Inhalt 1", category="funny", video_file="http://localhost:8000/media/videos/IMG_0866.mp4")
#         Video.objects.create(title="Video 2", description="Wichtiger Inhalt 2" ,category="kids", video_file="http://localhost:8000/media/videos/IMG_0866.mp4")
#         Video.objects.create(title="Video 3", description="Wichtiger Inhalt 3" ,category="kids", video_file="http://localhost:8000/media/videos/IMG_0866.mp4")

#        #Benutzer, wenn Authentifizierung erforderlich ist
#         # self.user = User.objects.create_user(username='testuser', password='12345')
#         # self.client.login(username='testuser', password='12345')

#     def test_get_queryset(self):
#         # Test, ob die Filterung nach Kategorien funktioniert
#         url = reverse('video-list') + '?category=kids'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)  # Erwarte zwei Videos in der Kategorie "kids"

#     def test_list_videos(self):
#         # Testen, ob die Liste-API wie erwartet funktioniert
#         url = reverse('video-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 3)  # Erwarte insgesamt alle drei Videos


