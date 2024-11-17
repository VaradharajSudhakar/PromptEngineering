from Graph import *

events = graph.stream(
    {
        "messages": [
            HumanMessage(
                content="create a image for diwali greeting with some quotes in english"
            )
        ],
    },
    # Maximum number of steps to take in the graph
    {"recursion_limit": 100},
)
for s in events:
    print(s)
    print("----")