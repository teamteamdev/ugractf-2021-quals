import sqlite3

numbers = {}
ids = set()

with sqlite3.connect("oeis.sqlite") as db:
    db.execute("CREATE TABLE IF NOT EXISTS seq_items (number int not null, id int not null)")
    db.execute("CREATE TABLE IF NOT EXISTS seq (id int not null, desc varchar(512) not null)")
    db.commit()

    with open("stripped") as numbers_file:
        for line in numbers_file:
            if not line.startswith("A"):
                continue

            seqid, seq = line.split()
            seqid = int(seqid[1:], 10)

            for item in map(int, seq.split(',')[1:-1]):
                if not 1000 <= item <= 9999:
                    continue

                numbers.setdefault(item, set())
                if len(numbers[item]) < 10:
                    db.execute("INSERT INTO seq_items VALUES (?, ?)", (item, seqid))
                    numbers[item].add(seqid)
                    ids.add(seqid)

    with open("names") as names_file:
        for line in names_file:
            if not line.startswith("A"):
                continue

            seqid = line[:7]
            name = line[8:]
            seqid = int(seqid[1:], 10)

            if seqid in ids:
                db.execute("INSERT INTO seq VALUES (?, ?)", (seqid, name))
