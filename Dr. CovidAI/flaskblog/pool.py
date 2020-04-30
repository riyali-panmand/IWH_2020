import random
# import Dataset as ds
from flaskblog import poolData
from flaskblog import DoctorData as doctor 

FILTER_THRESHOLD_PERC = 30
POOL_BUFFER_SIZE = 10
POOL_SIZE = 5


def filterData(Data):
    filteredData = {}
    for entry in Data:
        if Data[entry]["probability"] >= FILTER_THRESHOLD_PERC:
            filteredData[entry] = Data[entry]
    print("Filtered Data has length: ", len(filteredData))
    return filteredData


def locSort(filteredData):
    locData = {}
    for entry in filteredData:
        currentLocation = filteredData[entry]["location"]
        currentProb = filteredData[entry]["probability"]
        if currentLocation not in locData:
            locData[currentLocation] = {}
        locData[currentLocation][entry] = currentProb
    # print("Data sorted based on location: ",  locData)
    return locData


def genPools(poolData):
    Pools = []
    if len(poolData) < POOL_BUFFER_SIZE:
        return Pools
    else:
        idList = [id for id in poolData]
        numPools = len(idList)//POOL_SIZE
        chosenIdList = random.sample(
            idList, k=(numPools * POOL_SIZE))

        def sortId(id):
            return poolData[id]
        sortedIdList = sorted(chosenIdList, key=sortId)

        for _ in range(0, numPools):
            Pools.append([])

        for index, id in enumerate(sortedIdList):
            x = sortedIdList[index]
            Pools[index % numPools].append(x)
            # print(index, index % POOL_SIZE, id)
        return Pools


def main():
    # Data = ds.Data
    Data = poolData.Data
    filteredData = filterData(Data)
    locData = locSort(filteredData)
    Pools = []

    for location in locData:
        locPools = genPools(locData[location])
        Pools.extend(locPools)
        # print(Pools, location)

    # print(Pools)
    for poolIndex, Pool in enumerate(Pools):
        print(f'Pool {poolIndex+1}:')
        for id in Pool:
            print(filteredData[id])

    return Pools


def add_to_dataset(Location, Probability):
    Data = poolData.Data
    id = random.randint(10000, 60000)

    while(id_present(id)):
        id = random.randint(10000, 60000)

    print(id)

    Data[str(id)] = {
        "location": str(Location),
        "probability": int(Probability)
    }

    outFile = open("poolData.py","w")
    outFile.write("Data = " + (str(Data)))
    outFile.close()

    print("Data added")

def id_present(id):
    Data = poolData.Data
    id = str(id)

    for userId in Data.keys():
        if userId == id:
            return True
            break

    return False

def fetch_pool_batch(Pools, userId):
    print("\n\n------------------------------------------------------")
    print(Pools)

    userBatch = []
    Data = poolData.Data
    Doctor = doctor.Doctors

    user_pool_details = []

    for batch in Pools:
        if str(userId) in batch:
            userBatch = batch 

    print(userBatch)

    for id in userBatch:
        user_details = []
        for key in Data.keys():
            if key == id:
                user_details.append(str(id))
                user_details.append(Data[key]["location"])
                user_details.append(Data[key]["probability"])

        for docs in Doctor.keys():
            if Doctor[docs]["location"] == Data[key]["location"]:
                user_details.append(Doctor[docs]["name"])
                user_details.append(Doctor[docs]["hospital"])

        user_pool_details.append(user_details)

    # print(user_pool_details)
    return user_pool_details


# if __name__ == '__main__':
#     # add_to_dataset("Powai", 80)
#     main()
