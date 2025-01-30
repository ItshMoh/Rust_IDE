# LLM Code Generator 🚀

This project leverages a **Qwen2.5 Coder 7b model** to generate Rust projects based on user prompts. The generated code is automatically parsed and saved in a structured repository format.

## 📜 Project Overview

### 🔹 Features:
- Accepts user prompts to generate Rust projects.
- Automatically structures project files (`Cargo.toml`, `src/main.rs`, etc.).
- Saves the generated files in the repository.
- Ensures proper formatting and error handling.
**NOTE**
- Currently the rust compiler has not been integrated in the project for sending the errors to the llm again. 
- I am figuring out the best way to store the context for the fast retrieval for the qwen model.
---

## 🛠️ Setup & Installation

### 1️⃣ Prerequisites
- Python 3.7+ installed
- `pip` installed
- Rust installed (if testing generated projects)

### 2️⃣ Clone the Repository
```sh
git clone <your-repo-url>
pip install -r requirements.txt
python3 main.py

```
Here is the Video link for using it. [https://www.loom.com/share/bbc3d8bfb37a40e99b526dbbed61bd3c?sid=7fdbe2d6-eb09-4484-b02f-1dcf29bda3ce]
