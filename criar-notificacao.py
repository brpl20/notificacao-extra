import os
from openai import OpenAI
from PyPDF2 import PdfReader
from PIL import Image
from pytesseract import image_to_string

client = OpenAI(api_key="")

input_folder = "."
output_folder = "output"

json_object = {}

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page_num in range(min(4, len(reader.pages))):
        page = reader.pages[page_num]
        text += page.extract_text() + "\n"

    return text


texto_notificante = "NOTIFICANTE: "

advogado = "BRUNO "

texto_notificado = "NOTIFICADO "

texto_notificacao = "O(A) notificante foi colaborador(a) da empresa no período de, conforme cópia do CNIS e CTPS anexa, e por isso solicita o fornecimento dos seguintes documentos para fins previdenciários:  1. PERFIL PROFISSIOGRÁFICO PREVIDENCIÁRIO – PPP (ou formulário equivalente DIRBEN-8030, DSS-8030, DISES-BE 5235, SB-40); \n 2. LAUDO TÉCNICO (LTCAT, PPRA, PCMSO, PCMAT, PGR etc.) que serviu de base para elaboração do PPP; \n 3. COMPROVANTE DE ENTREGA e CERTIFICADO DE APROVAÇÃO DOS EPI´s, caso haja indicação de que o(a) notificante tenha feito a utilização dos equipamentos. \n 4. Na hipótese de não haver laudo ou responsável técnico referente a todo o período em que houve a execução do trabalho, poderá ser apresentado documento extemporâneo, ainda que de funcionário diverso, desde que de atividade similar. \n 5. Nesse caso, o laudo deverá ser acompanhado de declaração da empresa, assinada pelo representante legal, relatando a inexistência de documentação contemporânea ao exercício do labor e informando que o ambiente de trabalho não sofreu modificações ao longo do tempo, nos termos da tese fixada no âmbito do Tema 208 pela Turma Nacional de Uniformização. \n 6. Caso não seja possível o fornecimento de algum documento, favor manifestar-se sobre a respectiva indisponibilidade, por meio de declaração assinada e carimbada pelo representante legal da empresa. \n 7. Ressalte-se que a elaboração e o fornecimento dos documentos solicitados deve ser efetuado de acordo com os parâmetros exigidos pelo INSS, observando a legislação vigente (em especial a IN/128 do INSS, Decreto n° 3.048/99 e Lei n° 8.213/91), devendo conter a mensuração adequada dos fatores de risco, indicação do responsável técnico (engenheiro ou médico do trabalho, nos termos do art. 68, §3°, do Decreto n° 3.048/99), carimbo e assinatura do responsável legal da empresa, sob pena de inviabilizar o direito previdenciário do notificante e implicar em eventual responsabilização do empregador. \n 8. Qualquer assunto pertinente à presente notificação deverá ser direcionado diretamente ao procurador signatário, via e-mail , pelo telefone  ou no endereço do procurador indicado na qualificação desta notificação, no prazo de 10 (dez) dias úteis a contar do recebimento. Cientes de vossa colaboração, agradecemos desde já pela atenção despendida."


def ask_chatgpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extraia o CNPJ da empresa e seu endereço, crie uma notificação extrajudicial com base no texto fornecido:  "},
            {"role": "user", "content": f"Crie um texto combinando o {texto_notificante}, o {advogado}, o {texto_notificado} com o texto do {prompt} e o {texto_notificacao}"}

        ]
    )
    return response.choices[0].message.content

def process_pdf_files(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(input_path)

            prompt = f"Texto extraído do PDF:\n\n{text}"
            #print(prompt)
            result = ask_chatgpt(prompt)
            json_object['response'] = result


            output_path = os.path.join(output_folder, f"{filename}.md")
            with open(output_path, "w") as output_file:
                output_file.write(result)

process_pdf_files(input_folder)
