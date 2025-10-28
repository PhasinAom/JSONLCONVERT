import pandas as pd
import json

# ---- SETTINGS ----
csv_file = "test_FamBear_chatbot_finetune - Sheet1.csv"  # input file (.csv or .xlsx)
jsonl_file = "FamBear_chatbot_data.jsonl"  # output file, you can change the name

# ---- LOAD CSV ----
if csv_file.endswith(".xlsx"):
    df = pd.read_excel(csv_file)
else:
    df = pd.read_csv(csv_file)

df.columns = df.columns.str.strip()

# ---- BUILD JSONL ----
with open(jsonl_file, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        user_prompt = str(row.get("user_prompt", "")).strip()
        assistant_response = str(row.get("assistant_response", "")).strip()
        intent = str(row.get("Example of intent", "")).strip()

        user_type = str(row.get("User Type", "")).strip()
        service_type = str(row.get("Service Type", "")).strip()
        notes = str(row.get("notes", "")).strip()
        tone = str(row.get("Tone/Voice", "Friendly and Approachable")).strip()

        metadata = {
            "User Type": user_type,
            "Service Type": service_type,
            "notes": notes,
            "Tone/Voice": tone
        }
        
        # ---- CHANGE IS HERE ----
        # 1. Create a dictionary for the assistant's content
        assistant_content = {
            "intent": intent,
            "response": assistant_response
        }

        messages = [
            {"role": "system", "content": f"metadata: {json.dumps(metadata, ensure_ascii=False)}"},
            {"role": "user", "content": user_prompt},
            # 2. Convert that dictionary to a JSON string for the 'content' field
            {"role": "assistant", "content": json.dumps(assistant_content, ensure_ascii=False)}
        ]

        f.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")

print("✅ Conversion complete. JSONL saved to", jsonl_file)
