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
            'output/02_hr.md',
            'output/03_interview.md'
        ]
        
        # Emojis para cada sección
        section_emojis = {
            '00_extract': '📋',
            '01_research': '💻',
            '02_hr': '🤝',
            '03_interview': '✨'
        }
        
        # Nombres y descripciones de las secciones
        section_info = {
            '00_extract': {
                'title': 'Análisis del Puesto',
                'description': 'Desglose detallado de los requisitos y responsabilidades del puesto.'
            },
            '01_research': {
                'title': 'Preguntas Técnicas',
                'description': 'Preguntas específicas para evaluar conocimientos y experiencia técnica.'
            },
            '02_hr': {
                'title': 'Preguntas de RRHH',
                'description': 'Preguntas para evaluar habilidades blandas y ajuste cultural.'
            },
            '03_interview': {
                'title': 'Respuestas Modelo',
                'description': 'Ejemplos de respuestas y consejos para la entrevista.'
            }
        }
        
        combined_output = "# 🎯 Preparación para la Entrevista\n\n"
        
        for file_path in output_files:
            file_key = file_path.split('/')[-1].replace('.md', '')
            section = section_info[file_key]
            emoji = section_emojis[file_key]
            
            # Agregar encabezado de sección con emoji y descripción
            combined_output += f"\n\n## {emoji} {section['title']}\n"
            combined_output += f"_{section['description']}_\n\n"
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Eliminar encabezados redundantes del contenido
                    content = content.replace(f"# {section['title']}\n", "")
                    content = content.replace(f"## {section['title']}\n", "")
                    combined_output += content
            except FileNotFoundError:
                combined_output += f"\n\n### Procesando... por favor espere.\n"
            except Exception as e:
                combined_output += f"\n\nError leyendo {file_path}: {str(e)}"
        
        # Agregar pie de página con consejos
        combined_output += "\n\n---\n"
        combined_output += "💡 **Consejos Finales:**\n"
        combined_output += "- Practica tus respuestas en voz alta\n"
        combined_output += "- Prepara ejemplos específicos de tu experiencia\n"
        combined_output += "- Investiga más sobre la empresa antes de la entrevista\n"
        
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
    
    Esta herramienta te ayudará a prepararte para tu entrevista de trabajo mediante un análisis completo y personalizado.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(
                label="📝 Descripción del Trabajo",
                placeholder="Pega aquí la descripción completa del trabajo...",
                info="Incluye la descripción completa para un mejor análisis.",
                lines=15
            )
            
            with gr.Row():
                submit_btn = gr.Button(
                    "🚀 Analizar Propuesta", 
                    variant="primary",
                    size="lg"
                )
                clear_btn = gr.Button(
                    "🔄 Limpiar",
                    size="lg"
                )
        
        with gr.Column(scale=1):
            output_text = gr.Markdown(
                value="### 📊 Los resultados aparecerán aquí...",
                label="Resultados del Análisis"
            )
    
    with gr.Accordion("💡 Tips y Recomendaciones", open=False):
        gr.Markdown("""
        ### Para obtener mejores resultados:
        
        1. **Descripción Completa** 📋
           - Incluye toda la información del puesto
           - No omitas secciones importantes
        
        2. **Requisitos Específicos** 🎯
           - Asegúrate de incluir los requisitos técnicos
           - Incluye las responsabilidades del puesto
        
        3. **Información de la Empresa** 🏢
           - Agrega cualquier información sobre la cultura
           - Incluye los beneficios mencionados
        """)
    
    def clear_inputs():
        return gr.Textbox.update(value="")
    
    submit_btn.click(
        fn=process_job_posting,
        inputs=input_text,
        outputs=output_text,
        api_name="analyze"
    )
    
    clear_btn.click(
        fn=clear_inputs,
        inputs=[],
        outputs=[input_text]
    )

if __name__ == "__main__":
    demo.launch(
        share=True,
        debug=True
    ) 