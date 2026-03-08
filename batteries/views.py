import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages

from .models import BatterySubmission
from .forms import RegisterForm, BatterySubmissionForm
from .cities import RUSSIAN_CITIES, CITY_ABSENT
from .city_coordinates import CITY_COORDINATES


def home(request):
    """Главная: общее количество сданных батареек и карта по городам."""
    total = BatterySubmission.objects.aggregate(total=Sum('count'))['total'] or 0
    # Сумма по городам (только города с хотя бы одной сдачей)
    city_totals_qs = (
        BatterySubmission.objects.values('city')
        .annotate(total=Sum('count'))
        .order_by('-total')
    )
    # Добавляем координаты; пропускаем город, если координат нет
    cities_on_map = []
    for row in city_totals_qs:
        city_name = row['city']
        coords = CITY_COORDINATES.get(city_name)
        if coords:
            cities_on_map.append({
                'city': city_name,
                'total': row['total'],
                'lat': coords[0],
                'lon': coords[1],
            })
    return render(request, 'batteries/home.html', {
        'total_batteries': total,
        'cities_on_map': cities_on_map,
        'cities_on_map_json': json.dumps(cities_on_map, ensure_ascii=False),
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('batteries:my_submissions')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('batteries:my_submissions')
    else:
        form = RegisterForm()
    return render(request, 'batteries/register.html', {'form': form})


@login_required
def my_submissions(request):
    """Мои сдачи и форма добавления."""
    submissions = BatterySubmission.objects.filter(user=request.user)
    user_total = submissions.aggregate(s=Sum('count'))['s'] or 0

    if request.method == 'POST':
        form = BatterySubmissionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, f'Добавлено {obj.count} батареек.')
            return redirect('batteries:my_submissions')
    else:
        form = BatterySubmissionForm()

    # Список для автоподстановки: города + "Город отсутствует" первым
    cities_for_autocomplete = [CITY_ABSENT] + sorted(RUSSIAN_CITIES)
    return render(request, 'batteries/my_submissions.html', {
        'submissions': submissions,
        'user_total': user_total,
        'form': form,
        'cities_json': json.dumps(cities_for_autocomplete, ensure_ascii=False),
    })
