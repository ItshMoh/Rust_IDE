# LLM Code Generator 🚀

This project leverages a **DeepSeek R1 Distill Llama 70B** to generate Rust projects based on user prompts. The generated code is automatically parsed and saved in a structured repository format.

## 📜 Project Overview

### 🔹 Features:
- Accepts user prompts to generate Rust projects.
- Automatically structures project files (`Cargo.toml`, `src/main.rs`, etc.).
- Saves the generated files in the repository.
- Ensures proper formatting and error handling.

**NOTE**

- The rust compiler is being integrated into this project.So now it sends error back to the llm and model iterates over the code and fix the errors.
- It is not performing very good on complex project.
---

## 🛠️ Setup & Installation

### 1️⃣ Prerequisites
- Python 3.7+ installed
- `pip` installed
- Rust installed (if testing generated projects)
- A mongo database.

### 2️⃣ Executing the project
```sh
git clone <https://github.com/ItshMoh/Rust_IDE.git>
pip install -r requirements.txt
cd src
cp .env.example .env
cd ..
python3 main.py

```
Here is the Video link for using it. [https://www.loom.com/share/34958ed9dc8145ae81d6ee8f49b563bc?sid=71e14109-bed4-4455-b70c-878be62a1fda]
