from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union
import feedparser
from bs4 import BeautifulSoup
from haystack import Document, component, default_from_dict, default_to_dict, logging
from haystack.components.converters.utils import get_bytestream_from_source, normalize_metadata
from haystack.dataclasses import ByteStream

logger = logging.getLogger(__name__)

@component
class RSSToDocument:
    """
    Converts an RSS file to a Document.

    Usage example:
    ```python
    from rss import RSSToDocument

    converter = RSSToDocument()
    results = converter.run(sources=["path/to/sample.rss"])
    documents = results["documents"]
    print(documents[0].content)
    # 'This is a text from the RSS file.'
    ```
    """

    def __init__(
        self,
    ):
        """
        Create an RSSToDocument component.
        """

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the component to a dictionary.

        :returns:
            Dictionary with serialized data.
        """
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RSSToDocument":
        """
        Deserializes the component from a dictionary.

        :param data:
            The dictionary to deserialize from.
        :returns:
            The deserialized component.
        """
        return default_from_dict(cls, data)

    @component.output_types(documents=List[Document])
    def run(
        self,
        sources: List[Union[str, Path, ByteStream]],
        meta: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    ):
        """
        Converts a list of RSS files to Documents.

        :param sources:
            List of RSS file paths or ByteStream objects.
        :param meta:
            Optional metadata to attach to the Documents.
            This value can be either a list of dictionaries or a single dictionary.
            If it's a single dictionary, its content is added to the metadata of all produced Documents.
            If it's a list, the length of the list must match the number of sources, because the two lists will be zipped.
            If `sources` contains ByteStream objects, their `meta` will be added to the output Documents.

        :returns:
            A dictionary with the following keys:
            - `documents`: Created Documents
        """

        documents = []
        meta_list = normalize_metadata(meta=meta, sources_count=len(sources))
        

        for source, metadata in zip(sources, meta_list):
            try:
                bytestream = get_bytestream_from_source(source=source)
            except Exception as e:
                logger.warning("Could not read {source}. Skipping it. Error: {error}", source=source, error=e)
                continue
            try:
                file_content = bytestream.data.decode("utf-8")
                feed = feedparser.parse(file_content)
                text = ''
                for item in feed.entries:
                    text = text + item.title + ' ' + item.description + ' '
                soup = BeautifulSoup(text, "html.parser")
                text = soup.text
            except Exception as conversion_e:
                logger.warning(
                    "Failed to extract text from {source}. Skipping it. Error: {error}",
                    source=source,
                    error=conversion_e,
                )
                continue

            merged_metadata = {**bytestream.meta, **metadata}
            document = Document(content=text, meta=merged_metadata)
            documents.append(document)

        return {"documents": documents}