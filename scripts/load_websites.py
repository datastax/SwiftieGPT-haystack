import logging
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from rss import RSSToDocument
from haystack.components.writers import DocumentWriter
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.document_stores.astra import AstraDocumentStore

# load variable defined in .env into the environment
load_dotenv()

# turn on logging at the INFO level
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

# initialize the fetcher that will download content from a webpage as HTML
fetcher = LinkContentFetcher()

# initialize the converter that will take HTML and turn it into plain text
converter = HTMLToDocument()

# initialize the splitter that will take the text and break it into chunks
splitter = DocumentSplitter(split_by="word", split_overlap=50, split_length=150)

# define the model that we'll use to create embeddings
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"

# initialize the document store
document_store = AstraDocumentStore(
    duplicates_policy=DuplicatePolicy.SKIP,
    embedding_dimension=384,
    collection_name="swiftipedia"
)

# initialize the Haystack pipeline
index_pipeline = Pipeline()

# add the components to the pipeline
index_pipeline.add_component(instance=SentenceTransformersDocumentEmbedder(model=embedding_model_name), name="embedder")
index_pipeline.add_component(instance=fetcher, name="fetcher")
index_pipeline.add_component(instance=converter, name="converter")
index_pipeline.add_component(instance=splitter, name="splitter")
index_pipeline.add_component(instance=DocumentWriter(document_store=document_store, policy=DuplicatePolicy.SKIP), name="writer")

# connect the components in the order they should be executed
index_pipeline.connect("fetcher.streams", "converter.sources")
index_pipeline.connect("converter.documents", "splitter.documents")
index_pipeline.connect("splitter.documents", "embedder.documents")
index_pipeline.connect("embedder.documents", "writer.documents")

taylorPages = [
  'https://time.com/6342806/person-of-the-year-2023-taylor-swift/',
  'https://en.wikipedia.org/wiki/Taylor_Swift',
  'https://en.wikipedia.org/wiki/Taylor_Swift_albums_discography',
  'https://www.taylorswift.com/tour/',
  'https://taylorswift.tumblr.com/',
  'https://www.forbes.com/profile/taylor-swift/?sh=242c42f818e2',
  'https://taylorswiftstyle.com/',
  'https://www.tstheerastourfilm.com/participating-territories/',
  'https://www.cosmopolitan.com/entertainment/celebs/a29684699/taylor-swift-dating-boyfriend-history/E',
  'https://www.tstheerastourfilm.com/participating-territories/',
  'https://en.wikipedia.org/wiki/The_Eras_Tour',
  'https://taylorswift.fandom.com/wiki/The_Eras_Tour',
  'https://www.taylorswiftweb.net/',
  'https://taylorswift.fandom.com/wiki/Taylor_Swift_Wiki'
]

# run the pipeline
index_pipeline.run(data={"fetcher": {"urls": taylorPages}})

# print the number of documents processed
print(document_store.count_documents())
