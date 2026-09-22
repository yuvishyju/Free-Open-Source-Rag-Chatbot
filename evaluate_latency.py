import csv
import time

from modules.rag_engine import RAGEngine


rag = RAGEngine()


def evaluate_latency():

    response_times = []

    with open(
        "evaluation/questions.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            question = row["question"]

            print("\n" + "=" * 60)
            print("Question:", question)

            start_time = time.time()

            result = rag.ask(question)

            end_time = time.time()

            response_time = end_time - start_time

            response_times.append(response_time)

            print(
                "Response time:",
                f"{response_time:.2f} seconds"
            )

    average_time = sum(response_times) / len(response_times)

    fastest_time = min(response_times)
    slowest_time = max(response_times)

    print("\n" + "=" * 60)
    print("LATENCY RESULTS")
    print("=" * 60)

    print(
        "Average response time:",
        f"{average_time:.2f} seconds"
    )

    print(
        "Fastest response:",
        f"{fastest_time:.2f} seconds"
    )

    print(
        "Slowest response:",
        f"{slowest_time:.2f} seconds"
    )


if __name__ == "__main__":
    evaluate_latency()
    