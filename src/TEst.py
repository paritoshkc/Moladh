# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:23:41 2019

@author: Esmond Dsouza
"""

import json
import requests


class MovieDetails:
    def __init__(self, page, totalResults, totalPages, movieLists):
        self.page = page
        self.totalResults = totalResults
        self.totalPages = totalPages
        self.movieLists = movieLists


api_url = 'https://api.themoviedb.org/3/discover/movie?api_key=1bdb3c9ec250982017d0358e85f4f30a&language=en-US&sort_by=popularity.desc&include_video=false&page=1&with_genres=12';
headers = {}
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = json.loads(response.content)
    movieDetails1 = MovieDetails(data["page"], data["total_results"], data["total_pages"], data["results"])
    print('Its working')
    print(movieDetails1.movieLists)
else:
    print('Error')

print(movieDetails1.page)


