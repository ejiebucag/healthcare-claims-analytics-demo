
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Configuration
RNG = random.Random(42)
NUMBER_OF_CLAIMS = 2000

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "data" / "synthetic" / "claims.csv"

CATEGORIES = [
    "Medical",
    "Surgical",
    "Maternity",
    "Emergency",
    "Outpatient",
]

DENIAL_REASONS = [
    "Incomplete documentation",
    "Invalid claim code",
    "Eligibility issue",
]

def generate_claims():
    records = []
    start_date = date(2025, 1, 1)

    for number in range(1, NUMBER_OF_CLAIMS + 1):
        claim_id = f"CLM-{number:06d}"

        submission_date = start_date + timedelta(
            days=RNG.randint(0, 364)
        )

        category = RNG.choice(CATEGORIES)

        status = RNG.choices(
            ["PAID", "DENIED", "PENDING"],
            weights=[65, 15, 20],
            k=1,
        )[0]

        submitted_amount = RNG.randrange(3000, 50001, 100)

        paid_amount = 0
        payment_date = ""
        denial_reason = ""

        if status == "PAID":
            paid_amount = round(
                submitted_amount * RNG.uniform(0.55, 0.95),
                2,
            )

            payment_date = (
                submission_date
                + timedelta(days=RNG.randint(5, 90))
            ).isoformat()

        elif status == "DENIED":
            denial_reason = RNG.choice(DENIAL_REASONS)

        records.append({
            "claim_id": claim_id,
            "category": category,
            "submission_date": submission_date.isoformat(),
            "submitted_amount": f"{submitted_amount:.2f}",
            "status": status,
            "payment_date": payment_date,
            "paid_amount": f"{paid_amount:.2f}",
            "denial_reason": denial_reason,
        })

    return records


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    claims = generate_claims()

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=claims[0].keys()
        )
        writer.writeheader()
        writer.writerows(claims)

    print(f"Generated {len(claims):,} synthetic claims")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
