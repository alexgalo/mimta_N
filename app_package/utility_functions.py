import codecs
import unicodedata
import re
from nltk.stem import SnowballStemmer

def represents_int(s):
    try:
        int(s)
        return True
    except:
        return False

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', str(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def replace_symbols(s, list_symbs, replace_by):
    for c in list_symbs:
        s = s.replace(c, replace_by)
    return s


def replace_symbols_alone(s, list_symbs, replace_by):
	for c in list_symbs:
		cad = r"(\s)"+re.escape(c)+r"(\s)"
		temp = re.compile(cad)
		s = temp.sub(r"\1"+replace_by+r"\2", s)
	return s

def writefile(fn, st):
	f = codecs.open(fn, "w", "utf-8")
	f.write(st)
	f.close()

def writefile2(fn, st):
	f = open(fn, "w")
	print >> f, st.encode("utf8",'ignore')
	f.close()

def replace_numbers(s, replace_by):
	re.purge()
	temp = re.compile(r'([0-9]+(st|th|rd|nd|,[0-9]+|.[0-9]+)?)', re.UNICODE)
	s = temp.sub(replace_by, s)
	return s

def remove_numbers(s):
    r = ''.join([i for i in s if not i.isdigit()])
    return r

def remove_links(s, replace_by):
	#quita url www.algo.com/djj
    re.purge()
    temp = re.compile(r"\s*www\.\. \w+\.(com|net|me|org)?(\s|/*[-\w+&@#/%!?=~_:.\[\]()0-9]*)")
    s = temp.sub(replace_by, s)
    #quita http://
    temp = re.compile(r"(((http|ftp|https)://\. |(http|ftp|https)://\.)[-/\w.]*)")
    s = temp.sub(replace_by, s)
    temp = re.compile(r"\w+/\w")
    s = temp.sub(replace_by, s)
    return s

def replace_usernames(s, replace_by):
	temp = re.compile(r"@[A-Za-z0-9_-]*")
	s = temp.sub(replace_by, s)
	return s

def remove_spaces(s, replace_by):
	s = re.sub("\s+" , replace_by, s)
	return s

def remove_returns(s, replace_by):
	'''EOL: End of Line'''
	re.purge()
	temp = re.compile(r"\s+")
	s = temp.sub(replace_by, s)
	return s

def replace_hashtags(s, replace_by):
	s = re.sub(r'#[A-Za-z0-9_-]*', replace_by, s)
	return s

def onlywords(s, replace_by):
	temp = re.compile(r"[^.\w<> ]")
	s = temp.sub(replace_by, s)
	s = remove_spaces(s, " ")
	return s


#def stemmingSpanish(s):
#	return " ".join(stemmer.stem(word) for word in s.split(" "))

def merge(d1, d2, merge_fn=lambda x,y:y):
    """
	source: http://stackoverflow.com/a/44512
    Merges two dictionaries, non-destructively, combining
    values on duplicate keys as defined by the optional merge
    function.  The default behavior replaces the values in d1
    with corresponding values in d2.  (There is no other generally
    applicable merge strategy, but often you'll have homogeneous
    types in your dicts, so specifying a merge technique can be
    valuable.)

    Examples:

    >>> d1
    {'a': 1, 'c': 3, 'b': 2}
    >>> merge(d1, d1)
    {'a': 1, 'c': 3, 'b': 2}
    >>> merge(d1, d1, lambda x,y: x+y)
    {'a': 2, 'c': 6, 'b': 4}

    """
    result = dict(d1)
    for k,v in d2.iteritems():
        if k in result:
            result[k] = merge_fn(result[k], v)
        else:
            result[k] = v
    return result
