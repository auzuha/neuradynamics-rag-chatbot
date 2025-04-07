


# How to run:
- Pull the qdrant image from docker: ```docker pull qdrant/qdrant```
- Run the qdrant docker container: ```docker run -p 6333:6333 -v ~/qdrant_storage:/qdrant/storage qdrant/qdrant```
- Make sure you have all the environment variables set in the .env file.
- Run the streamlit server: ```streamlit run .\main.py```
- The Chat UI will be available on ```http://localhost:8501/```
- You can ask the bot about the weather in any cities, or ask it to fetch information from the documents that you upload.