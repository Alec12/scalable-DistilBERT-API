from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "winegarj/distilbert-base-uncased-finetuned-sst2"
save_directory = "./distilbert-base-uncased-finetuned-sst2"

# Download and save the model
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.save_pretrained(save_directory)

# Download and save the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

print(f"Model and tokenizer saved to {save_directory}")