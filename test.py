from similarity import check_similarity, get_warning, get_top_match
from preprocessing import preprocess_text, word_count

print("=" * 50)
print("CONTENT SIMILARITY DETECTION SYSTEM — TEST SUITE")
print("=" * 50)

# ── TEST 1: High Similarity ──────────────────────────
print("\n📄 TEST 1: High Similarity Content")
print("-" * 40)
text1 = """Copyright law protects original creative works including 
written articles and blog posts. Unauthorized reproduction without 
attribution is a violation of intellectual property rights."""

status, results = check_similarity(text1)
if status == "success":
    print(f"Word Count : {word_count(text1)}")
    print(f"Status     : {status}\n")
    for doc, score in results:
        print(f"  {doc:20} {score}%")
    top_doc, top_score = get_top_match(results)
    print(f"\nTop Match  : {top_doc} ({top_score}%)")
    print(f"Warning    : {get_warning(top_score)}")


# ── TEST 2: Low Similarity ───────────────────────────
print("\n📄 TEST 2: Unrelated Content")
print("-" * 40)
text2 = "The weather outside is sunny and very beautiful today."

status, results = check_similarity(text2)
if status == "success":
    print(f"Word Count : {word_count(text2)}")
    for doc, score in results:
        print(f"  {doc:20} {score}%")
    top_doc, top_score = get_top_match(results)
    print(f"\nTop Match  : {top_doc} ({top_score}%)")
    print(f"Warning    : {get_warning(top_score)}")


# ── TEST 3: Empty Input ──────────────────────────────
print("\n📄 TEST 3: Empty Input")
print("-" * 40)
text3 = ""
status, results = check_similarity(text3)
print(f"Status: {status}")
print("System Response: Please enter some text before analyzing.")


# ── TEST 4: Too Short Input ──────────────────────────
print("\n📄 TEST 4: Too Short Input (1 word)")
print("-" * 40)
text4 = "copyright"
status, results = check_similarity(text4)
print(f"Status: {status}")
print("System Response: Please enter at least 3 words for meaningful comparison.")


# ── TEST 5: Only Punctuation ─────────────────────────
print("\n📄 TEST 5: Only Punctuation/Symbols")
print("-" * 40)
text5 = "!!! ??? @@@ ###"
status, results = check_similarity(text5)
print(f"Status: {status}")
print("System Response: No valid content detected after processing.")


# ── TEST 6: WIPO Related Content ─────────────────────
print("\n📄 TEST 6: WIPO / IP Related Content")
print("-" * 40)
text6 = """WIPO provides international frameworks for protecting copyright 
and trademarks. Digital content theft is a serious challenge for 
publishers worldwide."""

status, results = check_similarity(text6)
if status == "success":
    print(f"Word Count : {word_count(text6)}")
    for doc, score in results:
        print(f"  {doc:20} {score}%")
    top_doc, top_score = get_top_match(results)
    print(f"\nTop Match  : {top_doc} ({top_score}%)")
    print(f"Warning    : {get_warning(top_score)}")

print("\n" + "=" * 50)
print("ALL TESTS COMPLETE")
print("=" * 50)