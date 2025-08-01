from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Модель предмету
class Item(models.Model):
    # Вибір категорії предмету
    CATEGORY_CHOICES = [
        ('electronic', 'Електроніка'),
        ('clothing', 'Одяг'),
        ('shoes', 'Взуття'),
        ('accessories', 'Аксесуари'),
        ('toys', 'Іграшки'),
        ('furniture', 'Меблі'),
        ('repair', 'Ремонт'),
        ('auto', 'Авто'),
        ('animals', 'Тварини'),
        ('hobby', 'Хоббі і відпочинок'),
        ('sport', 'Спорт'),
        ('other', 'Інше'),
    ]

    # Назва предмету
    title = models.CharField('Назва речі', max_length=50)
    # Опис предмету
    description = models.TextField('Опис речі', max_length=100)
    # Категорія предмету
    category = models.CharField('Категорія', max_length=20, choices=CATEGORY_CHOICES)
    # Категорія для обміну предмету
    exchange_category = models.CharField('Категорія для обміну', max_length=20, choices=CATEGORY_CHOICES)
    # Фото предмету
    image = models.ImageField('Фото', upload_to='media/', null=True, blank=True)
    # Користувач, що додав предмет
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Повертає відображення категорії предмету
    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES)[self.category]

    # Повертає відображення категорії для обміну предмету
    def get_exchange_category_display(self):
        return dict(self.CATEGORY_CHOICES)[self.exchange_category]

    # Повертає URL фото предмету, якщо воно існує
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    # Представлення предмету у форматі рядка
    def __str__(self):
        return self.title 

    class Meta:
        verbose_name = 'Річ'
        verbose_name_plural = 'Речі'

# Модель запиту на обмін
class ExchangeRequest(models.Model):
    # Користувач, що відправив запит
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    # Користувач, що отримав запит
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    # Предмет, що пропонується для обміну
    item_offered = models.ForeignKey('Item', related_name='offered_requests', on_delete=models.CASCADE)
    # Предмет, що запитується для обміну
    item_requested = models.ForeignKey('Item', related_name='requested_requests', on_delete=models.CASCADE)
    # Чи був запит на обмін прийнятий
    is_accepted = models.BooleanField(default=False)

    # Представлення запиту на обмін у форматі рядка
    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username} - {self.item_offered.title} for {self.item_requested.title}'

    class Meta:
        verbose_name = 'Запит на обмін'
        verbose_name_plural = 'Запити на обмін'
