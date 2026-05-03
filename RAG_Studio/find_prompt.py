try:
    from langchain.prompts import PromptTemplate
    print("PromptTemplate: langchain.prompts")
except ImportError:
    try:
        from langchain_core.prompts import PromptTemplate
        print("PromptTemplate: langchain_core.prompts")
    except ImportError:
        print("PromptTemplate NOT FOUND!")
