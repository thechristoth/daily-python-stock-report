from datetime import datetime

with open("output.md", "w") as f:
    f.write(f"# Daily Report\n\nGenerated on {datetime.utcnow()} UTC\n")
    f.write("- Everything is running smoothly!\n")
