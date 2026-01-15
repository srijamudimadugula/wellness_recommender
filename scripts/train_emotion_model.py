import os
import torch
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    TrainingArguments, 
    Trainer
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Constants
MODEL_CHECKPOINT = "distilbert-base-uncased"
DATASET_NAME = "dair-ai/emotion" # Standard emotion dataset
OUTPUT_DIR = "./models/emotion_classifier_finetuned"
NUM_LABELS = 6

def compute_metrics(eval_pred):
    load_metric = lambda x, y: precision_recall_fscore_support(x, y, average='weighted')
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def main():
    print("Loading dataset...")
    # Load emotion dataset
    dataset = load_dataset(DATASET_NAME)
    
    print("Initializing tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)
    
    encoded_dataset = dataset.map(tokenize_function, batched=True)
    
    print("Initializing model...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_CHECKPOINT, 
        num_labels=NUM_LABELS
    ).to(device)
    
    # Practical Engineering: Freeze early layers to simulate efficient fine-tuning
    # Freezing embeddings and first 4 layers, training only last 2 + classifier
    for param in model.distilbert.embeddings.parameters():
        param.requires_grad = False
        
    for layer in model.distilbert.transformer.layer[:4]:
        for param in layer.parameters():
            param.requires_grad = False
            
    print("Model layers frozen. Training only top layers.")

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_dir='./logs',
        logging_steps=100,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encoded_dataset["train"],
        eval_dataset=encoded_dataset["validation"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    print("Starting training...")
    trainer.train()
    
    print("Evaluating...")
    test_results = trainer.evaluate(encoded_dataset["test"])
    print(f"Test Results: {test_results}")
    
    print(f"Saving model to {OUTPUT_DIR}")
    trainer.save_model(OUTPUT_DIR)

if __name__ == "__main__":
    main()
