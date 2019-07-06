"""Main application and routing logic for TwitOff."""
from decouple import config 
from flask import Flask, render_template, request

from .models import DB, User
from .twitter import add_or_update_user, get_trending, compare_trending, compare_topics, compare_names
from .nltk import top_words

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)


    @app.route('/')
    def root():
        users = User.query.all()
        names = ['ewarren', 'JoeBiden', 'KamalaHarris', 'BernieSanders', 'realDonaldTrump', 'BetoORourke', 'sethmoulton', 
                  'JoeSestak', 'JayInslee', 'GovBillWeld', 'AndrewYang', 'MichaelBennet']
        for name in names:
                add_or_update_user(name)
        top_word = top_words(names)
        candidate_names = compare_names(names)
        trends = get_trending()
        candidate_trends = compare_trending(names, trends)
        return render_template('home.html', title='Home', users=users, top_word=top_word,
                                candidate_names=candidate_names, candidate_trends=candidate_trends, trends=trends)


    @app.route('/topics', methods=['POST'])
    def topics():
        topics = request.values['topics']
        names = ['ewarren', 'JoeBiden', 'KamalaHarris', 'BernieSanders', 'realDonaldTrump', 'BetoORourke', 'sethmoulton', 
                  'JoeSestak', 'JayInslee', 'GovBillWeld', 'AndrewYang', 'MichaelBennet']
        candidate_topics = compare_topics(names, topics)
        return render_template('topics.html', title='Trends', topics=topics, 
                        candidate_topics=candidate_topics)

   
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message = ''
        name = name
        try:
            message = 'User {} succesfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets[:5]
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                                message=message, name=name)

    @app.route('/resetreset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('home.html', title='DB Reset!', users=[])
        
    return app

