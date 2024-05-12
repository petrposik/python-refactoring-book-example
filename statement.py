import json

PLAYS_DB_FPATH = "plays.json"
INVOICES_DB_FPATH = "invoices.json"

Play = dict[str, str]
Performance = dict[str, str | int]
Invoice = dict[str, str | list[Performance]]


def read_json_file(filename):
    with open(filename) as f:
        return json.load(f)


def statement(invoice: Invoice, plays: list[Play]) -> str:

    def play_for(performance: Performance) -> Play:
        return plays[performance["playID"]]

    def amount_for(performance: Performance, play: Play) -> int:
        """Compute the 100*amount for a performance."""
        result = 0
        match play["type"]:
            case "tragedy":
                result = 40000
                if performance["audience"] > 30:
                    result += 1000 * (performance["audience"] - 30)
            case "comedy":
                result = 30000
                if performance["audience"] > 20:
                    result += 10000 + 500 * (performance["audience"] - 20)
                result += 300 * performance["audience"]
            case _:
                raise RuntimeError(f"unknown play type: {play.type}")
        return result

    total_amount: int = 0
    volume_credits: int = 0
    result = [f'Statement for {invoice["customer"]}']
    for perf in invoice["performances"]:
        play = play_for(perf)
        this_amount = amount_for(perf, play)

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
    for invoice in invoices:
        print(statement(invoice, plays))
        print("----------------------")
