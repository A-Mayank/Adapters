# 1. Install the right library (if not installed already)
# !pip install adapter-transformers

import os
import torch
from datasets import load_dataset, Dataset
from transformers import (
    AutoTokenizer,
    TrainingArguments,
    AutoConfig,
    AutoModelForMaskedLM,
)
from adapters import AutoAdapterModel, AdapterConfig, AdapterTrainer

# 2. Load Tokenizer & Base Model (MLM Head)
model_name = "ai4bharat/indic-bert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)

# 3. Add a Language Adapter
adapter_name = "bhojpuri_mlm"
model.add_adapter(adapter_name)
model.add_masked_lm_head(adapter_name)  # Needed for MLM task
model.train_adapter(adapter_name)  # Freeze rest of model

# 4. Load Unlabeled Dataset
# You should replace this with your actual file path
dataset = load_dataset(
    "text", data_files={"train": "Datasets\Bhojpuri_unlabeeeld data.txt"}
)


# 5. Tokenize the Dataset
def tokenize_function(example):
    return tokenizer(
        example["text"], truncation=True, padding="max_length", max_length=128
    )


tokenized_dataset = dataset.map(tokenize_function, batched=True)

# 6. MLM-specific data collator (dynamic masking)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

# 7. Define Training Arguments
training_args = TrainingArguments(
    output_dir="./bhojpuri_adapter_model",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=16,
    save_steps=1000,
    save_total_limit=2,
    logging_steps=100,
    learning_rate=5e-5,
    prediction_loss_only=True,
)

# 8. Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator,
)

# 9. Train the Adapter
trainer.train()

# 10. Save the trained adapter
model.save_adapter("./bhojpuri_adapter", adapter_name)
