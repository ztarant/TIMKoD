import string
import math

def count_subarray(subarr, arr): 
    count=0

    j=0
    i=0
    #print("len", len(subarr), len(arr))
    #for i in range(len(arr)):
    while i<len(arr):
        #print(i,j)
        if arr[i]==subarr[j]:
            j+=1
            if j==len(subarr):
                count+=1
                j=0
        #elif arr[i]==subarr[0]:
            #j=1
        else:
            i=i-j
            j=0
        i+=1
    return count

def count_array(text,n):
    counts = dict()
    
    text_size=len(text)
    for i in range(n,text_size+1):
        ngram=text[i-n:i]
        ngram=tuple(ngram)
        

    '''for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1'''

    return counts


#entropia
#print((-1)*math.log((1/37), 2))
    
ngrams1={}
ngrams2={}
ngrams3={}
ngrams4={}
ngrams5={}

def get_ngram_probabilities_words(text, n): 
    words=text.split(' ')
    dic={}
    dic2={}
    count_all=0
    text_size=len(words)+1
    #print(words[0:5])
    
    for i in range(n, text_size):
        ngram_arr=words[i-n:i]
        #print(ngram_arr)
        ngram=tuple(ngram_arr)
        if dic.get(ngram) == None:
            #c = count_subarray(ngram_arr, words)
            
            dic[ngram]=1
            count_all+=1
            #print(dic[ngram])
        else:
            dic[ngram]+=1
            count_all+=1
    
    for key, value in dic.items():
        dic2[key]=value/count_all
    #print(dic2)
    return dic2

def frequency(text):
    dic={}
    probability=[]
    alphabet=[]
    signs='0123456789 '+string.ascii_lowercase
    l=len(text)
    for i in signs: 
        dic[i]= text.count(i)/l
        probability.append(dic[i])
        alphabet.append(i)
    return probability, alphabet

def probability_word(text):
    dic={}
    probability=[]
    words=[]
    text=text.split(' ')
    length=len(text)
    for word in text:
        if word != '' and dic.get(word) == None :
            dic[word]= text.count(word)/length
            probability.append(dic[word])
            words.append(word)
    return probability, words


def get_ngram_probabilities_chars(text, n): #znajduje wszystkie bigramy
    dic={}
    dic2={}
    count_all=0
    for i in range(n, len(text)+1):
        ngram=text[i-n:i]
        if dic.get(ngram) == None:
            dic[ngram]=text.count(ngram)
            count_all+=dic[ngram]
    for key, value in dic.items():
        dic2[key]=value/count_all
    return dic2


def get_probabilities_chars(ngrams, begins_with):  
    letters=[]                              
    probabilities=[]
    count_all=0
    for key, value in ngrams.items():
        if key[:-1] == begins_with and value > 0:
            letters.append(key[-1])
            probabilities.append(value)
            count_all+=value
    for i in range(len(probabilities)):
        probabilities[i]=probabilities[i]/count_all
    return letters, probabilities


def get_probabilities_words(ngrams, begins_with):  
    words=[]                              
    probabilities=[]
    count_all=0
    begins_with=tuple(begins_with)
    for key, value in ngrams.items():
        if key[:-1] == begins_with and value > 0:
            words.append(key[-1])
            probabilities.append(value)
            count_all+=value
    for i in range(len(probabilities)):
        probabilities[i]=probabilities[i]/count_all
    return words, probabilities



def entropy_chars(text):
    probability, alphabet = frequency(text)
    H=0
    for p in probability:
        if p>0:
            H-=p*(math.log(p, 2))
    return H

def entropy_words(text):
    probability, words = probability_word(text)
    H=0
    for p in probability:
        H-=(p*math.log(p, 2))
    return H

def cond_entropy_chars(text, n):
    ngrams_n1 = get_ngram_probabilities_chars(text, n+1)
    ngrams_n = get_ngram_probabilities_chars(text, n)

    H=0

    for ngram, prob in ngrams_n.items():
        letters, probabilities = get_probabilities_chars(ngrams_n1, ngram)
        for letter, probability in zip(letters, probabilities):
            new_ngram = ngram+letter
            p1 = ngrams_n1.get(new_ngram)
            H-=p1*math.log(probability, 2)
    return H

def cond_entropy_words(text, n,ngrams_n, ngrams_n1):
    #ngrams_n1 = get_ngram_probabilities_words(text, n+1)
    #ngrams_n = get_ngram_probabilities_words(text, n)

    H=0

    for ngram, prob in ngrams_n.items():
        words, probabilities = get_probabilities_words(ngrams_n1, ngram)
        for word, probability in zip(words, probabilities):
            lista=list(ngram)
            lista.append(word)
            new_ngram = tuple(lista)
            p1 = ngrams_n1.get(new_ngram)
            H-=p1*math.log(probability, 2)
    return H





input=open("data/norm_wiki_eo.txt", 'r')
#input=open("test.txt", 'r')
output=open("result.txt", 'w')
text1=input.read()[:200000]
#text1=input.read()

result = entropy_chars(text1)
print(result)
output.write("norm_wiki_en.txt\nEntropia znaków:")
output.write(str(result))

result = entropy_words(text1)
print(result)
output.write("\nEntropia słów:")
output.write(str(result))


for i in range(1,5):
    result = cond_entropy_chars(text1, i)
    print(result)
    pom="\nEntropia warunkowa znaków "+str(i)+" rzędu:"
    output.write(pom)
    output.write(str(result))
    """
    result = cond_entropy_chars(text1, 2)
    print(result)
    output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 2 rzędu:")
    output.write(str(result))
    result = cond_entropy_chars(text1, 3)
    print(result)
    output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 3 rzędu:")
    output.write(str(result))
    result = cond_entropy_chars(text1,4)
    print(result)
    output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 4 rzędu:")
    output.write(str(result))
    result = cond_entropy_chars(text1,5)
    print(result)
    output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 5 rzędu:")
    output.write(str(result))
    """

ngrams1=get_ngram_probabilities_words(text1, 1)
ngrams2=get_ngram_probabilities_words(text1, 2)
ngrams3=get_ngram_probabilities_words(text1, 3)
ngrams4=get_ngram_probabilities_words(text1, 4)
ngrams4=get_ngram_probabilities_words(text1, 5)


result = cond_entropy_words(text1,1, ngrams1, ngrams2)
print(result)
pom="\nEntropia warunkowa słów 1 rzędu:"
output.write(pom)
output.write(str(result))

result = cond_entropy_words(text1,2, ngrams2, ngrams3)
print(result)
pom="\nEntropia warunkowa słów 2 rzędu:"
output.write(pom)
output.write(str(result))

result = cond_entropy_words(text1,3, ngrams3, ngrams4)
print(result)
pom="\nEntropia warunkowa słów 3 rzędu:"
output.write(pom)
output.write(str(result))

result = cond_entropy_words(text1,4, ngrams4, ngrams5)
print(result)
pom="\nEntropia warunkowa słów 4 rzędu:"
output.write(pom)
output.write(str(result))


output.close()