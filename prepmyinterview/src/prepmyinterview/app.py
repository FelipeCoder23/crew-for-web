import gradio as gr
from crew import Prepmyinterview

def process_job_posting(job_posting):
    """Process the job posting through the crew"""
    try:
        # Initialize and run the crew with the raw job posting
        crew = Prepmyinterview()
        crew.crew().kickoff(inputs={'job_description': job_posting})
        
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
        placeholder="Paste the complete job posting here...",
        label="Job Posting"
    ),
    outputs=gr.Textbox(
        lines=20,
        label="Interview Preparation Results"
    ),
    title="Interview Preparation Assistant",
    description="Paste a job posting and get a complete interview preparation guide."
)

if __name__ == "__main__":
    iface.launch(share=True) 