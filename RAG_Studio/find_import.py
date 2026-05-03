try:
    from langchain.chains import RetrievalQA
    print("Found in langchain.chains")
except ImportError:
    try:
        from langchain_community.chains import RetrievalQA
        print("Found in langchain_community.chains")
    except ImportError:
        try:
            from langchain_classic.chains import RetrievalQA
            print("Found in langchain_classic.chains")
        except ImportError:
            print("RetrievalQA NOT FOUND anywhere!")
