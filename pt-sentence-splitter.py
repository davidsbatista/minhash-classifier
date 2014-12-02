import nltk
sent_tokenizer=nltk.data.load('tokenizers/punkt/portuguese.pickle')
f_txt = open('/home/dsbatista/Desktop/text.txt')
sentences = sent_tokenizer.tokenize(f_txt.read())
f_txt.close()
print sentences
