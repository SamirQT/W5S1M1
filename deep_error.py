def fetch_records():
    # Simulates fetching raw text entries
    return [
        "user:1|score:100",
        "user:2|score:abc",
        "bad_format_record",
        "user:3|score:50"
    ]

def parse_record(record):
    # Expect format "user:<id>|score:<number>"
    parts = record.split("|")
    if len(parts) != 2:
        raise ValueError(f"Format error in '{record}'")
    u_part = parts[0].split(":")
    s_part = parts[1].split(":")
    if len(u_part) != 2 or len(s_part) != 2:
        raise ValueError(f"Parsing error in '{record}'")
    return u_part[1], s_part[1]

def process_records():
    users = []
    scores = []
    for rec in fetch_records():
        try:
            uid, raw_score = parse_record(rec)
            score = int(raw_score)            # may raise ValueError
        except ValueError as e:
            print(f"[Warning] Skipping record: {e}")
        else:
            users.append(uid)
            scores.append(score)
        finally:
            print(f"Finished processing: {rec}")
    # Compute total without returning anything
    total = 0
    for i in range(len(scores)):
        total += scores[i]
    print("Total score:", total)
