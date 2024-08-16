from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# cau hinh
model_file = "models/vinallama-7b-chat_q5_0.gguf"

# load llm
def load_llm(model_file):
    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=20,
        temperature=0.01,
    )
    return llm


# create prompt
def create_prompt(template):
    prompt = PromptTemplate(template=template, input_variables=['question'])
    return prompt


# create chain
def simple_chain(llm,prompt):
    llm_chain = LLMChain(prompt=prompt,llm=llm)
    return llm_chain


# tao template
template="""
system
Bạn là một trợ lí AI chuyên cung cấp câu trả lời ngắn gọn, đúng trọng tâm.

user {question}
assistant
"""


# tao prompt template
prompt = create_prompt(template)

# tao llm
llm = load_llm(model_file)

# Tạo simple chain mới
llm_chain = simple_chain(llm, prompt)

question = """
Liệt kê Điều 8 : các hành vi bị nghiêm cấm trong lĩnh vực lao động của bộ
Luật lao động chương 1 những quy định chung
"""
response = llm_chain.invoke({"question": question})

print(response)