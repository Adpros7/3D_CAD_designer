import os

for i in os.listdir(r'C:\Users\prani\Coding\AI\3D_CAD_designer\new\blender_python_reference_5_1'):
    print(i)
    with open(f'C:/Users/prani/Coding/AI/3D_CAD_designer/new/blender_python_reference_5_1/{i}', 'r', encoding="utf-8") as f:
        data = f.read()
        start = data.find('<article role="main" id="furo-main-content">')
        end = data.find("</article>")
        data = data[start:end]
        extracted = ""
        extractedFlag = False
        for j in data:
            if j == ">":
                extractedFlag = True

            elif j == "<":
                extractedFlag = False

            elif extractedFlag:
                extracted += j

            with open(f'C:/Users/prani/Coding/AI/3D_CAD_designer/new/docs/{i}', 'w') as f:
                f.write(extracted.replace("¶", "").replace("\n\n", "\n"))
