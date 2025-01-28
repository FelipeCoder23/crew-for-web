from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, task, crew
from crewai.process import Process
from textwrap import dedent
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Verificar API key
if not os.getenv("OPENAI_API_KEY"):
	raise ValueError("Por favor configura OPENAI_API_KEY en el archivo .env")

@CrewBase
class Prepmyinterview:
	def __init__(self):
		self.agents_config = self._load_config('agents.yaml')
		self.tasks_config = self._load_config('tasks.yaml')
		# Crear directorio output si no existe
		os.makedirs('output', exist_ok=True)

	def _load_config(self, filename):
		import yaml
		import os
		config_path = os.path.join(os.path.dirname(__file__), 'config', filename)
		with open(config_path, 'r', encoding='utf-8') as f:
			return yaml.safe_load(f)

	@agent
	def extractor(self):
		return Agent(
			role=self.agents_config['extractor']['role'],
			goal=self.agents_config['extractor']['goal'],
			backstory=self.agents_config['extractor']['backstory'],
			allow_delegation=False,
			verbose=True
		)

	@agent
	def researcher(self):
		return Agent(
			role=self.agents_config['researcher']['role'],
			goal=self.agents_config['researcher']['goal'],
			backstory=self.agents_config['researcher']['backstory'],
			allow_delegation=False,
			verbose=True
		)

	@agent
	def hr_specialist(self):
		return Agent(
			role=self.agents_config['hr_specialist']['role'],
			goal=self.agents_config['hr_specialist']['goal'],
			backstory=self.agents_config['hr_specialist']['backstory'],
			allow_delegation=False,
			verbose=True
		)

	@agent
	def interviewer(self):
		return Agent(
			role=self.agents_config['interviewer']['role'],
			goal=self.agents_config['interviewer']['goal'],
			backstory=self.agents_config['interviewer']['backstory'],
			allow_delegation=False,
			verbose=True
		)

	@task
	def extract_task(self):
		return Task(
			description=self.tasks_config['extract_task']['description'],
			expected_output=self.tasks_config['extract_task']['expected_output'],
			agent=self.extractor(),
			output_file='output/00_extract.md'
		)

	@task
	def research_task(self):
		extract_output = self.extract_task()
		return Task(
			description=self.tasks_config['research_task']['description'],
			expected_output=self.tasks_config['research_task']['expected_output'],
			agent=self.researcher(),
			context=[extract_output],
			output_file='output/01_research.md'
		)

	@task
	def hr_task(self):
		extract_output = self.extract_task()
		return Task(
			description=self.tasks_config['hr_task']['description'],
			expected_output=self.tasks_config['hr_task']['expected_output'],
			agent=self.hr_specialist(),
			context=[extract_output],
			output_file='output/02_hr.md'
		)

	@task
	def interview_task(self):
		extract_output = self.extract_task()
		research_output = self.research_task()
		hr_output = self.hr_task()
		return Task(
			description=self.tasks_config['interview_task']['description'],
			expected_output=self.tasks_config['interview_task']['expected_output'],
			agent=self.interviewer(),
			context=[extract_output, research_output, hr_output],
			output_file='output/03_interview.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Crea la tripulación con la secuencia de tareas para la preparación de entrevistas"""
		return Crew(
			agents=self.agents,  # Agentes creados automáticamente por el decorador @agent
			tasks=self.tasks,    # Tareas creadas automáticamente por el decorador @task
			process=Process.sequential,
			verbose=True
		)
