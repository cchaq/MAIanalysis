from typing import Optional

from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_self_ask_with_search_agent
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain_experimental.tools import PythonREPLTool

python_repl = PythonREPLTool()
wikipedia_api_wrapper = WikipediaAPIWrapper(lang="en", top_k_results=3)

def load_tools(tool_names: list[str], llm: Optional[BaseLanguageModel] = None,) -> list[BaseTool]:
    prompt = hub.pull("hwchase17/self-ask-with-search")
    search_wrapper = DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper())
    search_tool = Tool(name="Intermediate Answer", func=search_wrapper.invoke, description="Search",)
    self_ask_agent = AgentExecutor(agent=create_self_ask_with_search_agent(llm=llm, tools=[search_tool],prompt=prompt,),
                                   tools=[search_tool],)
    
    available_tools = {
        "ddg-search": DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper()),
        "wikipedia": WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)
    }


    tools = []
    for name in tool_names:
        if name in available_tools:
            tools.append(available_tools[name])
    return tools