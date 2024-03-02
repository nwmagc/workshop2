from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt 
import matplotlib
import io
import urllib,base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to my Home Page</h1>')
    #return render(request, 'home.html', {'name':'Lorena Goez'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})
def about(request):
    #return HttpResponse('<h1>This is the About page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_views(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('-year')[:26]
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = None
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions_year = range(len(movie_counts_by_year))

    plt.bar(bar_positions_year, movie_counts_by_year.values(), width=bar_width, align='center')

    plt.title('Películas por año')
    plt.xlabel('Año')
    plt.ylabel('Número de películas')
    plt.xticks(bar_positions_year, movie_counts_by_year.keys(), rotation=45, ha="right", rotation_mode="anchor")

    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()

    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Generar la segunda gráfica (por género)
    matplotlib.use('Agg')
    genres = Movie.objects.exclude(genre__isnull=True).values_list('genre', flat=True).distinct().order_by('genre')[:26]
    movie_counts_by_genre = {}

    for genre in genres:
        movies_in_genre = Movie.objects.filter(genre__startswith=genre)
        count = movies_in_genre.count()
        movie_counts_by_genre[genre] = count

    bar_positions_genre = range(len(movie_counts_by_genre))

    plt.figure()  # Crear una nueva figura para la segunda gráfica

    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center', color='orange')

    plt.title('Películas por género')
    plt.xlabel('Género')
    plt.ylabel('Número de películas')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=45, ha="right", rotation_mode="anchor")

    plt.subplots_adjust(bottom=0.3)
    buffer_genre = io.BytesIO()

    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()

    image_genre_png = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_genre_png)
    graphic_genre = graphic_genre.decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic, 'graphic_genre': graphic_genre})
