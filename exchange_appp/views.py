from django.shortcuts import render
from .models import Item
from .forms import ItemForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import DetailView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from .models import ExchangeRequest
from django.http import HttpResponseBadRequest


# Головна сторінка
def index(request):
    items = Item.objects.all()
    return render(request, 'exchange_appp/index.html', {'title': 'Головна сторінка сайту', 'items': items})


# Сторінка "Мої речі"
@login_required
def my(request):
    title = 'Мої речі'
    my_items = Item.objects.filter(user=request.user)
    return render(request, 'exchange_appp/my.html', {'title1': 'Мої речі', 'items': my_items})


# Реєстрація нового користувача
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Автоматична автентифікація користувача
            login(request, user)
            
            return redirect('MyItems')
    else:
        form = UserCreationForm()
    return render(request, 'exchange_appp/registration.html', {'title2': 'Реєстрація', 'form': form})


# Вхід користувача
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('MyItems')
        else:
            error_message = "Невірний логін або пароль. Спробуйте ще раз."
    else:
        form = AuthenticationForm()
        error_message = None

    return render(request, 'exchange_appp/login.html', {'title3': 'Вхід', 'form': form, 'error_message': error_message})


# Створення нового предмету користувачем
@login_required
def create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('MyItems')  
    else:
        form = ItemForm()

    return render(request, 'exchange_appp/create.html', {'form': form})


# Деталі предмету та обробка запитів на обмін
class ItemDetailView(DetailView):
    model = Item
    template_name = 'exchange_appp/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_items = Item.objects.filter(user=self.request.user)
        context['user_items'] = user_items
        return context

    def post(self, request, pk):
        item = Item.objects.get(pk=pk)
        if 'exchangeItem' in request.POST:
            selected_item_id = request.POST['exchangeItem']
            selected_item = Item.objects.get(pk=selected_item_id)
            
            # Створення запиту на обмін, встановлення відправника і отримувача відповідно
            ExchangeRequest.objects.create(
                sender=request.user,
                receiver=item.user,  # Встановлюємо власника поточного товару, а не власника вибраного товару для обміну
                item_offered=item,
                item_requested=selected_item
            )
            messages.success(request, 'Запит на обмін відправлено!')
            return redirect('ItemDetali', pk=pk)

        return render(request, 'exchange_appp/item_detail.html', {'item': item})


# Сторінка з обмінними запитами
class ExchangeRequestsView(View):
    def get(self, request):
        sent_requests = ExchangeRequest.objects.filter(sender=request.user, is_accepted=False)
        received_requests = ExchangeRequest.objects.filter(receiver=request.user, is_accepted=False)
        return render(request, 'exchange_appp/exchange_requests.html', {'sent_requests': sent_requests, 'received_requests': received_requests})

    def post(self, request):
        if 'cancelRequest' in request.POST:
            request_id = request.POST['cancelRequest']
            exchange_request = ExchangeRequest.objects.get(pk=request_id)

            # Перевірка, чи користувач є відправником або отримувачем запиту
            if exchange_request.sender == request.user or exchange_request.receiver == request.user:
                exchange_request.delete()
                messages.success(request, 'Запит на обмін відмінено!')
            else:
                messages.error(request, 'Ви не можете відмінити запит, який не є вашим.')

        elif 'confirmRequest' in request.POST:
            request_id = request.POST['confirmRequest']
            exchange_request = ExchangeRequest.objects.get(pk=request_id)

            # Перевірка, чи користувач є отримувачем запиту
            if exchange_request.receiver == request.user:
                exchange_request.is_accepted = True
                exchange_request.save()
                messages.success(request, 'Запит на обмін підтверджено!')
            else:
                messages.error(request, 'Ви не можете підтвердити цей запит.')

        return redirect('ExchangeRequests')
