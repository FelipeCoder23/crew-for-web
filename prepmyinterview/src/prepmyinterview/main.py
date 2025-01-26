#!/usr/bin/env python
import sys
from crew import Prepmyinterview

def run():
    """
    Run the crew.
    """
    inputs = {
        'job_description': """
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
    }
    Prepmyinterview().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'company_name': 'Isapre Consalud',
        'job_title': 'Data Scientist'
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
        'company_name': 'Isapre Consalud',
        'job_title': 'Data Scientist'
    }
    try:
        Prepmyinterview().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
