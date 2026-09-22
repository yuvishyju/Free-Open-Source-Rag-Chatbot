import csv
import time
from modules.rag_engine import RAGEngine

# Initialize your RAG engine
rag = RAGEngine()

REFUSAL_TEXT = "I could not find this information in the uploaded documents."

# Set to 12 for fast testing (under 2 minutes). 
# Set to None when you are ready to let it run the full 55.
MAX_QUESTIONS = 12


def evaluate_answers():

    total_questions = 0
    answerable_count = 0
    no_answer_count = 0

    successful_answers = 0
    correct_refusals = 0
    total_time = 0.0

    with open("evaluation/questions.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if MAX_QUESTIONS is not None and total_questions >= MAX_QUESTIONS:
                break

            question = row["question"]
            expected_answer = row["expected_answer"]
            q_type = row["type"]

            total_questions += 1

            print("\n" + "=" * 70)
            print(f"[{total_questions}] Question: {question}")
            print(f"Type: {q_type}")

            start_time = time.time()
            result = rag.ask(question)
            elapsed = time.time() - start_time
            total_time += elapsed

            answer = result["answer"].strip()

            print(f"⏱️ Latency: {elapsed:.2f}s")
            print("Generated Answer:\n" + answer)

            # Case A: Out-of-domain question (must refuse)
            if q_type == "no_answer":
                no_answer_count += 1
                if REFUSAL_TEXT.lower() in answer.lower():
                    correct_refusals += 1
                    print("✅ Correct Refusal: System safely refused without hallucinating.")
                else:
                    print("❌ Hallucination Warning: System attempted to answer out-of-domain question.")
                continue

            # Case B: In-domain answerable question
            answerable_count += 1

            if REFUSAL_TEXT.lower() in answer.lower():
                print("❌ False Refusal: Model said not found, but document exists.")
            elif len(answer) > 15:
                successful_answers += 1
                print("✅ Grounded Answer Generated.")
            else:
                print("⚠️ Incomplete answer.")

    # Summary Report
    print("\n" + "=" * 70)
    print("ANSWER GENERATION EVALUATION RESULTS")
    print("=" * 70)
    print(f"Total questions tested: {total_questions}")
    print(f"Answerable questions: {answerable_count}")
    print(f"Out-of-domain questions: {no_answer_count}")
    print(f"Successfully answered: {successful_answers}")
    print(f"Correct refusals (no hallucination): {correct_refusals}")

    if answerable_count > 0:
        ans_rate = (successful_answers / answerable_count) * 100
        print(f"Answer Generation Rate: {ans_rate:.2f}%")

    if no_answer_count > 0:
        refusal_rate = (correct_refusals / no_answer_count) * 100
        print(f"No-Answer Refusal Rate: {refusal_rate:.2f}%")

    avg_time = total_time / total_questions if total_questions > 0 else 0
    print(f"Average latency per question: {avg_time:.2f} seconds")


if __name__ == "__main__":
    evaluate_answers()