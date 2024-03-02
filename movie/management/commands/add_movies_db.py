from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        json_file_path = 'movie/management/commands/movies.json'

        with open(json_file_path, 'r') as file:
            movies_data = json.load(file)

        for movie_data in movies_data:
            # Asegúrate de que 'genre' esté presente y no sea None
            genre = movie_data.get('genre')
            if genre is not None:
                exist = Movie.objects.filter(title=movie_data['title']).first()
                if not exist:
                    Movie.objects.create(
                        title=movie_data['title'],
                        image='movie/images/default.jpg',
                        genre=genre,
                        year=movie_data['year']
                    )
