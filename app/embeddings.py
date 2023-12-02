import os
from langchain.embeddings import OpenAIEmbeddings
import util

os.environ["OPENAI_API_KEY"] = util.OPENAI_API_KEY
embeddings_model = OpenAIEmbeddings()