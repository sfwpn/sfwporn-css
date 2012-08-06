# Fetches CSS from one subreddit and applies it to other subreddits
# Subreddits to have CSS applied to MUST HAVE the delimiters in the CSS file.
# With the default delimiters the CSS should include a chunk of text like:
# 
# /*
#   Begin Network CSS - DO NOT EDIT
# */
#
# /*
#   End Network CSS - EDIT BELOW THIS LINE
# */
#
# (Subredit-specific CSS goes here.)


import re
import reddit
import HTMLParser
from ConfigParser import SafeConfigParser
import sys, os

# set up the config parser
cfg_file = SafeConfigParser()
path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
path_to_cfg = os.path.join(path_to_cfg, 'network-css.cfg')
cfg_file.read(path_to_cfg)


# defines the source and network subreddits
CSS_SUBREDDIT = 'dakta'
NETWORK_SUBREDDITS = ['ourhearts']

# login info for the script to log in as, this user must be a mod in the main subreddit
REDDIT_USERNAME = cfg_file.get('reddit', 'username')
REDDIT_PASSWORD = cfg_file.get('reddit', 'password')
REDDIT_UA = cfg_file.get('reddit', 'user_agent')

# don't change unless you want different delimiter strings for some reason
START_DELIM = '/* Network-Wide CSS - DO NOT EDIT HERE */'
END_DELIM = '/* End Network CSS - EDIT BELOW THIS LINE */'


# log into reddit
print "Logging in as /u/"+REDDIT_USERNAME+"..."
r = reddit.Reddit(user_agent=REDDIT_UA)
r.login(REDDIT_USERNAME, REDDIT_PASSWORD)
print "  Success!"


# get the source stylesheet
print "Getting source stylesheet from /r/"+CSS_SUBREDDIT+"..."
css_subreddit = r.get_subreddit(CSS_SUBREDDIT)
# fetch the stylesheet from the main subreddit
source_stylesheet = css_subreddit.get_stylesheet()['stylesheet']
# construct the regex object
replace_pattern = re.compile('%s.*?%s' % (re.escape(START_DELIM), re.escape(END_DELIM)), re.IGNORECASE|re.DOTALL|re.UNICODE)
# extract CSS from source stylesheet
source_css = re.search(replace_pattern, source_stylesheet).group(0)
print "  Success!"


# Apply CSS to network subreddits
print "Updating network subreddits' stylesheets:"
for dest_sr in NETWORK_SUBREDDITS:
    print "  /r/"+dest_sr+"..."
    
    dest_subreddit = r.get_subreddit(dest_sr)
    dest_css = dest_subreddit.get_stylesheet()['stylesheet']

#     new_css = re.sub(replace_pattern,
#                      '%s\\n\%s\\n%s' % (START_DELIM, source_css, END_DELIM),
#                      dest_css)
    new_css = re.sub(replace_pattern, source_css, dest_css)
    print new_css
    
    dest_subreddit.set_stylesheet(new_css)
    
    print "    Done!"


# update the sidebar
# current_sidebar = main_subreddit.get_settings()['description']
# current_sidebar = HTMLParser.HTMLParser().unescape(current_sidebar)
# replace_pattern = re.compile('%s.*?%s' % (re.escape(START_DELIM), re.escape(END_DELIM)), re.IGNORECASE|re.DOTALL|re.UNICODE)
# new_sidebar = re.sub(replace_pattern,
#                     '%s\\n\\n%s\\n%s' % (START_DELIM, list_text, END_DELIM),
#                     current_sidebar)
# main_subreddit.update_settings(description=new_sidebar)