import os
from dotenv import load_dotenv
import textwrap
import google.generativeai as genai
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from IPython.display import Markdown

class ColabTextAnalyzer:
    def __init__(self, pdf_directory):
        self.pdf_directory = pdf_directory
        self.genai_key = None

    def setup(self):
        genai.configure(api_key=self.genai_key)
        load_dotenv()

    def load_documents(self):
        loader = PyPDFDirectoryLoader(self.pdf_directory)
        data = loader.load_and_split()
        context = "\n".join(str(p.page_content) for p in data)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
        texts = text_splitter.split_text(context)
        return texts

    def create_embeddings(self, texts):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_index = Chroma.from_texts(texts, embeddings).as_retriever()
        return vector_index

    def analyze_question(self, question):
        docs = self.vector_index.get_relevant_documents(question)
        return self.chat_documents(docs, question)

    def chat_documents(self, docs, question):
        prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
        return self.to_markdown(response['output_text'])

    def to_markdown(self, text):
        text = text.replace('•', '*')
        return Markdown(textwrap.indent(text, '>', predicate=lambda _: True))

    def run_all(self):
        self.setup()
        texts = self.load_documents()
        self.vector_index = self.create_embeddings(texts)
        question = input("Enter your question: ")
        answer = self.analyze_question(question)
        print(answer)
