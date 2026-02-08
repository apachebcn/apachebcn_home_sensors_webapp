from django.test import TestCase
from django.contrib.auth.models import User
from .models import InputDataHistory

class InputDataHistoryTests(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='apachebcn', password='securepassword')

        # Crear una instancia de InputDataHistory con el usuario de prueba
        self.obj = InputDataHistory.objects.create(
            user_id=self.user,
            data_s1_temp=15,
        )

    def test_objeto_creado(self):
        # Verificar que la instancia del modelo se haya creado correctamente
        self.assertEqual(self.obj.data_s1_temp, 15)
        self.assertEqual(self.obj.user_id, self.user)

    def test_otro_comportamiento(self):
        # Verificar el método es_valido() (si existe)
        self.assertEqual(self.obj.user_id, self.user)
