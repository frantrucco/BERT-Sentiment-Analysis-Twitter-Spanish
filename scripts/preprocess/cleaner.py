import re
from stop_words import get_stop_words


# URL pattern due to John Gruber, modified by Tom Winzig. See
# https://gist.github.com/winzig/8894715
# FRANCOLQ: also modified by me to remove naked URLs
URLS = r"""			# Capture 1: entire matched URL
  (?:
  https?:				# URL protocol and colon
    (?:
      /{1,3}				# 1-3 slashes
      |					#   or
      [a-z0-9%]				# Single letter or digit or '%'
                                        # (Trying not to match e.g. "URI::Escape")
    )
    |					#   or
                                        # looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:[a-z]{2,13})
    /
  )
  (?:					# One or more:
    [^\s()<>{}\[\]]+			# Run of non-space, non-()<>{}[]
    |					# or
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (...(...)...)
    |
    \([^\s]+?\)				# balanced parens, non-recursive: (...)
  )+
  (?:					# End with:
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (...(...)...)
    |
    \([^\s]+?\)				# balanced parens, non-recursive: (...)
    |					#   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]	# not a space or one of these punct chars
  )
"""

# Remaining word types:
# FRANCOLQ: fixed ellipsis dots to avoid spaces in-between.
ELSE = r"""
    (?:[^\W\d_](?:[^\W\d_]|['\-_])+[^\W\d_]) # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    # (?:\.(?:\s*\.){1,})            # Ellipsis dots.
    (?:\.{2,})
    |
    (?:\S)                         # Everything else that isn't whitespace.
"""

url = re.compile(r'https?://[\w./\-?=&+]+')

# one or more user mentions
mentions = re.compile(r'((?<=\W)|^)(@\w+)(\s*@\w+)*')

email = re.compile(r'[\w.+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+')
# (based on http://emailregex.com/)

numbers = re.compile(r'[0-9]+')

emoji_pattern = re.compile("["
                           "\U0001F600-\U0001F64F"  # emoticons
                           "\U0001F300-\U0001F5FF"  # symbols & pictographs
                           "\U0001F680-\U0001F6FF"  # transport & map symbols
                           "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{3,}")
    return pattern.sub(r"\1\1\1", text)


def remove_punctuation(text):
    punctuation = '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~'
    spaces = ' ' * len(punctuation)
    return text.translate(str.maketrans(punctuation, spaces))

def remove_stopwords(text):
    stopwords = get_stop_words('es') 
    return " ".join([word for word in text.split() if word not in stopwords])


def clean(text):
    text = text.lower()
    text = url.sub('URL', text)
    text = mentions.sub('USER', text)
    text = email.sub('MAIL', text)
    text = emoji_pattern.sub(r'', text)
    text = numbers.sub(r'', text)
    text = remove_punctuation(text)
    text = reduce_lengthening(text)
    text = remove_stopwords(text)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text
