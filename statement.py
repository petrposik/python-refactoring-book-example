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

    def amount_for(performance: Performance) -> int:
        """Compute the 100*amount for a performance."""
        result = 0
        match play_for(perf)["type"]:
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
                raise RuntimeError(f'unknown play type: {play_for(perf)["type"]}')
        return result

    def volume_credits_for(performance: Performance) -> int:
        result = max(performance["audience"] - 30, 0)
        if "comedy" == play_for(performance)["type"]:
            result += performance["audience"] // 5
        return result

    total_amount: int = 0
    volume_credits: int = 0
    result = [f'Statement for {invoice["customer"]}']
    for perf in invoice["performances"]:
        volume_credits += volume_credits_for(perf)
        result.append(
            f'  {play_for(perf)["name"]}: ${amount_for(perf)/100:,.2f}'
            f' ({perf["audience"]} seats)'
        )
        total_amount += amount_for(perf)
    result.append(f"Amount owed is ${total_amount/100:,.2f}")
    result.append(f"You earned {volume_credits} credits")
    return "\n".join(result)


if __name__ == "__main__":
    plays = read_json_file(PLAYS_DB_FPATH)
    invoices = read_json_file(INVOICES_DB_FPATH)
    for invoice in invoices:
        print(statement(invoice, plays))
        print("----------------------")
