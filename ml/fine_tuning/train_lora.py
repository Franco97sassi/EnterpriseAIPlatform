from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
)

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

from ml.fine_tuning.prepare_dataset import prepare_dataset


MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "models/sentiment_lora"


def main():
    # =========================
    # DATASET
    # =========================

    dataset = prepare_dataset()

    # =========================
    # TOKENIZER
    # =========================

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
        )

    tokenized_dataset = dataset.map(
        tokenize,
        batched=True,
    )

    print("Dataset tokenizado:")
    print(tokenized_dataset)

    # =========================
    # MODELO BASE
    # =========================

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
    )

    # =========================
    # CONFIGURACIÓN LoRA
    # =========================

    lora_config = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        target_modules=[
            "q_lin",
            "v_lin",
        ],
    )

    # =========================
    # APLICAR LoRA
    # =========================

    model = get_peft_model(
        model,
        lora_config,
    )

    print("\nParámetros entrenables:")
    model.print_trainable_parameters()

    # =========================
    # DATA COLLATOR
    # =========================

    data_collator = DataCollatorWithPadding(
        tokenizer=tokenizer,
    )

    # =========================
    # TRAINING ARGUMENTS
    # =========================

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        learning_rate=2e-4,
        logging_steps=1,
        save_strategy="no",
        report_to="none",
    )

    # =========================
    # TRAINER
    # =========================

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        data_collator=data_collator,
    )

    print("\nTrainer configurado correctamente.")

    print("\nEjemplos de entrenamiento:")
    print(len(tokenized_dataset["train"]))

    print("Ejemplos de evaluación:")
    print(len(tokenized_dataset["test"]))

    # =========================
    # FINE-TUNING
    # =========================

    print("\nIniciando fine-tuning con LoRA...")

    train_result = trainer.train()

    print("\nFine-tuning terminado.")

    print("\nMétricas de entrenamiento:")
    print(train_result.metrics)

    # =========================
    # GUARDAR ADAPTER LoRA
    # =========================

    model.save_pretrained(
        OUTPUT_DIR
    )

    tokenizer.save_pretrained(
        OUTPUT_DIR
    )

    print(
        f"\nAdapter LoRA guardado en: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()