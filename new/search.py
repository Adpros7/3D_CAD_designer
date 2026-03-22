import os


def search(s):
    files = {}
    for i in os.listdir(r"C:\Users\prani\Coding\AI\3D_CAD_designer\new\docs"):
        with open(
            rf"C:\Users\prani\Coding\AI\3D_CAD_designer\new\docs\{i}", encoding="utf-8"
        ) as f:
            if s in f.read():
                files.update(
                    {
                        rf"C:/Users/prani/Coding/AI/3D_CAD_designer/new/docs/{i}": len(f.read().split(
                            s
                        ))
                    }
                )

    return files


if __name__ == "__main__":
    print(search("armature"))
