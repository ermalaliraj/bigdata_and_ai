FROM python:3.7-slim-buster

COPY . /root
WORKDIR /root

RUN pip install -r requirements.txt
RUN python -c "import nltk;nltk.download('punkt');nltk.download('brown');nltk.download('gutenberg');nltk.download('stopwords');nltk.download('averaged_perceptron_tagger')"  
# python -m nltk.downloader -d /usr/local/share/nltk_data all

CMD python nlp_nltk.py