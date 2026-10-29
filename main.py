import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    # 1. Bucle principal del Agente (límite de 20 iteraciones)
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions, 
        )
        
        if response.usage is None:
            raise RuntimeError("No response received from the OpenAI API.")
            
        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens} | Response tokens: {response.usage.completion_tokens}")
            
        message = response.choices[0].message
        
        # 2. Añadimos la respuesta del asistente al historial de mensajes ANTES de procesar las herramientas
        messages.append(message)
        
        # 3. Comprobamos si el LLM decidió usar herramientas
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                
                if not result_message.get("content"):
                    raise Exception("El resultado de la función está vacío")
                
                if args.verbose:
                    # Truncamos el output en consola si es muy largo, para no saturar la pantalla
                    print(f"-> {result_message['content'][:200]}...")
                
                # 4. Añadimos el resultado de la herramienta al historial
                messages.append(result_message)
        else:
            # 5. Si no hay llamadas a herramientas, es el mensaje final
            if message.content:
                print("\nFinal response:")
                print(message.content)
            
            # Salimos del bucle (y del programa) porque el agente ha terminado
            return

    # 6. Si el bucle termina las 20 iteraciones sin llegar al "return", hubo un problema
    print("\nError: The agent reached the maximum number of iterations (20) without completing the task.")
    sys.exit(1)

if __name__ == "__main__":
    main()