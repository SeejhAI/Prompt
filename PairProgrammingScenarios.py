import os

import google.generativeai as palm
from google.api_core import client_options as client_options_lib
from dotenv import load_dotenv
import random
load_dotenv()
API_KEY: str = os.getenv("API_KEY")
palm.configure(
    api_key=API_KEY,
    transport="rest",
    client_options=client_options_lib.ClientOptions(
        api_endpoint=os.getenv("GOOGLE_API_BASE"),
    )
)

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model_bison = models[0]
model_bison
from google.api_core import retry
@retry.Retry()
def generate_text(prompt, 
                  model=model_bison, 
                  temperature=0.0):
    return palm.generate_text(prompt=prompt,
                              model=model,
                              temperature=temperature)
    
# Scenario 1: Improve existing code
prompt_template = """
I don't think this code is the best way to do it in Python, can you help me?

{question}

Please explain, in detail, what you did to improve it.
"""
question = """
def func_x(array)
  for i in range(len(array)):
    print(array[i])
"""
completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print(" Scenario 1: Improve existing code")
print(completion.result)
print("\n\n\n\n\n\n\n")

# Ask for multiple ways of rewriting your code

prompt_template = """
I don't think this code is the best way to do it in Python, can you help me?

{question}

Please explore multiple ways of solving the problem, and explain each.
"""

completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print("Ask for multiple ways of rewriting your code")
print(completion.result)
print("\n\n\n\n\n\n\n")

# Paste markdown into a markdown cell
prompt_template = """
I don't think this code is the best way to do it in Python, can you help me?

{question}

Please explore multiple ways of solving the problem, 
and tell me which is the most Pythonic
"""

completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print("Paste markdown into a markdown cell")
print(completion.result)
print("\n\n\n\n\n\n\n")

# Scenario 2: Simplify code

# option 1
prompt_template = """
Can you please simplify this code for a linked list in Python?

{question}

Explain in detail what you did to modify it, and why.
"""

# option 2
prompt_template = """
Can you please simplify this code for a linked list in Python? \n
You are an expert in Pythonic code.

{question}

Please comment each line in detail, \n
and explain in detail what you did to modify it, and why.
"""

question = """
class Node:
  def __init__(self, dataval=None):
    self.dataval = dataval
    self.nextval = None

class SLinkedList:
  def __init__(self):
    self.headval = None

list1 = SLinkedList()
list1.headval = Node("Mon")
e2 = Node("Tue")
e3 = Node("Wed")
list1.headval.nextval = e2
e2.nextval = e3

"""

completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print("Scenario 2: Simplify code")
print(completion.result)
print("\n\n\n\n\n\n\n")



#  Scenario 3: Write test cases
prompt_template = """
Can you please create test cases in code for this Python code?

{question}

Explain in detail what these test cases are designed to achieve.
"""
#  Note that the code I'm using here was output in the previous
# section. Your output code may be different.
question = """
class Node:
  def __init__(self, dataval=None):
    self.dataval = dataval
    self.nextval = None

class SLinkedList:
  def __init__(self):
    self.head = None

def create_linked_list(data):
  head = Node(data[0])
  for i in range(1, len(data)):
    node = Node(data[i])
    node.nextval = head
    head = node
  return head

list1 = create_linked_list(["Mon", "Tue", "Wed"])
"""
completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print("section. Your output code may be different")
print(completion.result)
print("\n\n\n\n\n\n\n")

# Scenario 4: Make code more efficient

prompt_template = """
Can you please make this code more efficient?

{question}

Explain in detail what you changed and why.
"""


question = """
# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        return -1

# Test array
arr = [ 2, 3, 4, 10, 40 ]
x = 10

# Function call
result = binary_search(arr, 0, len(arr)-1, x)

if result != -1:
    print("Element is present at index", str(result))
else:
    print("Element is not present in array")

"""

completion = generate_text(
    prompt = prompt_template.format(question=question)
)
print("Make code more efficient")
print(completion.result)
print("\n\n\n\n\n\n\n")


# Scenario 5: Debug your code

prompt_template = """
Can you please help me to debug this code?

{question}

Explain in detail what you found and why it was a bug.
"""
# I deliberately introduced a bug into this code! Let's see if the LLM can find it.
# Note -- the model can't see this comment -- but the bug is in the
# print function. There's a circumstance where nodes can be null, and trying
# to print them would give a null error.
question = """
class Node:
   def __init__(self, data):
      self.data = data
      self.next = None
      self.prev = None

class doubly_linked_list:
   def __init__(self):
      self.head = None

# Adding data elements
   def push(self, NewVal):
      NewNode = Node(NewVal)
      NewNode.next = self.head
      if self.head is not None:
         self.head.prev = NewNode
      self.head = NewNode

# Print the Doubly Linked list in order
   def listprint(self, node):
       print(node.data),
       last = node
       node = node.next

dllist = doubly_linked_list()
dllist.push(12)
dllist.push(8)
dllist.push(62)
dllist.listprint(dllist.head)

"""

completion = generate_text(
    prompt = prompt_template.format(question=question),
    temperature = 0.7
)

print("Debug your code")
print(completion.result)