from langchain_community.document_loaders import WebBaseLoader


def extract_data(url):
    loader = WebBaseLoader(url)
    documents = loader.load()

    courses_data = [doc.page_content for doc in documents if doc.page_content.strip()]
    return courses_data


if __name__ == "__main__":
    url_actual = "https://brainlox.com/courses/category/technical"
    extracted_data = extract_data(url_actual)
    for course in extracted_data:
        print(course)
