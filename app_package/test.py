from twython import Twython

import twitter_credentials as tc





def get_profileTwython(username):

    twitter = Twython(tc.CONSUMER_KEY, tc.CONSUMER_SECRET, tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
    twitter.verify_credentials()
    #twitter.get_home_timeline()

    profile= twitter.show_user(screen_name= '_alexgalo')

    name = profile['name']
    profile_img = profile['profile_image_url']
    username = profile['screen_name']
    location = profile['location']
    created_at = profile['created_at']
    post = profile['statuses_count']
    followers = profile['followers_count']
    following = profile['friends_count']
    description = profile['description']

    # Almacena la información relacionada al perfil.
    user_profile_Y = dict()

    user_profile_Y = {'name': name,
                    'username': username,
                    'location': location,
                    'created_at': created_at,
                    'post': post,
                    'followers': followers,
                    'following': following,
                    'description': description,
                    'profile_img': profile_img

    }

    print('Finish')

    return user_profile_Y


"""
for key, value in profile.items() :
    print (key, value)
"""

get_profileTwython('_alexgalo')