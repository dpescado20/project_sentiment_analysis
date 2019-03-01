from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

api_key = 'AIzaSyD9xwls_UC1qFXe5AiZOuQ34DMBAyyypPg'


# # # # YOUTUBE COMMENTS ANALYSER # # # #
class YoutubeAnalyser():
    def __init__(self, comments):
        self.comments = comments

    def tweet_analyser_scores(self):
        analyser = SentimentIntensityAnalyzer()
        score = analyser.polarity_scores(self.comments)
        return score


# # # # YOUTUBE COMMENTS GENERATOR # # # #
class YoutubeClient():
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_youtube_comments(self, video_title):
        req = self.youtube.search().list(
            q=video_title,
            part='snippet',
            type='video')
        res1 = req.execute()

        videoId_list = []
        for item in res1['items']:
            videoId_list.append(item['id']['videoId'])

        comments = []
        for id in videoId_list:
            com = self.youtube.commentThreads().list(
                part='snippet',
                videoId=id,
                order='relevance',
                textFormat='plainText')
            res2 = com.execute()

            for item in res2['items']:
                comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
        comments_str = ','.join(comments)
        return comments_str
