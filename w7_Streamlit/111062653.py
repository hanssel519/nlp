import re
from collections import Counter
from typing import final
import streamlit as st

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


#####
def verify(w):
    if w != correction(w):
        st.markdown(f'<p style="background-color:#FF0000;font-size:24px;border-radius:2%;">{correction(w)}</p>', unsafe_allow_html=True)
    elif w == correction(w):
        st.markdown(f'<p style="background-color:#3CB371;font-size:24px;border-radius:2%;">{correction(w)}</p>', unsafe_allow_html=True)


select_word = st.selectbox('choose a word or ...', ['','apple', 'lamon', 'speling', 'hapy', 'language', 'greay'])
text_input = st.text_input('type your own!!!')


check_shown = st.sidebar.checkbox('Show the original word')

if check_shown:
    if select_word:
        st.text('Original word: ')
        st.text(select_word)
    elif text_input:
        st.text('Original word: ')
        st.text(text_input)




if text_input:
    #w = selected_word
    verify(text_input)
elif select_word:
    verify(select_word)

