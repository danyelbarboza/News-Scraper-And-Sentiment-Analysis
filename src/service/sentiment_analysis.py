from transformers import pipeline
import re
from service.sentiment_model import sentiment_pipeline

class SentimentAnalysis():
    @staticmethod
    def analyze(article):
        caracteres = 150
        analysis = []
        
        if not isinstance(article, str) or len(article.strip()) == 0:
            print("Artigo inválido ou None ->", article)
            return None, None

        # tentar criar o texto com try/except
        try:
            text = article[:caracteres].ljust(caracteres)
            text = re.sub(r'["\']', '', text)
        except Exception as e:
            print("Erro ao preparar texto:", e)
            return None, None

        resultado = sentiment_pipeline(text)
        label = resultado[0]['label']
        score = resultado[0]['score']
        rounded_score = round(score, 2)
        return label, rounded_score