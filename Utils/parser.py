from Model.Antique import Antique


def parse_train_data():
    all_antique = []

    train_data_files = ["resources/antique/collection-all.tsv", "resources/wikIR1k/documents-new.tsv"]
    for file_path in train_data_files:
        f = open(file_path, "r", encoding="utf-8")
        all_antique.extend(Antique.parse_all(f))
    return all_antique


def parse_test_data():
    queries = []
    test_data_files = ["resources/antique/test/queries.txt", "resources/wikIR1k/validation/queries-new.csv"]


    for file_path in test_data_files:
        f = open(file_path, "r", encoding="utf-8")
        queries.extend(Antique.parse_all(f))

    return queries


def parse_relevant_dic():
    qrles_files = ["resources/antique/test/qrels", "resources/wikIR1k/validation/qrels"]  #

    relevant_dic = {}
    for file_path in qrles_files:
        f = open(file_path, "r")
        for line in f:
            split = line.split(" ")
            if len(split[0]) == 0:
                continue
            id = int(split[0])
            related_id = split[2]
            # print(related_id)
            if id not in relevant_dic:
                relevant_dic[id] = []
            relevant_dic[id].append(related_id)
    return relevant_dic



