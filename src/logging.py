from datetime import datetime


def write_log(ip, query, code):
    f = open(f"logs/{datetime.now().date()}.txt", "a")
    f.write(f"{ip} -{code}- [{datetime.now()}] \"{query}\"\n")
