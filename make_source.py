# Writes ~500 lines to source.txt (250 assigns + 250 prints)
with open("source.txt", "w") as f:
    for i in range(1, 251):
        f.write(f"x{i} = {i} + {i+1} - 1;\n")
        f.write(f"print x{i};\n")
print("source.txt written with ~500 lines.")
