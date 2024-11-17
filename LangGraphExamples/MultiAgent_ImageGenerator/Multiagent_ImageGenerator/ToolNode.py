from langgraph.prebuilt import ToolNode
from Tools import *


tools = [tavily_tool, Image_Generator]
tool_node = ToolNode(tools)