# Fetches CSS from one subreddit and applies it to other subreddits
# Subreddits to have CSS applied to MUST HAVE the delimiters in the CSS file.
# With the default delimiters the CSS should include a chunk of text like:
# 
# /* Network-Wide CSS - DO NOT EDIT HERE */
# 
# --Network css goes here--
#
# /* End Network CSS - SUBREDDIT-SPECIFIC CSS BELOW THIS LINE */
#
# --Subredit-specific CSS goes here--


import re
import reddit
import HTMLParser
from ConfigParser import SafeConfigParser
import sys, os
import shutil
import logging


import pprint

logging.basicConfig(level=logging.INFO)

# set up the config parser
cfg_file = SafeConfigParser()
path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
path_to_cfg = os.path.join(path_to_cfg, 'network-css.cfg')
cfg_file.read(path_to_cfg)


# defines the source and network subreddits
CSS_SUBREDDIT = 'sfwpornnetworkcss'
NETWORK_SUBREDDITS = ['dakta']
# CSS_SUBREDDIT = 'dakta'
# NETWORK_SUBREDDITS = ['ourhearts']

# login info for the script to log in as, this user must be a mod in the main subreddit
REDDIT_USERNAME = cfg_file.get('reddit', 'username')
REDDIT_PASSWORD = cfg_file.get('reddit', 'password')
REDDIT_UA = cfg_file.get('reddit', 'user_agent')

# don't change unless you want different delimiter strings for some reason
START_DELIM = '/* Network-Wide CSS - DO NOT EDIT HERE */'
END_DELIM = '/* End Network CSS - SUBREDDIT-SPECIFIC CSS BELOW THIS LINE */'


tmpdir = './tmp-'+CSS_SUBREDDIT

def login(username, password, user_agent):
    # log in to reddit
    logging.info("Logging in as /u/"+username+"...")
    r = reddit.Reddit(user_agent=user_agent)
    r.login(username, password)
    logging.info("  Success!")
    return r


def get_images(subreddit, directory, PRAW_object):
    ''' Downloads `subreddit`'s images into `directory`, returns a list of dicts containing
        all information about those images, and the subreddit's CSS text. Must pass in authenticated PRAW_object.
    '''

    # get the source stylesheet
    logging.info("Getting source stylesheet from /r/"+subreddit+"...")
    css_subreddit = PRAW_object.get_subreddit(subreddit)
    # fetch the stylesheet from the main subreddit
    source_style = css_subreddit.get_stylesheet()
    logging.info("  Success!")
    
    source_CSS = source_style['stylesheet']
    source_images = source_style['images']

    # cleanup
    # needs to happen before, in case it gets cut off by aborted execution
    if (os.path.isdir(tmpdir)):
        shutil.rmtree(tmpdir)
    
    # setup
    os.mkdir(tmpdir)

        
    image_file_map = []
    
    for image in source_images:
    	# os.system('cd '+tmpdir+'; wget '+image['url']+' -O '+image['name'])
    	# os.system('cd '+tmpdir+'; url='+image['url']+'; filename=$(basename "$url"); wget "$url"; touch "$filename"; mv $filename '+image['name'])
    	os.system('cd '+tmpdir+'; wget --quiet '+image['url'])
    	image_file_map.append({'name': image['name'], 'file': os.path.basename(image['url']), 'type': os.path.basename(image['url'].split('.')[-1])})
    pprint.pprint(os.listdir(tmpdir))
    pprint.pprint(image_file_map)
    
    return image_file_map, source_CSS

def upload_images(images, directory, subreddit, PRAW_object):
    ''' Uploads each image from `images` to `subreddit` from `directory`.
        Must pass authenticated PRAW_object.
    '''
    
    for image in images:
        PRAW_object.delete_image(subreddit, name=image['name'], header=False)
        PRAW_object.upload_image(subreddit, directory+'/'+image['file'], name=image['name'], header=False)
        


def main():
    r = login(REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_UA)
    images, stylesheet = get_images(CSS_SUBREDDIT, tmpdir, r)
    for subreddit in NETWORK_SUBREDDITS:
        upload_images(images, tmpdir, subreddit, r)
    

if __name__ == '__main__':
    main()