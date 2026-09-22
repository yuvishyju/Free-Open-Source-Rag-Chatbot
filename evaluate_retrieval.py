import csv
from modules.retriever import Retriever

# Initialize the retriever from your modules
retriever = Retriever()


def evaluate_retrieval():

    total_questions = 0
    answerable_count = 0
    no_answer_count = 0

    hits = 0
    correct_rejections = 0

    with open("evaluation/questions.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            question = row["question"]
            q_type = row["type"]
            expected_doc = row["expected_document"]
            expected_page = int(row["expected_page"])

            total_questions += 1

            print("\n" + "=" * 60)
            print(f"[{total_questions}] Question: {question}")
            print(f"Type: {q_type} | Target: {expected_doc} (Page {expected_page})")

            # 1. Search ChromaDB using your existing retriever
            results = retriever.search(question, top_k=4)

            # 2. Case A: Out-of-domain question (e.g., FIFA World Cup)
            if q_type == "no_answer":
                no_answer_count += 1
                if results is None:
                    correct_rejections += 1
                    print("✅ Correctly rejected: Out-of-domain question.")
                else:
                    print("❌ False positive: Retrieved chunks for an unrelated question.")
                continue

            # 3. Case B: Answerable question
            answerable_count += 1

            if results is None:
                print("❌ Failed: No documents met the similarity threshold.")
                continue

            # Check if ANY of the top 4 chunks came from the correct document and page
            metadatas = results["metadatas"][0]
            found_hit = False

            for i, meta in enumerate(metadatas):
                chunk_doc = meta["filename"]
                chunk_page = meta["page_number"]

                # Match document name and check if page is within +/- 1 page
                if chunk_doc == expected_doc and abs(chunk_page - expected_page) <= 1:
                    found_hit = True
                    print(f"✅ Hit at Rank {i + 1}! Found in {chunk_doc} on Page {chunk_page}")
                    break

            if found_hit:
                hits += 1
            else:
                print("❌ Miss: Relevant page not found in top 4 results.")

    # 4. Final summary calculation
    print("\n" + "=" * 60)
    print("FINAL EVALUATION RESULTS")
    print("=" * 60)
    print(f"Total questions tested: {total_questions}")
    print(f"Answerable questions: {answerable_count}")
    print(f"Out-of-domain questions: {no_answer_count}")
    print(f"Successful hits (correct doc & page): {hits}")
    print(f"Correct no-answer rejections: {correct_rejections}")

    if answerable_count > 0:
        hit_rate = (hits / answerable_count) * 100
        print(f"Retrieval Hit Rate: {hit_rate:.2f}%")

    if no_answer_count > 0:
        rejection_rate = (correct_rejections / no_answer_count) * 100
        print(f"No-Answer Rejection Rate: {rejection_rate:.2f}%")


if __name__ == "__main__":
    evaluate_retrieval()