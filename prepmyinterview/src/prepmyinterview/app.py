import gradio as gr
import os
from main import run

def process_job_posting(job_posting):
    """Process the job posting through the crew"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Clean previous output files
        for file in os.listdir('output'):
            if file.endswith('.md'):
                os.remove(os.path.join('output', file))
        
        # Run the crew with the job posting
        result = run(job_posting)
        
        # Read and combine all output files in order
        output_files = [
            'output/00_extract.md',
            'output/01_research.md',
            'output/02_interview.md'
        ]
        
        combined_output = ""
        for file_path in output_files:
            section_name = file_path.split('/')[-1].replace('.md', '').replace('_', ' ').title()
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Add a section header
                    combined_output += f"\n\n## {section_name}\n\n"
                    # Read and add file content
                    content = f.read()
                    combined_output += content
            except FileNotFoundError:
                combined_output += f"\n\n## {section_name}\n\nProcesando... por favor espere."
            except Exception as e:
                combined_output += f"\n\nError leyendo {file_path}: {str(e)}"
        
        return combined_output
    
    except Exception as e:
        return f"Error procesando la descripción del trabajo: {str(e)}"

# Configuración del tema personalizado
custom_theme = gr.themes.Soft().set(
    body_background_fill="*background-color: #0f172a",
    body_text_color="#e2e8f0",
    button_primary_background_fill="#3b82f6",
    button_primary_text_color="#ffffff",
    button_primary_background_fill_hover="#2563eb",
    block_title_text_color="#f8fafc",
    block_label_text_color="#e2e8f0",
    input_background_fill="#1e293b",
    input_border_color="#475569",
    input_placeholder_color="#94a3b8"
)

with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("""
    # 🎯 Asistente de Preparación para Entrevistas
    
    Esta herramienta te ayudará a prepararte para tu entrevista de trabajo mediante:
    
    1. **Análisis** de la descripción del trabajo
    2. **Investigación** de la empresa y la industria
    3. **Identificación** de requisitos técnicos clave
    4. **Generación** de preguntas relevantes para la entrevista
    5. **Preparación** de ejemplos de respuestas
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(
                label="Descripción del Trabajo",
                placeholder="Pega aquí la descripción completa del trabajo...",
                info="Incluye todos los detalles sobre la posición.",
                lines=15
            )
            submit_btn = gr.Button(
                "📝 Analizar Propuesta", 
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=1):
            output_text = gr.Markdown(
                value="### Los resultados aparecerán aquí...",
                label="Resultados del Análisis"
            )
    
    with gr.Row():
        gr.Markdown("""
        ### 💡 Tips:
        - Asegúrate de incluir la descripción completa del trabajo
        - Incluye información sobre requisitos y responsabilidades
        - Los resultados se mostrarán en formato estructurado
        """)
    
    submit_btn.click(
        fn=process_job_posting,
        inputs=input_text,
        outputs=output_text,
        api_name="analyze"
    )

if __name__ == "__main__":
    demo.launch(
        share=True,
        debug=True
    ) 