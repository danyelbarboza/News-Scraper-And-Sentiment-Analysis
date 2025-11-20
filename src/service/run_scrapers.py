from datetime import datetime
from service.save_database import Database
from datetime import timedelta, datetime
from service.sentiment_analysis import SentimentAnalysis
from service.classifier_model import ClassifierModel
import time


# Coleta as notícias e salva no banco de dados
def run_scraper_db(portal_scraper, period, portal_name):
    start = time.time()
    headers_news, last_page = portal_scraper.get_news(period) # Retorna as notícias em formato de lista e o número de páginas
    resultados = []
    db = Database()
    data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sentiment_model = SentimentAnalysis()
    classifier_model = ClassifierModel()
    batch_size = 10
    
    
    for item in headers_news:
        
        # TRABALHANDO COM O G1
        if portal_name == "g1":
            if item['link']:
                full_article, news_date = portal_scraper.get_full_article(item['link'])
            else:
                full_article, news_date = None, None
            if full_article is None:
                continue
            diference = datetime.now() - news_date
            if period == ['minuto', 'minutos']:
                if diference > timedelta(hours=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas']:
                if diference > timedelta(days=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias']:
                if diference > timedelta(days=7):
                    break
            
            main_label, score_main_label, second_label, secondscore, sublabel, score_sublabel = classifier_model.classify_text(item['title'])
            sentiment_analysis, score_sentiment = SentimentAnalysis().analyze(full_article)   
            
            resultados.append({
                "title": item['title'],
                "link": item['link'],
                "scraping_date": data_coleta,
                "news_date": news_date,
                "article": full_article,
                "sentiment_analysis": sentiment_analysis,
                "score_sentiment": score_sentiment,
                "main_label": main_label,
                "score_main_label": score_main_label,
                "second_label": second_label,
                "second_score": secondscore,
                "sublabel": sublabel,
                "score_sublabel": score_sublabel,
            })
            print(f"- Coletado: {item['title']}")
            print(f"Página {item['current_page']} de {last_page}")
            
            # --- SALVAR EM LOTES ---
            if len(resultados) >= batch_size:
                print(f"\n>>> Salvando lote de {len(resultados)} notícias no banco...")
                db.insert_news(resultados, portal_name)
                resultados = []
                print(">>> Lote salvo e memória liberada.\n")
            
            
        # TRABALHANDO COM O MONEYTIMES
        elif portal_name == "moneytimes":
            if item['link']:
                full_article, news_date = portal_scraper.get_full_article(item['link'])
            else:
                full_article, news_date = None, None
            if full_article is None:
                continue
            diference = datetime.now() - news_date
            if period == ['minuto', 'minutos']:
                if diference > timedelta(hours=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas']:
                if diference > timedelta(days=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias', 'mes', 'meses']:
                if diference > timedelta(days=30):
                    break 
            
            main_label, score_main_label, second_label, secondscore, sublabel, score_sublabel = classifier_model.classify_text(item['title'])
            sentiment_analysis, score_sentiment = SentimentAnalysis().analyze(full_article)   
            
            resultados.append({
                "title": item['title'],
                "link": item['link'],
                "scraping_date": data_coleta,
                "news_date": news_date,
                "article": full_article,
                "sentiment_analysis": sentiment_analysis,
                "score_sentiment": score_sentiment,
                "main_label": main_label,
                "score_main_label": score_main_label,
                "second_label": second_label,
                "second_score": secondscore,
                "sublabel": sublabel,
                "score_sublabel": score_sublabel,
            })
            print(f"- Coletado: {item['title']}")
            print(f"Página {item['current_page']} de {last_page}")
            
            # --- SALVAR EM LOTES ---
            if len(resultados) >= batch_size:
                print(f"\n>>> Salvando lote de {len(resultados)} notícias no banco...")
                db.insert_news(resultados, portal_name)
                resultados = []
                print(">>> Lote salvo e memória liberada.\n")
            
        # TRABALHANDO COM OS OUTROS PORTAIS    
        else:
            try:
                full_article = portal_scraper.get_full_article(item['link']) if item['link'] else None
            except Exception as e:
                print("Erro ao coletar artigo:", e)
                continue

            if not isinstance(full_article, str): 
                continue

            if full_article is None:
                continue
            
            diference = datetime.now() - item['time']
            if period == 1:
                if diference > timedelta(hours=1):
                    break
            elif period == 2:
                if diference > timedelta(days=1):
                    break
            elif period == 3:
                if diference > timedelta(days=7):
                    break
            elif period == 4:
                if diference > timedelta(days=30):
                    break
            
            main_label, score_main_label, second_label, secondscore, sublabel, score_sublabel = classifier_model.classify_text(item['title'])
            sentiment_analysis, score_sentiment = SentimentAnalysis().analyze(full_article)   
            
            resultados.append({
                "title": item['title'],
                "link": item['link'],
                "scraping_date": data_coleta,
                "news_date": item['time'],
                "article": full_article,
                "sentiment_analysis": sentiment_analysis,
                "score_sentiment": score_sentiment,
                "main_label": main_label,
                "score_main_label": score_main_label,
                "second_label": second_label,
                "second_score": secondscore,
                "sublabel": sublabel,
                "score_sublabel": score_sublabel,
            })
            print(f"- Coletado: {item['title']}")
            print(f"Página {item['current_page']} de {last_page}")
            
            # --- SALVAR EM LOTES ---
            if len(resultados) >= batch_size:
                print(f"\n>>> Salvando lote de {len(resultados)} notícias no banco...")
                db.insert_news(resultados, portal_name)
                resultados = []
                print(">>> Lote salvo e memória liberada.\n")

    # --- SALVAR O RESTANTE ---
    if len(resultados) > 0:
        print(f"\n>>> Salvando as últimas {len(resultados)} notícias...")
        db.insert_news(resultados, portal_name)
    
    end = time.time()
    print(f"Tempo de execução: {end - start:.2f} segundos")

    