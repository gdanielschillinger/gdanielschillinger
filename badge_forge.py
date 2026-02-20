def generate_nfc_payload(recruiter_name="GUEST"):
    portfolio_url = f"https://your-portfolio-link.vercel.app?ref=NFC_{recruiter_name}"
    
    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:Schillinger;Daniel;;;
FN:Daniel Schillinger
ORG:Sentient Sync AI;
TITLE:Cyber-AI Architect / ex-Visa AI Ambassador
URL:{portfolio_url}
END:VCARD"""

    with open(f"nfc_payload_{recruiter_name}.txt", "w") as f:
        f.write(vcard)
    
    print(f"[+] NFC Payload forged for {recruiter_name}. Encode this to your NTAG216 via Pixel 10.")

if __name__ == "__main__":
    generate_nfc_payload("EMERGE_AMERICAS_2026")
