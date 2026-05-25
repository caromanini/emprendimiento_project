from google import genai
from google.genai import types
from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
AI_MODEL = "gemini-3.1-flash-lite"

def get_chat_response(message: str, chat_history: list, topics: list):
    topic_instructions = "\n".join([f"- {t}" for t in topics]) if topics else "- Hazle compañía y pregúntale cómo se siente hoy."

    system_instructions = get_cami_system_prompt(topic_instructions)

    config = types.GenerateContentConfig(
        system_instruction=system_instructions,
        temperature=0.7,
        max_output_tokens=300,
    )

    formatted_contents = []
    for msg in chat_history:
        formatted_contents.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    formatted_contents.append(
        types.Content(
            role="user", 
            parts=[types.Part.from_text(text=message)]
        )
    )

    try:
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=formatted_contents,
            config=config
        )
        return response.text
    except Exception:
        return "Lo siento mucho, tuve un pequeño mareo técnico. ¿Me puedes repetir lo último que me dijiste?"

def generate_daily_report(chat_history: list, topics: list) -> str:
    if not chat_history:
        return "No hay conversación registrada el día de hoy."

    topic_instructions = "\n".join([f"- {t.instruction}" for t in topics]) if topics else "- Sin tareas específicas."
    conversation = "\n".join([f"{'Abuelo' if m.role == 'user' else 'Bot'}: {m.content}" for m in chat_history])
    report = get_daily_report_instructions(topic_instructions, conversation)

    try:
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=report,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=300
            )
        )
        return response.text
    except Exception as e:
        print(f"Error generando reporte: {e}")
        return "Ocurrió un error al intentar generar el resumen de hoy."

def get_cami_system_prompt(topic_instructions: str):
    return f"""
    Eres C.A.M.I., un asistente virtual sumamente cálido, paciente y empático, que le hace compañía a adultos mayores por WhatsApp.
    
    Tu misión a lo largo de la conversación de hoy es averiguar discretamente esta información:
    {topic_instructions}
    
    REGLAS DE CONVERSACIÓN:
    1. EMPATÍA ACTIVA (Prioridad Máxima): Si el usuario menciona que se siente mal, que le duele algo, que tuvo un accidente o que está triste, DETÉN tu misión principal. Muestra genuina preocupación y haz una pregunta breve de seguimiento sobre ese tema para saber cómo está.
    2. RITMO NATURAL: No lances tus tareas como un checklist. Intercala tus preguntas con comentarios amables sobre lo que te cuentan. 
    3. UNA PREGUNTA A LA VEZ: Jamás incluyas más de una pregunta en el mismo mensaje. No los abrumes.
    4. BREVEDAD Y CERCANÍA: Habla corto (2 o 3 oraciones como máximo). Usa modismos chilenos suaves y respetuosos si encajan en la charla.
    5. CONDICIÓN DE TÉRMINO: Solo cuando hayas validado tus tareas principales de forma natural, despídete con mucho cariño hasta mañana.
    """

def get_daily_report_instructions(topic_instructions, conversation):
    return f"""
    Eres un asistente clínico y analítico. Tu tarea es leer la transcripción del chat de hoy entre un adulto mayor y un bot, y generar un resumen conciso para el familiar a cargo.

    TAREAS QUE EL BOT DEBÍA AVERIGUAR HOY:
    {topic_instructions}

    TRANSCRIPCIÓN DEL CHAT DE HOY:
    {conversation}

    INSTRUCCIONES DE FORMATO ESTRICTAS:
    Genera el reporte usando exactamente esta estructura:
    1. Estado de Ánimo y Salud general: (Breve resumen de cómo se siente).
    2. Cumplimiento de Tareas: (Indica claramente si cumplió o no las tareas asignadas basándote en lo que respondió).
    3. Alertas o Novedades: (Cualquier cosa fuera de lo común, como dolores, caídas, o simplemente di "Sin novedades").
    
    Sé muy directo, profesional y breve. No incluyas saludos ni despedidas.
    """