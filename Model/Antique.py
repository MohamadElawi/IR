class Antique:

    def __init__(self, id, content):
        self.id = id
        self.content = content

    @staticmethod
    def parse_all(file):

        antiques = []
        for line in file:
                data = line.strip().split("\t")
                id = data[0]
                content = data[1]
                # print(id , content)
                antique = Antique(id, content)
                # print(antique)
                antiques.append(antique)
        # print(antiques)
        return antiques


def save_antiques_to_file(antiques, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for antique in antiques:
            f.write(f"{antique.id}\t{antique.content}\n")






