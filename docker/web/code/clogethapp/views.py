from django.shortcuts import render

# Create your views here.
from .models import Block,Transaction

def post_home(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:4]
    # news = News.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:4]
    # sliders = SliderHome.objects.filter(is_enable=True).order_by('-published_date')[:4]
    # gallery = Photo.objects.all()[:4]

    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
        # 'sliders': sliders,
        # 'posts': posts,
        # 'news': news,
        # 'gallery': gallery,
    })
def block_list(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })
def block(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })
def tx(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })
def tx_list(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })
def addr(request, pk):
    title = 'Главная - owasp.ru'
    keywords = 'owasp'
    return render(request, 'home.html', {
        'title': title,
        'keywords': keywords,
    })