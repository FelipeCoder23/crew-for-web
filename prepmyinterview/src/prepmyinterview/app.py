import gradio as gr
from crew import Prepmyinterview
import re

def extract_job_info(job_posting):
    """Extract job title and company name from the job posting"""
    # Try to find company name and job title
    company_match = re.search(r'Logotipo de (.*?)\n', job_posting)
    title_match = re.search(r'\n(.*?)\n.*?·', job_posting)
    
    company_name = company_match.group(1) if company_match else "Unknown Company"
    job_title = title_match.group(1).strip() if title_match else "Unknown Position"
    
    return company_name, job_title, job_posting

def process_job_posting(job_posting):
    """Process the job posting through the crew"""
    try:
        # Extract information
        company_name, job_title, job_description = extract_job_info(job_posting)
        
        # Initialize and run the crew
        inputs = {
            'company_name': company_name,
            'job_title': job_title,
            'job_description': job_description
        }
        
        crew = Prepmyinterview()
        crew.crew().kickoff(inputs=inputs)
        
        # Read and combine all output files
        output_files = [
            'output/01_company_analysis.md',
            'output/02_job_analysis.md',
            'output/03_interview_questions.md',
            'output/04_interview_answers.md'
        ]
        
        combined_output = ""
        for file_path in output_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_output += f"\n\n# {file_path.split('/')[-1].replace('.md', '').replace('_', ' ').title()}\n\n"
                    combined_output += f.read()
            except Exception as e:
                combined_output += f"\nError reading {file_path}: {str(e)}\n"
        
        return combined_output
    
    except Exception as e:
        return f"Error processing job posting: {str(e)}"

# Create the Gradio interface
iface = gr.Interface(
    fn=process_job_posting,
    inputs=gr.Textbox(
        lines=10,
        placeholder="Paste the complete job posting from LinkedIn here...",
        label="Job Posting"
    ),
    outputs=gr.Textbox(
        lines=20,
        label="Interview Preparation Results"
    ),
    title="Interview Preparation Assistant",
    description="Paste a job posting from LinkedIn and get a complete interview preparation guide.",
    examples=[
        ["""Logotipo de Scotiabank
Scotiabank
Analista Inteligencia de Negocios 
Área metropolitana de Santiago · hace 3 semanas..."""]
    ]
)

if __name__ == "__main__":
    iface.launch(share=True) 