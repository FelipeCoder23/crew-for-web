#!/usr/bin/env python
from crew import Prepmyinterview

def run(job_description):
    """
    Run the crew with a job description.
    Args:
        job_description (str): The complete job posting text
    Returns:
        dict: Results from the crew execution
    """
    inputs = {
        'job_description': job_description
    }
    return Prepmyinterview().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    # Test run with example input
    test_description = """
    [Aquí va una descripción de trabajo de ejemplo para pruebas]
    """
    run(test_description)
