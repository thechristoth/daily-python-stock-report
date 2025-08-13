import datetime

current_date = datetime.date.today().strftime("%B %d, %Y")
with open("index.html", "a") as f:
    f.write(f"<h2>Updated content at 16:00 Budapest on this date: {current_date}.</h2>")
