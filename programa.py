import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(model='openai/gpt-4o-mini')
api_key = os.environ.get("OPENAI_API_KEY")

assunto = input('Qual o assunto: ')

tool = SerperDevTool()

agent = Agent(
    role='Criador de imagens',
    goal='Ler o arquivo {assunto} e fazer uma imagem realista e precisa.',
    backstory='Você é um experiente designer e ilustrador  capaz de trazer detalhes que poucas pessoas observariam.',
    tools=[tool],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

task = Task(
    description='Sua tarefa é criar uma imagem realista com riquezas de detalhes do {assunto} e trazer uma imagem impactante',
    expected_output='Uma análise detalhada do documento {assunto} trazendo uma imagem realista.',
    tools=[tool],
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential
)

result = crew.kickoff(inputs={"arquivo":assunto })
    
print(result)


