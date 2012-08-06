# Network Reddit CSS maintainer

Maintains CSS across a network of subreddits by copying CSS from a source
subreddit to any number of other subreddits. CSS to be copied is delimited
by strings (can be customized) in the source and destination subreddits.
Preserves all CSS not within the delimiters on destination/network
subreddits, ignores CSS outside delimiters in source subreddit stylesheet.

# Requires:

- Python Reddit API Wrapper package, "reddit"

# To use:

1. Rename network-css.cfg.example to network-css.cfg, update it to
include correct info.

2. Edit network-css.py and change the subreddits.

3. Set up your subreddits. Put the delimiters around the CSS you want copied
in the CSS_SUBREDDIT subreddit, and put them in, empty, in the
NETWORK_SUBREDDITs. I advise you put the network CSS at the top, that way you
can use the cascading functionality of CSS to make changes on each subreddit.

4. Run the script under python2.7 every time you want to update the CSS.