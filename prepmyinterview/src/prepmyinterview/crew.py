from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import WebsiteSearchTool
from dotenv import load_dotenv
import os

# Configure environment
load_dotenv()

@CrewBase
class Prepmyinterview():
	"""Prepmyinterview crew for IT job interview preparation"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self):
		# Create output directory if it doesn't exist
		os.makedirs('output', exist_ok=True)
		
		# Clean output files at start
		for file in os.listdir('output'):
			if file.endswith('.md'):
				os.remove(os.path.join('output', file))

	@agent
	def job_parser(self) -> Agent:
		return Agent(
			config=self.agents_config['job_parser'],
			llm_model="gpt-4",
			verbose=True
		)

	@agent
	def company_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['company_researcher'],
			tools=[WebsiteSearchTool()],
			llm_model="gpt-4",
			verbose=True
		)

	@agent
	def job_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['job_analyzer'],
			llm_model="gpt-4",
			verbose=True
		)

	@agent
	def interview_question_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['interview_question_generator'],
			llm_model="gpt-4",
			verbose=True
		)

	@agent
	def answer_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['answer_generator'],
			llm_model="gpt-4",
			verbose=True
		)

	@task
	def company_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['company_research_task']
		)

	@task
	def job_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['job_analysis_task']
		)

	@task
	def question_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['question_generation_task']
		)

	@task
	def answer_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['answer_generation_task']
		)

	@task
	def job_parsing_task(self) -> Task:
		return Task(
			config=self.tasks_config['job_parsing_task']
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True
		)
