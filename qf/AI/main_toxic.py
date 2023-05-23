

def test_nlp(sentence):
    from transformers import pipeline
    nlp = pipeline("sentiment-analysis", model='akhooli/xlm-r-large-arabic-toxic')
    nlp.return_all_scores = True
    
    test = nlp(sentence)
    test_main_label = test[0]['label']
    test_main_score = test[0]['score']
    
    if test_main_label == 'LABEL_0':
        label = 'non-toxic'
    elif test_main_label == 'LABEL_1':
        label = 'toxic'
    else:
        label = 'undefined'

    return test_main_score
