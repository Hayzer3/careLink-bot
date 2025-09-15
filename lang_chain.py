from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY
from my_helper import encode_image
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model=GEMINI_FLASH
)

resposta = llm.invoke("Quais canais do YouTube você recomenda para aprender mais sobre smartphones?")
print("Gemini: ", resposta.content)

# CORREÇÃO: Caminho da imagem
imagem = encode_image(r"dados\snup.jpeg")  # Adiciona 'r' antes


# CORREÇÃO: Template com sintaxe correta
template_analisador = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ 
            Assuma que você é um analisador de imagens. A sua tarefa principal é analisar imagens e extrair
            informações de forma objetiva.

            # Formato de saída
            descrição da imagem: 'coloque a descrição aqui'
            rótulos: 'Coloque uma lista com três termos chave separados por vírgula'
            """
        ),
        (
            "user",
            [
                {
                    "type": "text",
                    "text": "Descreva a imagem: "
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{imagem_informada}"}
                }
            ]
        )
    ]
)

template_resposta = PromptTemplate(
    template="""
    Geere um resumo, utilizando uma linguagem clara e objetiva, focada no público brasileiro. A idéia é que a comunicação
    do resultado seja o mais fácil possível, priorizando registros para consultas posteriores.

    #resultado da imagem
    {resposta_cadeia_analise_imagem}
    """,
    input_variables=["resposta_cadeia_analise_imagem"]
)

cadeia_resumo = template_resposta | llm | StrOutputParser()

cadeia_analise_imagem = template_analisador | llm | StrOutputParser()
cadeia_completa = (cadeia_analise_imagem | cadeia_resumo)
resposta = cadeia_completa.invoke({"imagem_informada": imagem})

print(resposta)