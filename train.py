from transformers import (
    AutoModelWithLMHead,
    AutoConfig,
    Trainer,
    AutoTokenizer,
    TextDataset,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    GenerateTextArguments,
    generate,
)

import random

# Add the import statement for the generate function
from transformers import GenerateTextArguments, generate

train_dataset = TextDataset(
    tokenizer=tokenizer, file_path="/content/oKay.txt", block_size=128
)
# validation_dataset = TextDataset(
#     tokenizer=tokenizer,
#     file_path="/content/oKay2.txt",
#     block_size=128,
# )
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
training_args = TrainingArguments(
    output_dir="/content/Rewrite5",
    num_train_epochs=1.0,
    per_device_train_batch_size=2,
    # optim="adafactor",
    # gradient_accumulation_steps=4,
    # gradient_checkpointing=True,
    # use_cache=False,
    logging_dir="/content/Rewrite5",
    save_steps=4000,
)
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Define the callback function
def sample_during_training(trainer, model, tokenizer):
  def callback(eval_step, logs):
    # Generate and print samples every 1000 steps
    if eval_step % 1000 == 0:
      prompts = ["The President of the United States is", "The Vice President of the United States is"]  # set the prompts to generate samples from
      for prompt in prompts:
        text = tokenizer.encode(prompt)
        myinput, past_key_values = torch.tensor([text]), None
        myinput = myinput.to(device)
        logits, past_key_values = model(myinput, past_key_values=past_key_values, return_dict=False)
        logits = logits[0, -1]
        probabilities = torch.nn.functional.softmax(logits)
        best_logits, best_indices = logits.topk(4)
        best_words = [tokenizer.decode([idx.item()]) for idx in best_indices]
        print(best_words)
  return callback

# Add the callback to the trainer
trainer.add_callback(sample_during_training(trainer, model, tokenizer))

# Start training
trainer.train()
