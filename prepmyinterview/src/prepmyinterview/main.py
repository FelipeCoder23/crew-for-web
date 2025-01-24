#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
import time
from crew import Prepmyinterview

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def extract_job_info(job_description: str) -> dict:
    """
    Extract company name and job title from the job description.
    For now, this is a simple implementation that could be enhanced later.
    """
    # This is a placeholder - in a real implementation, you'd want to use
    # more sophisticated parsing
    lines = job_description.split('\n')
    company_name = next((line for line in lines if 'Isapre Consalud' in line), 'Unknown Company')
    job_title = next((line for line in lines if 'Data Scientist' in line), 'Unknown Position')
    
    return {
        'company_name': company_name.strip(),
        'job_title': job_title.strip(),
        'job_description': job_description,
        'current_year': str(datetime.now().year)
    }

def run_with_retry(max_retries=3, delay=2):
    """
    Run the crew with retries in case of temporary failures.
    """
    sample_job = """
    Isapre Consalud
    Data Scientist 
    Las Condes, Región Metropolitana de Santiago, Chile

    Trabajamos para brindar tranquilidad y seguridad en el acceso a la salud a más de 500 mil personas cada día.

    Para lograrlo contamos con el respaldo de la Cámara Chilena de la Construcción y un gran equipo de personas comprometidas con el bienestar de Chile. Tenemos la convicción de que es posible acceder a una experiencia de salud y bienestar superior que se articula de manera integral en torno a las necesidades.

    Nuestra área de Analytics está en búsqueda de un profesional para el cargo de Data Scientist, donde su principal desafío será explotar diversas fuentes de datos, haciendo uso técnicas estadísticas avanzadas para la generación de valor y retroalimentación de insights a las distintas áreas de negocio.

    Entre sus principales funciones se encuentran:
    - Encontrar soluciones innovadoras en equipo, ser clave en generar Insights independientes que impulsen la toma de decisiones.
    - Detectar oportunidades de incorporar nuevas tecnologías, herramientas y soluciones de Analytics.
    - Garantizar que Consalud haga uso de todas las instancias de recuperar información que ayude a la gestión y análisis sobre los clientes, servicios, mercado e industria.

    Entre los principales requisitos se encuentran:
    - Título Universitario: Ingeniería en Estadística, Ingeniería Informática, Ingeniería Matemática, Ingeniería Civil Industrial o a fin.
    - Desde 1 año de experiencia laboral en Modelos Predictivos, Machine Learning, Programación Python / SQL
    - Deseable: AWS / GitHub / Tableau / Docker

    En Consalud promovemos el valor de ser tú mismo, por lo que impulsamos la inclusión laboral y diversidad bajo la Ley 21.015. Nos enfocamos en el equilibrio de tu vida personal y laboral, por lo que trabajamos 40 horas semanales.
    """
    
    for attempt in range(max_retries):
        try:
            inputs = extract_job_info(sample_job)
            result = Prepmyinterview().crew().kickoff(inputs=inputs)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed after {max_retries} attempts. Last error: {e}")
            print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
            time.sleep(delay)

def run():
    """
    Run the interview preparation crew.
    """
    try:
        run_with_retry()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Prepmyinterview().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Prepmyinterview().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Prepmyinterview().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
