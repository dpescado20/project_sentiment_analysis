from flask import Blueprint
from flask_restplus import Api, Resource

app_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(app=app_api)

ns_sa = api.namespace('nlp', description='Natural Language Process')
ns_metrics = api.namespace('metrics', description='Metrics')


# # # # NLP ROUTES # # # #
@ns_sa.route('/sentiment_score/<string:text>/')
class Sentiment(Resource):
    def get(self):
        """
        Returns Sentiment Score of given Text
        """
        return True


@ns_sa.route('/bag_of_words/<string:text>/')
class Sentiment(Resource):
    def get(self):
        """
        Returns Bag of Words of given Text
        """
        return True


# # # # METRICS ROUTES # # # #
@ns_metrics.route('/f1_score/<string:text>/')
class Sentiment(Resource):
    def get(self):
        """
        Returns F1 Score of the Classifier
        """
        return True


@ns_metrics.route('/precision/<string:text>/')
class Sentiment(Resource):
    def get(self):
        """
        Returns Precision Value of the Classifier
        """
        return True


@ns_metrics.route('/recall/<string:text>/')
class Sentiment(Resource):
    def get(self):
        """
        Returns Recall Value of the Classifier
        """
        return True


@ns_metrics.route('/classification_report/<string:text>/')
class Sentiment(Resource):
    def get(self):
        """
        Returns Classification Report of the Classifier
        """
        return True


@ns_metrics.route('/confusion_matrix/<string:text>/')
class Sentiment(Resource):
    def get(self):
        """
        Returns Confusion Matrix of the Classifier
        """
        return True
