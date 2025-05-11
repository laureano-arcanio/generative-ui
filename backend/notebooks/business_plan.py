# %%
import sys
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from prompts import (
    describe_business_prompt,
    business_overview_questions_prompt,
    analyse_business_overview_questions_prompt,
    business_owner_characteristics_prompt,
)
from business_descriptions import (
    forniture_tiny_spaces
)
from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")


# Print the Python version
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

# Generate a filename using LangChain
def generate_filename(description, model):
    prompt = """
    Generate a concise and descriptive filename (under 30 characters) 
    Based on the content of the business description.
    The filename should reflect the main theme or focus of the business.
    from the following business description:\n\n
    use snake_case format,
    and avoid using spaces, special characters, or punctuation.
    The filename should be in lowercase.
    The filename should not include the file extension.
    """
    message = model.invoke(
        [
            SystemMessage(
                content=prompt,
            ),
            HumanMessage(
                content=description,
            ),
        ]
    )
    return f"{message.content.strip()}.md"

# Write content to a Markdown file
def write_to_markdown(filename, sections):
    with open(filename, "w", encoding="utf-8") as file:
        for title, content in sections.items():
            file.write(f"# {title}\n\n")
            file.write(f"{content}\n\n")

# Abstract model invocation logic
def model_invoke(model, system_message, user_message=None):
    message_template = ChatPromptTemplate.from_messages(
        [("system", system_message), ("user", "{text}")]
    )
    
    prompt = message_template.invoke({"text": user_message})
    response = model.invoke(prompt)
    return response.content


# %%
# Describe the business

model = init_chat_model("gpt-4.1-nano", model_provider="openai")
print("Business desciption rewrited")

# business_desciption =  microlearning_platform
business_desciption =  forniture_tiny_spaces

business_desciption_rewrited = model_invoke(model, describe_business_prompt, business_desciption)
print("Business description rewrited")
print(business_desciption_rewrited)
filename = generate_filename(business_desciption_rewrited, model)

sections = {
    "Rewritten Business Description": business_desciption_rewrited,
}

# %%
# Business overview questions

business_overview_questions = model_invoke(model, business_overview_questions_prompt, business_desciption_rewrited)
print("Business overview questions")
print(business_overview_questions)

sections["Business Overview Questions"] = business_overview_questions

# %%
# Business overview questions analysis

business_overview_questions_analysis = model_invoke(model, analyse_business_overview_questions_prompt, business_overview_questions)
print("Business overview questions analysis")
print(business_overview_questions_analysis)

sections["Business Overview Questions Analysis"] = business_overview_questions_analysis

# %%
# Business owner characteristics

business_owner_characteristics = model_invoke(model, business_owner_characteristics_prompt, business_desciption_rewrited)
print("Business owner characteristics")
print(business_owner_characteristics)

sections["Business Owner Characteristics"] = business_owner_characteristics

# Write all sections to the Markdown file
write_to_markdown(filename, sections)
print(f"Results written to {filename}")

# %%

class Question(BaseModel):
    """A class representing a question and its answer."""
    question: str  = Field(description="- The question to be answered")
    answer: str = Field(description="* The answer to the question")

class BusinessOverviewQuestions(BaseModel):
    """A class representing a list of business overview questions."""
    questions: list[Question] = Field(description="A list of questions and answers")


promprt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract questions and answers from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value."
            "Questions are marqued with a dash (-) and answers with an asterisk (*). "
         ),
        ("user", "{text}"),
    ]
)

prompt = promprt_template.invoke(
    {
        "text": business_overview_questions
    }
)


structured_model = model.with_structured_output(BusinessOverviewQuestions)

structured_response = structured_model.invoke(prompt)
print("Structured response:")
print(structured_response)

# %%
