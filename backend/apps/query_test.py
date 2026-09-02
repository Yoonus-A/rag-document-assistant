from service.retriever import generate_answer


while True:
    query = input("\nAsk a question (or type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    result = generate_answer(query)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(
            f"Page {source['page']}, "
            f"distance: {source['distance']}"
        )