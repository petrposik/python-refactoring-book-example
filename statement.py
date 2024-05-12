import json

PLAYS_DB_FPATH = "plays.json"
INVOICES_DB_FPATH = "invoices.json"


def read_json_file(filename):
    with open(filename) as f:
        return json.load(f)


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = [f'Statement for {invoice["customer"]}']
    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = 0
        match play["type"]:
            case "tragedy":
                this_amount = 40000
                if perf["audience"] > 30:
                    this_amount += 1000 * (perf["audience"] - 30)
            case "comedy":
                this_amount = 30000
                if perf["audience"] > 20:
                    this_amount += 10000 + 500 * (perf["audience"] - 20)
                this_amount += 300 * perf["audience"]
            case _:
                raise RuntimeError(f"unknown play type: {play.type}")

        # Add volume credits
        volume_credits += max(perf["audience"] - 30, 0)
        # Add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += perf["audience"] // 5

        result.append(
            f'  {play["name"]}: ${this_amount/100:,.2f} ({perf["audience"]} seats)'
        )
        total_amount += this_amount
    result.append(f"Amount owed is ${total_amount/100:,.2f}")
    result.append(f"You earned {volume_credits} credits")
    return "\n".join(result)


if __name__ == "__main__":
    plays = read_json_file(PLAYS_DB_FPATH)
    invoices = read_json_file(INVOICES_DB_FPATH)
    print(statement(invoices[0], plays))
