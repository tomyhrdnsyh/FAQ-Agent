# ✨ Description Generator

This module is responsible for generating short semantic descriptions from LinkAja FAQ question-answer pairs. These descriptions are used to enhance vector embeddings for better semantic retrieval in the RAG system.

---

## 📌 Purpose

Given a Q&A pair, we use a Language Model (e.g. OpenAI GPT) to generate a concise **Bahasa Indonesia** sentence that summarizes the core information. This is useful for:

- Improving retrieval performance
- Capturing semantic meaning better than plain question text

---

## 📁 File Structure

```
preprocessing/
├── generate_description.py   # Main class-based description generator
├── prompt_template.py        # Prompt used to instruct the LLM
├── README.md                 # This file
```

---

## 🧠 Prompt Logic

The prompt is written in English but instructs the model to produce output in **Bahasa Indonesia**.

**Example Output:**
```json
{
  "question": "Bagaimana cara reset PIN?",
  "answer": "Masuk ke aplikasi lalu klik lupa PIN...",
  "description": "Panduan untuk mereset PIN akun LinkAja ketika pengguna lupa atau salah memasukkan PIN."
}
```

---

## ⚙️ How to Use

### Run as script:

```bash
export OPENAI_API_KEY=your_key_here
python -m preprocessing.generate_description
```

This will read from `data/faq.json` and write to `data/faq_preprocessed.json`.

### Use as a class:

```python
from preprocessing.generate_description import DescriptionGenerator

gen = DescriptionGenerator()
desc = gen.generate_description("Bagaimana cara ganti nomor?", "Kirim email ke support@linkaja.id...")
print(desc)
```

---

## 📦 Dependencies

Install from root `requirements.txt`, which should include:

- `openai`
- `tqdm`

---

## 🔐 Notes

- Make sure `OPENAI_API_KEY` is set in your environment variables.
- You can swap out OpenAI with another LLM provider by modifying the class.

---

## 🛠️ Next Steps

You can plug the descriptions into your embedding pipeline to compute more meaningful vector representations!