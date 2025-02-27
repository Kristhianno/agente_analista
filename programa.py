import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


def main():

    st.title('Agente Analisador')
    st.text('Insira o arquivo')
    input = st.file_uploader(label='Coloque o arquivo aqui.')

    llm = ChatOpenAI(model='openai/gpt-4o-mini')
    api_key = os.environ.get("OPENAI_API_KEY")


    tool = PDFSearchTool()

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
        description='Sua tarefa é executar uma análise detalhada do documento {input} e trazer em tópicos o que você viu',
        expected_output='Uma análise detalhada do documento {input} sugerindo melhorias.',
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
        input = input('O arquivo é :  ')
        if input == 'exit':
            break
        result = crew.kickoff(inputs={"input": input})
        
        print(result)


main()