from Reddit_Endo.Init import Init
from collections import defaultdict
from collections import OrderedDict
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import urllib.request
import json
import itertools

# https://github.com/arimorcos/getRedditDataset
init = Init()
users = defaultdict(int)

def returnUserDemographics(user, n_subRed):
    try:
        duration = init.duration
        six_months = date.today() - relativedelta(months=int(duration))
        sub = init.ConnectToReddit()
        if n_subRed == 'hot':
          endo = sub.subreddit(init.subReddit).hot(limit=None)
        else:
          endo = sub.subreddit(init.subReddit).new(limit=None)
        count = 0
        for hot_msg in endo:
            if not hot_msg.stickied:
                created_date = datetime.utcfromtimestamp(hot_msg.created)
             #  count += 1

                if created_date.date() > six_months:
                    hot_msg.comments.replace_more(limit=5) #
                    comments = hot_msg.comments.list()
                    for cmt in comments:
                        user[cmt.author] += 1

        return user

    except Exception as e:
         init.logger.writeError(e)

sub_reddits = ['hot', 'new']
for sub_red in sub_reddits:
      users =  returnUserDemographics(users, sub_red)

sorted_user = OrderedDict(sorted(users.items(), key=lambda kv:kv[1], reverse=True))
users = list(itertools.islice(sorted_user.items(), 0, 20))
#https://github.com/praw-dev/praw/issues?page=2&q=is%3Aissue+is%3Aclosed
users_non_endo_submissions = defaultdict(list)
for user in users:
    try:
        url = urllib.request.urlopen("https://api.pushshift.io/reddit/comment/search?metadata=true&before=0d&limit=1000&sort=desc&author=" + user)
        user_data = json.loads(url.read().decode())
        comment_num = user_data["metadata"]["results_returned"]
        total = user_data["metadata"]["total_results"]
        users_non_endo_submissions['Anne1662'] = defaultdict(int)
        for j in range(0, comment_num):
            comment = user_data["data"][j]
            body = comment['body']
            subreddit = comment['subreddit']
            date = datetime.utcfromtimestamp(comment['created_utc'])
            users_non_endo_submissions[user][subreddit] += 1
    except Exception as e:
        print(e)
   # comments_new = user.get_comments(time='week', limit=None)
    #comments_top = user.get_comments(limit=None, sort = 'top')
#init.fileWriter(user)

sorted_user = OrderedDict(sorted(user.items(), key=lambda kv:kv[1], reverse=True))
for k, v in sorted_user.items():
        print(k)
        print(v)

# https://www.reddit.com/r/redditdev/comments/8suiqu/scrape_all_submissions_and_comments_made_by_a/
