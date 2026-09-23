from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import UploadedFile


class GalleryTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username='owner',
            password='password',
        )
        self.other_user = get_user_model().objects.create_user(
            username='other',
            password='password',
        )
        self.uploaded_file = UploadedFile.objects.create(
            owner=self.owner,
            original_file_name='photo.jpg',
            file=SimpleUploadedFile('photo.jpg', b'image data', content_type='image/jpeg'),
        )

    def tearDown(self):
        self.uploaded_file.file.delete(save=False)
        super().tearDown()

    def test_gallery_shows_image_preview(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse('vault:gallery'))

        self.assertContains(response, self.uploaded_file.file.url)
        self.assertContains(response, 'photo.jpg')

    def test_owner_can_delete_file(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('vault:delete', args=[self.uploaded_file.id]),
        )

        self.assertRedirects(response, reverse('vault:gallery'))
        self.assertFalse(UploadedFile.objects.filter(id=self.uploaded_file.id).exists())

    def test_user_cannot_delete_another_users_file(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('vault:delete', args=[self.uploaded_file.id]),
        )

        self.assertRedirects(response, reverse('vault:gallery'))
        self.assertTrue(UploadedFile.objects.filter(id=self.uploaded_file.id).exists())
