

def test_nlp_positive(sentence):
    from transformers import pipeline 

    nlp = pipeline("sentiment-analysis", model='akhooli/xlm-r-large-arabic-sent')
    nlp.return_all_scores = True
    
    test = nlp(sentence)
    test_main_label = test[0]['label']
    test_main_score = test[0]['score']

    if test_main_label == 'LABEL_0':
        label = 'mixed'
    elif test_main_label == 'LABEL_1':
        label = 'negative'
    elif test_main_label == 'LABEL_2':
        label = 'positive'
    else:
        label = 'undefined'

    return test_main_score, label
