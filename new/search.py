import os

from easier_openai import Assistant

assistant = Assistant()

@assistant.openai_function
def search(s, n=5):# -> list[tuple[Any, Any]]:
    """
    Search for a term in blender documentation.

    Example:
    >>> search("bmesh")
    [("C:/Users/bob/Downloads/docs/bmesh.md", 3)]
    Args:
        s (str): The term to search for.
        n (int, optional): The number of results to return. Defaults to 5.

    Returns:
        list: A list of tuples containing the file path and the number of occurrences of the term in the file.


    """
    files = {}
    for i in os.listdir(r"C:\Users\prani\Coding\AI\3D_CAD_designer\new\docs"):
        with open(
            rf"C:\Users\prani\Coding\AI\3D_CAD_designer\new\docs\{i}", encoding="utf-8"
        ) as f:
            content = f.read()
            if s in content:
                files.update(
                    {
                        rf"C:/Users/prani/Coding/AI/3D_CAD_designer/new/docs/{i}": content.count(s)
                    }
                )

    return sorted(files.items(), key=lambda x: x[1], reverse=True)[:n]


if __name__ == "__main__":

    print(search("bmesh"))
