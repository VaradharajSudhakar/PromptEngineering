from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 


def Prompt_Generator(tools:str):
    if tools == 'tavily_tool':
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    " you should reasearch and understand the user request"
                    " prepare the description for how the image should be based on the analysis and a english quote ,"
                    " you should prepare the image description from the tavily search tool if you dont have the detail description,"
                    " image description should be very detailed and quote should be short and precise in english,"
                    " if you have description for the image generator, tool_calls the Image_Generator tool with description,"
                    " send the image description prepared to te image_generator ,"
                    " You have access to the following tools: {tool_names}.\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        

    elif tools == "Image_Generator":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    " you should call the Image_Generator tool call"
                    " if you have description for the image generator, tool_calls the Image_Generator tool with args as desc,"
                    " You have access to the following tools: {tool_names}.\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    else:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    " You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK, another assistant with different tools "
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any of the other assistants have the final answer or deliverable,"
                    " you should prepare the image description from the tavily search tool if you dont have the detail description,"
                    " if you have description for the image generator, tool_calls the Image_Generator tool with args as desc,"
                    " prefix your response with FINAL ANSWER so the team knows to stop,"
                    # " if you have description for the image generator, tool_calls the Image_Generator tool with args as prompt,"
                    " You have access to the following tools: {tool_names}.\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    return prompt