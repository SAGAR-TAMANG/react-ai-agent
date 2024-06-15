class Agent:
  def __call__(self, *args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)
    return ("Hey, I am being called.")

agent = Agent()

print(agent())

import re

action = "Action: average_dog_weight: Border Collie"

print(action[])