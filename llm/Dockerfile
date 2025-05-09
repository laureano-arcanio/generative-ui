# Use the official Ollama image
FROM ollama/ollama

# Set up any additional configurations if needed

# Pull the llama3.2:3b model
RUN ollama pull llama3.2:3b

# Expose the default port used by Ollama
EXPOSE 11434

# Command to run the Ollama container
CMD ["ollama", "serve"]