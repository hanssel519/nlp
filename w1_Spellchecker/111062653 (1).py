#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
from collections import Counter
from pprint import pprint
import string 


# In[2]:


def words(text): return re.findall(r'\w+', text.lower())


# In[3]:


word_count = Counter(words(open('big.txt').read()))


# In[4]:


N = sum(word_count.values())


# In[5]:


def P(word): return word_count[word] / N # float


# In[6]:


print( list(map (lambda x: (x, P(x)), words('speling spelling speeling'))) )


# In[7]:


letters    = 'abcdefghijklmnopqrstuvwxyz'


# In[8]:


def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word)+1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


# In[9]:


pprint( list(edits1('speling'))[:3])


# In[10]:


#pprint( list(map(lambda x: (x, P(x)), edits1('speling'))))


# In[11]:


print( list(filter(lambda x: P(x) != 0.0, edits1('speling'))) )


# In[12]:


print( max(edits1('speling'), key=P))


# In[13]:


def correction(word): 
    for i in word:
        if i in string.punctuation:
            return word
    return max(candidates(word), key=P)


# In[14]:


def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


# In[15]:


def known(words): 
    #print('in known')
    #print(set(w for w in words if w[0] in word_count))
    #print('end of known')
    
    return set(w for w in words if w in word_count)


# In[16]:


def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# In[17]:


print('speling -->', correction('speling'))


# In[18]:


import sys
sys.path


# In[19]:


len(word_count)


# In[20]:


sum(word_count.values())


# In[21]:


P('quintessential')


# In[22]:


word_count.most_common(10)


# In[23]:


P('the')


# In[24]:


def unit_tests():
    assert correction('speling') == 'spelling'              # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('bycycle') == 'bicycle'               # replace
    assert correction('inconvient') == 'inconvenient'       # insert 2
    assert correction('arrainged') == 'arranged'            # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    #assert len(word_count) == 32192, 'len(word_count)'
    #assert sum(word_count.values()) == 1115504
    assert word_count.most_common(10) == [
     ('the', 79808),
     ('of', 40024),
     ('and', 38311),
     ('to', 28765),
     ('in', 22020),
     ('a', 21124),
     ('that', 12512),
     ('he', 12401),
     ('was', 11410),
     ('it', 10681)]
    assert word_count['the'] == 79808
    assert P('quintessential') == 0
    assert 0.07 < P('the') < 0.08
    return 'unit_tests pass'


# In[25]:


def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]


# In[26]:


def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.perf_counter()

    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in word_count)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, word_count[w], right, word_count[right]))
    dt = time.perf_counter() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))


# In[27]:


#print(unit_tests())
#spelltest(Testset(open('dev_set.txt')))


# In[28]:


# spelltest(Testset(open('development_set.txt'))) # Development set
spelltest(Testset(open('spell-testset1.txt'))) # Development set
spelltest(Testset(open('spell-testset2.txt'))) # Final test set


# In[ ]:




