from typing import Literal

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains.base import Chain #TODO maybe this needs updating from langchain.chains to langchain.chain.base
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI

from tools_loader import load_tools
from config import set_environment

set_environment()

ReasoningStrategies = Literal["zero-shot-react","plan-and-solve"]

def load_agent(tool_names: list[str], strategy: ReasoningStrategies = "zero-shot-react") -> Chain:
    llm = ChatOpenAI(temperature=0, streaming=True)
    tools = load_tools(tool_names=tool_names, llm=llm)
    if strategy == "plan-and-solve":
        planner = load_chat_planner(llm)
        executor = load_agent_executor(llm, tools, verbose = True)
        return PlanAndExecute(planner=planner, executor=executor, verbose=True)
    
    prompt = hub.pull("hwchase17/react")
    return AgentExecutor(
        agent=create_react_agent(llm=llm, tools=tools, prompt=prompt), tools=tools
    )

def openai_file_analysis(file_attributes: dict) -> str:
    """"Analyse file attributes using openAI language model"""
    prompt_template = PromptTemplate(
        input_variables = ["attributes"],
        template="""
        You are a file analysis expert. Below are the details from VirusTotal about a file:
        {attributes}
        
        Based on the details, provide a detailed analysis of the file, including its potential risks, 
        why it might be flagged as malicious, and any recommendations for the user.
        """
    )

    openai_model = OpenAI(temperature=0)
    prompt = prompt_template.format(attributes=file_attributes)
    return openai_model(prompt)