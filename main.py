import ColeyAlgorithm
import ActivityCount

# load data from json in pandas


# coley("../clean_records/2/2LW152.json", "../clean_records/2/2RW298.json", "../clean_records/2/2ST151.json")
#ActivityCount.calculate("data/clean_records/2/2LW152.json", "data/clean_records/2/2RW298.json", "data/clean_records/2/2TR151.json", False)
#ActivityCount.calculate("data/clean_records/2/2LW152.json", "data/clean_records/2/2RW298.json", "data/clean_records/2/2TR151.json", False)

print("-----------------------")
ColeyAlgorithm.calculate("data/clean_records/1/1LW152.json", "data/clean_records/1/1RW298.json", "data/clean_records/1/1TR151.json", 76 - 3.9, 158.2 - 3.9)
# ColeyAlgorithm.calculate("data/clean_records/2/2LW152.json", "data/clean_records/2/2RW298.json", "data/clean_records/2/2TR151.json", 76 - 3.9, 158.2 - 3.9)
# ColeyAlgorithm.calculate("data/clean_records/2/2LW152.json", "data/clean_records/2/2RW298.json", "data/clean_records/2/2TR151.json", 345 - 3.9, 435.7 - 3.9)
