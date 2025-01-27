from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, task
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
		return Task(
			description=self.tasks_config['research_task']['description'],
			expected_output=self.tasks_config['research_task']['expected_output'],
			agent=self.researcher(),
			output_file='output/01_research.md'
		)

	@task
	def interview_task(self):
		return Task(
			description=self.tasks_config['interview_task']['description'],
			expected_output=self.tasks_config['interview_task']['expected_output'],
			agent=self.interviewer(),
			output_file='output/02_interview.md'
		)

	def crew(self):
		crew = Crew(
			agents=[
				self.extractor(),
				self.researcher(),
				self.interviewer()
			],
			tasks=[
				self.extract_task(),
				self.research_task(),
				self.interview_task()
			],
			verbose=True
		)
		return crew
