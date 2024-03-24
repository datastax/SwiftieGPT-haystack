# SwiftieGPT - Haystack Edition

![SwiftieGPT](gh-hero.png)

SwiftieGPT knows Taylor all too well. Ask questions in a clear and concise manner and get back responses based on details from publicly available data on Taylor. From tour dates to song lyrics, learn everything there is to know about the songstress here.

## The Haystack Fork

This is a fork of [SwiftieGPT](https://github.com/datastax/SwiftieGPT) that uses Haystack for ingesting webpages and RSS files.

## Prerequisites

- Python
- Node.js
- An Astra DB account. You can [create one here](https://astra.datastax.com/signup).
- An OpenAI account. You can [create one here](https://platform.openai.com/).

## Set-up

Clone this repository to your local machine:

```
git clone git@github.com:datastax/SwiftieGPT-haystack.git
```

Set-up your Python environment:

```
python -m venv venv  
source venv/bin/activate 
```

Install the Python dependencies:

```
pip install -r requirements.txt
```

Install the Node.js app dependencies:

```
npm install
```

Copy the `.env.example` file to `.env` and set up the following environment variables:

- `OPENAI_API_KEY`: API key for OpenAI
- `ASTRA_DB_API_ENDPOINT`: Your Astra DB vector database endpoint
- `ASTRA_DB_APPLICATION_TOKEN`: The generated app token for your Astra DB

## Ingesting data to Astra DB

Load the website pages:

```
python scripts/load_websites.py
```

Load the RSS files:

```
python scripts/load_rss.py
```

### Running the Next.js web app

Run:

```
npm run dev
``` 

Open [http://localhost:3000](http://localhost:3000) to view the chatbot in your browser.
