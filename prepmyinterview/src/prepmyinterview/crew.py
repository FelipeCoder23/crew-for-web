from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SeleniumScrapingTool
from dotenv import load_dotenv
import os

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()
os.environ['OPENAI_API_BASE'] = 'https://api.openai.com/v1'

@CrewBase
class Prepmyinterview():
	"""Prepmyinterview crew for IT job interview preparation"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def company_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['company_researcher'],
			tools=[SeleniumScrapingTool(
				headless=True,  # Run in headless mode
				timeout=30,     # Increase timeout
				ignore_ssl_errors=True  # Ignore SSL errors
			)],
			verbose=True
		)

	@agent
	def job_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['job_analyzer'],
			verbose=True
		)

	@agent
	def interview_question_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['interview_question_generator'],
			verbose=True
		)

	@agent
	def answer_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['answer_generator'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
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

	@crew
	def crew(self) -> Crew:
		"""Creates the interview preparation crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
