GENERATE_DESCRIPTION_PROMPT = """Your task is to create a short and concise description that summarizes the main topic of the following question and answer. The description should clearly explain the key information discussed, and be suitable for use as a semantic representation in a search system.

Output format: A single descriptive sentence in Bahasa Indonesia.

Example:
---
Question: Bagaimana cara reset dan buka blokir PIN?
Answer: Hai Sobat, bagaimana jika kamu lupa PIN? 
1. Log out dari aplikasi LinkAja kamu...
...
Description: Langkah-langkah yang dapat diambil pengguna LinkAja ketika lupa PIN atau ketika akun mereka terblokir karena salah memasukkan PIN lebih dari 3 kali.

Now, create a description for the following data:
---
Question: {question}
Answer: {answer}

Description:
"""