import os
import openai
from dotenv import load_dotenv
import datetime
import json

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def extract_task_info(user_input):
    """
    Extract task content and due time from user input using OpenAI API
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts task information from user input. Extract the task content and the due time. Return a JSON object with 'task' and 'due_time' fields. The due_time should be in ISO format."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.1,
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Ensure we have both task and due_time
        if 'task' not in result or 'due_time' not in result:
            return None
            
        # Parse the due_time to a datetime object
        try:
            due_time = datetime.datetime.fromisoformat(result['due_time'])
        except ValueError:
            # If parsing fails, try a more flexible approach
            try:
                from dateutil import parser
                due_time = parser.parse(result['due_time'])
            except:
                return None
                
        return {
            "content": result['task'],
            "due_time": due_time
        }
    except Exception as e:
        print(f"Error extracting task info: {e}")
        return None