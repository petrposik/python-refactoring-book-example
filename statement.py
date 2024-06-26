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
        match play_for(performance)["type"]:
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

    def usd(cents: int) -> str:
        return f"{cents/100:,.2f}"

    def total_volume_credits(invoice):
        return sum(volume_credits_for(perf) for perf in invoice["performances"])

    def total_amount(invoice):
        return sum(amount_for(perf) for perf in invoice["performances"])

    # Main statement body
    result = [f'Statement for {invoice["customer"]}']
    for perf in invoice["performances"]:
        result.append(
            f'  {play_for(perf)["name"]}: ${usd(amount_for(perf))}'
            f' ({perf["audience"]} seats)'
        )
    result.append(f"Amount owed is ${usd(total_amount(invoice))}")
    result.append(f"You earned {total_volume_credits(invoice)} credits")
    return "\n".join(result)


if __name__ == "__main__":
    plays = read_json_file(PLAYS_DB_FPATH)
    invoices = read_json_file(INVOICES_DB_FPATH)
    for invoice in invoices:
        print(statement(invoice, plays))
        print("----------------------")
