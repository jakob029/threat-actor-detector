"""Finetuning module utilizing Hugginfaces SFTTrainer."""

import os
import json

from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported

from unsloth import FastLanguageModel
from huggingface_hub import login

from datasets import Dataset

HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
OUTPUT_DIRECTORY = "<PATH_TO_OUTPUT_MODEL>"
DATASET_PATH = "<PATH_TO_DATASET_FILE>"

DATASET_PROMPT = "<Description of the fine-tuning process prompt>"
EOS_TOKEN = "<|end_of_text|>"


def create_dataset_from_json(json_pointer: str | dict, prompt: str) -> dict:
    """Create a complete formatted dataset.

    Args:
        json_pointer: Object either pointing to JSON file or a json structure.
        prompt: Description of the fine-tuning process prompt.

    Returns:
        Complete dataset.
    """
    if isinstance(json_pointer, str):
        with open(json_pointer, "r", encoding="utf-8") as file:
            clear_dataset = json.load(file)
    else:
        clear_dataset = json_pointer

    dataset_list = []
    for IoC, sentence in clear_dataset.items():
        dataset_list.append(f"{prompt}\n\n### Input:\n{sentence}\n\n### Response\n{IoC}")

    return {"text": dataset_list}


def train_model(training_dataset: str | dict = DATASET_PATH, save_model_to_path: str = OUTPUT_DIRECTORY) -> None:
    """Efficient finning of llama3.2-1B, utilizing frozen parameters (the pretrained parameters are not touched).

    Args:
        training_dataset: Path to JSON file or given dataset.
        save_model_to_path: Directory to save the generated model to.
    """
    login(HUGGINGFACE_TOKEN)

    max_seg_length = 2048  # This means the model will only handle up to 2048 tokens
    dtype = None
    load_in_4bit = True

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Llama-3.2-1B",
        max_seq_length=max_seg_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
    )

    # Loading some LORA extensions
    # No need for qLORA since load_in_4bit = True

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )

    dataset = create_dataset_from_json(training_dataset, DATASET_PROMPT)

    dataset = Dataset.from_dict(dataset)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=max_seg_length,
        dataset_num_proc=2,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            # Sätt num_train_epochs = 1 för att köra full träning
            # (för hela modellen istället för parametrar utanför frysta noder.)
            max_steps=60,
            learning_rate=2e-4,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            output_dir="outputs",
        ),
    )

    trainer.train()

    trainer.save_model(save_model_to_path)
