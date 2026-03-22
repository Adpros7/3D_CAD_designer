import os


def search(s):
    files = []
    for i in os.listdir(r"C:\Users\prani\Coding\AI\3D_CAD_designer\new\docs"):
        print(i)
        with open(
            rf"C:\Users\prani\Coding\AI\3D_CAD_designer\new\docs\{i}", encoding="utf-8"
        ) as f:
            if s in f.read():
                files.append(rf"C:/Users/prani/Coding/AI/3D_CAD_designer/new/docs/{i}")

    return files


if __name__ == "__main__":
    print(search("in"))
