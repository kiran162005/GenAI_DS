# Fine-Tuning BERT for POS Tagging

This project demonstrates how to fine-tune a BERT model for Part-of-Speech (POS) tagging using token classification.

## 📌 Objective
To build a transformer-based model that assigns grammatical labels (POS tags) to each word in a sentence.

## 📊 Dataset
- CoNLL-2003 Dataset
- Contains annotated data for POS tagging and chunking

## ⚙️ Technologies Used
- Python
- Hugging Face Transformers
- Datasets Library
- PyTorch
- Seqeval (for evaluation)

## 🔄 Workflow
1. Load dataset
2. Tokenization using BERT tokenizer
3. Label alignment
4. Model training using Trainer API
5. Evaluation using precision, recall, F1-score
6. Inference on custom sentences

## 📈 Evaluation Metrics
- Precision
- Recall
- F1 Score

## 🧠 Key Concepts
- Token Classification
- Transformer Models (BERT)
- Sequence Labeling
- Subword Tokenization

## ⚖️ POS Tagging vs Chunking

| POS Tagging | Chunking |
|------------|---------|
| Word-level classification | Phrase-level grouping |
| Easier | More complex |
| Example: NOUN, VERB | Example: NP, VP |

## 🚀 Results
The model successfully predicts POS tags for input sentences with good accuracy.

## 📌 Conclusion
BERT provides strong performance for NLP sequence labeling tasks due to its contextual understanding.

