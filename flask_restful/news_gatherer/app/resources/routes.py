from abc import ABC, abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup
from flask import g, make_response
from flask.json import jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_restful import Resource, reqparse
import requests

from app import db
from app.resources.models import NewsRequest, NewsSource
from app.resources.authorization import tokenauth

class NewsGatherer(ABC):

    @abstractmethod
    def get_news(self):
        raise NotImplementedError()


class BBCGatherer(NewsGatherer):

    def get_news(self):
        response = requests.get('https://www.bbc.co.uk/news')
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find('div', class_="nw-c-most-read__items gel-layout gel-layout--no-flex").find('ol').contents
            return make_response(jsonify({'articles:': [article.text for article in articles]}), 201)
        else:
            return make_response(jsonify({"message": "could not parse page"}), 500)


class GuardianGatherer(NewsGatherer):

    def get_news(self):
        response = requests.get('https://www.theguardian.com/uk')
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('span', class_="js-headline-text")[:10]
            return make_response(jsonify({'articles:': [article.text for article in articles]}), 201)
        else:
            return make_response(jsonify({"message": "could not parse page"}), 500)


class MetroGatherer(NewsGatherer):

    def get_news(self):
        response = requests.get(r'https://metro.co.uk/')
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find(attrs={'id': 'channel-bottom'}).find('ol').find_all('li')
            return make_response(jsonify({'articles': [article.text.strip() for article in articles]}), 201)
        else:
            return make_response(jsonify({"message": "could not parse page"}), 500)


class GetNews(Resource):
    @tokenauth.login_required
    def post(self):
        user = g.get('current_user')
        parser = reqparse.RequestParser()
        parser.add_argument('source', choices=['bbc', 'guardian', 'metro'])
        args = parser.parse_args()
        news_source = NewsSource.query.filter(NewsSource.source_name.like(args['source'])).first()
        news_request = NewsRequest(user_id=user.id, news_source=news_source.source_id, request_date=datetime.now())
        db.session.add(news_request)
        db.session.commit()
        news_gatherer = {'bbc': BBCGatherer(), 'guardian': GuardianGatherer(), 'metro': MetroGatherer()}.get(args['source'])
        return news_gatherer.get_news()
