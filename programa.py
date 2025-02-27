import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

tool = FileReadTool()
llm = ChatGroq(model='groq/llama3-70b-8192')
api_key = os.environ.get("GROQ_API_KEY")


agent = Agent(
    role='Analista de Documentos',
    goal='Ler o arquivo {input} e trazer detalhes do documento.',
    backstory='Você é um experiente analista de documentos capaz de trazer detalhes que poucas pessoas observariam.',
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

task = Task(
    description='Sua tarefa é executar uma análise detalhada do documento {input}',
    expected_output='Uma análise detalhada do documento {input}.',
    tools=[tool],
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential
)

while True:
    input = input('O arquivo é : ')
    if input == 'exit':
        break
    result = crew.kickoff(inputs={"input": input})
    print(result)