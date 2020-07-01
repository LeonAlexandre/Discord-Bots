import os
from dotenv import load_dotenv
import praw

load_dotenv()
username_reddit = os.getenv('USERNAME_REDDIT')
password_reddit = os.getenv('PASSWORD_REDDIT')

my_client_id = os.getenv('CLIENT_ID_REDDIT')
my_client_secret = 	os.getenv('CLIENT_SECRET_REDDIT')
my_user_agent = os.getenv('USER_AGENT_REDDIT')

reddit = praw.Reddit(client_id=my_client_id, 
                    client_secret=my_client_secret, 
                    user_agent=my_user_agent,
                    username=username_reddit,
                    password=password_reddit,
                    )

class RedditBot():
    def __init__(self):
        self.driver = praw.Reddit(client_id=my_client_id, 
                    client_secret=my_client_secret, 
                    user_agent=my_user_agent,
                    username=username_reddit,
                    password=password_reddit,
                    )
        self.current_post = None
    
    def get_post_new(self, sub):
        