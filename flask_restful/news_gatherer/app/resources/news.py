from bs4 import BeautifulSoup
from flask_restful import Resource, reqparse
import requests

class GetNews(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', choices=['bbc', 'guardian'])
        args = parser.parse_args()
        if args['source'] == 'bbc':
            response = requests.get('https://www.bbc.co.uk/news')
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find('div', class_="nw-c-most-read__items gel-layout gel-layout--no-flex").find('ol').contents
                return {'articles:': [article.text for article in items]}, 201
            else:
                return {"message": "could not parse page"}, 500
        if args['source'] == 'guardian':
            response = requests.get('https://www.theguardian.com/uk')
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find_all('span', class_="js-headline-text")[:10]
                return {'articles:': [article.text for article in items]}, 201
            else:
                return {"message": "could not parse page"}, 500
