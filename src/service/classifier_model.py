from transformers import pipeline

class ClassifierModel:
    # Inicializa o classificador
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0
    )

    # Labels principais
    candidate_labels = [
        "politics", "economy", "technology", "science", "health",
        "education", "environment", "crime", "entertainment",
        "sports", "culture", "other", "curiosities", "lifestyle"
    ]

    # Mapeamento de sublabels
    sublabels_map = {
        "politics": ["elections", "legislation", "government", "diplomacy", "policy"],
        "economy": ["markets", "trade", "finance", "jobs", "inflation"],
        "technology": ["artificial_intelligence", "gadgets", "software", "hardware", "internet", "tech_finance"],
        "science": ["biology", "physics", "chemistry", "space", "research"],
        "health": ["diseases", "nutrition", "mental_health", "fitness", "medicine"],
        "education": ["schools", "universities", "online_learning", "research", "policy"],
        "environment": ["climate", "pollution", "conservation", "wildlife", "renewables"],
        "crime": ["theft", "fraud", "homicide", "drugs", "corruption"],
        "entertainment": ["movies", "tv", "music", "theater", "celebrities"],
        "sports": ["football", "basketball", "tennis", "olympics", "athletes"],
        "culture": ["art", "literature", "traditions", "festivals", "history"],
        "other": ["miscellaneous", "trends", "opinion", "events", "trends"],
        "curiosities": ["weird_news", "facts", "history_bits", "records", "oddities"],
        "lifestyle": ["health_wellness", "fashion_beauty", "travel_leisure", "food_drink", "home_living"]
    }

    def classify_label(self, text, labels=candidate_labels):
        """Classifica o texto nas labels principais e retorna a primeira com score."""
        result = self.classifier(text, candidate_labels=labels)
        label = result['labels'][0]
        second_label = result['labels'][1]
        secondscore = result['scores'][1]
        score = result['scores'][0]
        score_rounded = round(score, 2)
        return label, score_rounded, second_label, secondscore


    def classify_sublabel(self, text, main_label, second_label):
        """Classifica o texto nas sublabels da label principal."""
        main_sublabels = self.sublabels_map.get(main_label, [])
        second_sublabels = self.sublabels_map.get(second_label, [])
        if not main_sublabels or not second_sublabels:
            return None, None
        main_sublabels.extend(second_sublabels)
        result = self.classifier(text, candidate_labels=main_sublabels)
        score_rounded = round(result['scores'][0], 2)
        return result['labels'][0], score_rounded
    
    def classify_text(self, text):
        """Classifica o texto nas labels principais e sublabels."""
        main_label, score_main_label, second_label, secondscore = self.classify_label(text)
        sublabel, score_sublabel = self.classify_sublabel(text, main_label, second_label)
        return main_label, score_main_label, second_label, secondscore, sublabel, score_sublabel


""""
    def classify_news(self, news_list):
        news_categorized_list = []
        for news in news_list:
            label_principal, score_principal = self.classify_text(news['title'])
            sublabel, score_sublabel = self.classify_sublabel(news['title'], label_principal)
            news_categorized_list.append({
                "title": news['title'],
                "link": news['link'],
                "scraping_date": news['scraping_date'],
                "news_date": news['news_date'],
                "article": news['article'],
                "sentiment_analysis": news['sentiment_analysis'],
                "confidence_score": news['confidence_score'],
                "main_label": label_principal,
                "score_main_label": score_principal,
                "sublabel": sublabel,
                "score_sublabel": score_sublabel
            })
        return news_categorized_list
    """