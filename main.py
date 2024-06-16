from typing import Any
from dotenv import load_dotenv
import google.generativeai as genai 
import os, re

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API'))

model = genai.GenerativeModel('gemini-1.5-flash')

# chat = model.start_chat(history=[])

# print(chat.send_message('Hi'))

prompt = """
INSTURCTIONS:

You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()

class Agent:
  def __init__(self, system=''):
    self.system = system
    self.messages = []

    if self.system:
      self.messages.append({
        'parts': [{
          'text': system
          }],
        'role': 'user'
      })
    
  def __call__(self, messages):
    self.chat = model.start_chat(history=self.messages)
    
    result = self.execute(messages)

    self.messages.append({
      'parts': [{
        'text': messages
      }],
      'role': 'user'
    })
    self.messages.append({
      'parts': [{
        'text': result
      }], 
      'role': 'model'
    })

    return result

  def execute(self, messages):
    response = self.chat.send_message(messages)
    return response.text
  
  def calculate(what):
    return eval(what)
  
  def average_dog_weight(name):
      if name in "Scottish Terrier": 
          return("Scottish Terriers average 20 lbs")
      elif name in "Border Collie":
          return("a Border Collies average weight is 37 lbs")
      elif name in "Toy Poodle":
          return("a toy poodles average weight is 7 lbs")
      else:
          return("An average dog weights 50 lbs")

  known_actions = {
      "calculate": calculate,
      "average_dog_weight": average_dog_weight
  }

action_re = re.compile('^Action: (\w+): (.*)$')   # python regular expression to selection action

# abot = Agent(prompt)
# result = abot('How much does a toy poodle weigh?')
# print(result)

def query(question, max_turns=5):
  i = 0
  bot = Agent(prompt)
  next_prompt = question
  while i < max_turns:
    result = bot(next_prompt)
    print(result)
    try:
      actions = [
        action_re.match(a)
        for a in result.split('\n')
        if action_re.match(a)
      ]
    except:
       print('EXCEPTION OCCURED AT actions')

    if actions:
      #  Action found to run
      action, actions_input = actions[0].groups()

      if action not in bot.known_actions:
         raise Exception(f'Unknown action: {action, actions_input}')
      print(f'-- running {action} {actions_input}')
      Observation = bot.known_actions[action](actions_input)
      print("Observation:", Observation)
      next_prompt = f"Observation: {Observation}"
    else:
      return

# query('How much does a toy poodle weigh?')
query('I have 2 dogs, a border collie and /a scottish terrier. What is their combined weight')

# if __name__ == "__main__":
#   main()
# else:
#   print("Failed At Beginning")