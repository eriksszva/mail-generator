import pandas as pd
import chromadb
import uuid
import os
import logging

class Portofolio():
    def __init__(self, file_path='resources/portofolio.csv'):
        # setting up logging configuration
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        self.file_path = file_path
        self.data = None
        self.chroma_client = None
        self.collection = None

        self.logger.info(f'Initializing Portofolio with file path: {self.file_path}')

        # attempt to read CSV data
        try:
            self.data = pd.read_csv(file_path)
            self.logger.info(f'Data loaded: {self.data.tail()}')
            self.logger.info('CSV file loaded successfully')
        except Exception as e:
            self.logger.error(f'Error loading CSV file: {e}')
            raise

        try:
            self.chroma_client = chromadb.HttpClient(host='server', port=8000)
            self.collection = self.chroma_client.get_or_create_collection(name='portofolio')
            self.logger.info('Chroma client initialized and collection created')
        except Exception as e:
            self.logger.error(f'Error initializing Chroma client or collection: {e}')
            raise

    def load_portofolio(self):
        self.logger.info('Loading portofolio data into ChromaDB')
        try:
            if not self.collection.count():
                self.logger.info('No data found in collection, loading new data')
                for _, row in self.data.iterrows():
                    self.collection.add(
                        documents=row['Techstack'],
                        metadatas={'Links': row['Links']},
                        ids=[str(uuid.uuid4())]
                    )
                self.logger.info('Data successfully loaded into ChromaDB')
            else:
                self.logger.info('Data already exists in the ChromaDB collection')
        except Exception as e:
            self.logger.error(f'Error loading data into ChromaDB: {e}')
            raise

    def query_links(self, skills):
        self.logger.info(f'Querying ChromaDB with skills: {skills}')
        try:
            result = self.collection.query(
                query_texts=skills,
                n_results=2
            ).get('metadatas', [])
            self.logger.info(f'Query results: {result}')
            return result
        except Exception as e:
            self.logger.error(f'Error querying ChromaDB: {e}')
            raise