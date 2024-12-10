
from pwn import asm

def generate_payload(technique_id):
    shellcode = asm(f"mov rax, {technique_id}; ret")
    return shellcode.hex()

def process_techniques(input_techniques, all_techniques):
    payload_results = []
    for tech in input_techniques:
        tech_data = next(
            (t for t in all_techniques if t['name'].lower() == tech.lower()), None
        )
        if tech_data:
            payload = generate_payload(tech_data['technique_id'])
            payload_results.append({
                "Technique": tech,
                "Description": tech_data['description'],
                "Payload": payload,
                "ID": tech_data['technique_id']
            })
        else:
            payload_results.append({
                "Technique": tech,
                "Description": "Not Found",
                "Payload": "N/A",
                "ID": "N/A"
            })
    return payload_results
