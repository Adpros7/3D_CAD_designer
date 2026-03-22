import os


def search(s, n=5):
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

    print(search("bpy"))
