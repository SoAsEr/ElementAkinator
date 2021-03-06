
from random import randint
from string import ascii_lowercase
# Define constants
# if 0, converges as quickly as possible
AVGNUMBEROFQUESTIONS = 0
# describes block of periodic table
periodicShapePeriod = ([1] * 2) + ([2] * 8) + \
    ([3] * 8) + ([4] * 18) + ([5] * 18) + ([6] * 18) + ([7] * 18)
periodicShapeFamily = [
    1, 18] + (([1, 2] + list(range(13, 19))) * 2) + (list(range(1, 19)) * 4)
# first I need to define the names (numbers (row, period))
elementNames = ["Hydrogen", "Helium", "Lithium", "Beryllium"]
elementNames += ["Boron", "Carbon", "Nitrogen", "Oxygen", "Fluorine", "Neon", "Sodium", "Magnesium", "Aluminum", "Silicon",
                 "Phosphorus", "Sulfur", "Chlorine", "Argon", "Potassium", "Calcium", "Scandium", "Titanium", "Vanadium", "Chromium"]
elementNames += ["Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc", "Gallium", "Germanium", "Arsenic", "Selenium", "Bromine", "Krypton",
                 "Rubidium", "Strontium", "Yttrium", "Zirconium", "Niobium", "Molybdenum", "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver"]
elementNames += ["Cadmium", "Indium", "Tin",
                 "Antimony", "Tellurium", "Iodine", "Xenon", "Cesium","Barium","Lanthanum","Hafnium","Tantalum","Tungsten","Rhenium","Osmium","Iridium","Platinum","Gold","Mercury","Thallium","Lead","Bismuth","Polonium","Astatine","Radon","Francium","Radium"]
elementNames+=["Actinium","Rutherfordium","Dubnium","Seaborgium","Bohrium","Hassium","Meitnerium","Darmstadtium","Roentgenium","Ununbium"]
elementNames+=["Ununtrium","Ununquadium","Ununpentium","Ununhexium","Ununseptium","Ununoctium"]


def atomicNumberToElectronConfig(i):
    electronConfig = ""
    if(i == 1):
        electronConfig = "1s1"
        return electronConfig
    else:
        electronConfig = "1s"
    currentPeriod = 2
    currentFamily = 1
    runningBlockCounter = 1
    currentBlock = ""
    j = 2
    while(j < i):
        if (j==57):
            electronConfig+=str(currentPeriod-2)+"f14 "
        if(periodicShapeFamily[j] == 1):
            electronConfig += str(runningBlockCounter + 1) + " "
            runningBlockCounter = 0
            electronConfig += str(periodicShapePeriod[j]) + "s"
        elif (periodicShapeFamily[j] == 3):
            electronConfig += str(runningBlockCounter + 1) + " "
            runningBlockCounter = 0
            electronConfig += str(periodicShapePeriod[j] - 1) + "d"
        elif (periodicShapeFamily[j] == 13):
            electronConfig += str(runningBlockCounter + 1) + " "
            runningBlockCounter = 0
            electronConfig += str(periodicShapePeriod[j]) + "p"
        else:
            runningBlockCounter += 1
        j += 1
    if(periodicShapeFamily[j-1] == 6):
        electronConfig = electronConfig[:-6]
        electronConfig += str(currentPeriod) + "s1 " + \
            str(currentPeriod - 1) + "d5 "
    elif(periodicShapeFamily[j-1] == 11):
        electronConfig = electronConfig[:-6]
        electronConfig += str(currentPeriod) + "s1 " + \
            str(currentPeriod - 1) + "d10 "
    else:
        electronConfig += str(runningBlockCounter + 1) + " "
    return electronConfig


def eliminate(remainingElementDictionaries, field, questionParam, condition):
    newDic = remainingElementDictionaries.copy()
    for i in range(0, len(remainingElementDictionaries)):

        if((str.lower(str(questionParam)) in str.lower(str(remainingElementDictionaries[i][field]))) != condition):
            for j in range(0, len(newDic)):
                if(newDic[j]["name"] == remainingElementDictionaries[i]["name"]):
                    newDic.pop(j)
                    break
    return newDic

# hell yeah, copy pasted quicksort code


def partition(arr, low, high):
    i = (low - 1)         # index of smaller element
    pivot = arr[high][2]     # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if arr[j][2] <= pivot:

            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index

# Function to do Quick sort


def quickSort(arr, low, high):
    if low < high:

        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


def getIdealQuestion(questionsLeft, remainingElementDictionaries):
    electronConfigPossibilites = []
    for i in range(1, 6):
        for j in range(1, 3):
            electronConfigPossibilites += [[str(i) + "s" + str(j) + " ", 0]]
        if(2 <= i):
            for j in range(1, 7):
                electronConfigPossibilites += [
                    [str(i) + "p" + str(j) + " ", 0]]
        if(3 <= i <= 4):
            for j in range(1, 11):
                electronConfigPossibilites += [
                    [str(i) + "d" + str(j) + " ", 0]]
    possibleQuestions = []
    numOfExceptions = 0
    family = [0 for i in range(18)]
    period = [0 for i in range(7)]
    atomic = [0 for i in range(10)]
    letters = [0 for i in range(26)]
    for elem in remainingElementDictionaries:
        possibleQuestions += [["name",
                               elem["name"], 1]]
        if(elem["exceptionToConfigRules"]):
            numOfExceptions += 1
        family[elem["family"] - 1] += 1
        period[elem["period"] - 1] += 1
        for j in range(0, len(electronConfigPossibilites)):
            if((electronConfigPossibilites[j][0]) in elem["electronConfig"]):
                electronConfigPossibilites[j][1] += 1
        for j in range(0, 10):
            if(str(j + 1) in elem["atomicNumber"]):
                atomic[j] += 1
        for j in range(0, 26):
            if(ascii_lowercase[j] in elem["name"]):
                letters[j] += 1

    # no zero check because info gain below takes care of it and it's more readable this way
    possibleQuestions += [["exceptionToConfigRules", True, numOfExceptions]]
    for i in range(0, 18):
        possibleQuestions += [["family", i + 1, family[i]]]

    for i in range(0, 5):
        possibleQuestions += [["period", i + 1, period[i]]]

    for elem in electronConfigPossibilites:
        possibleQuestions += [["electronConfig",
                               elem[0], elem[1]]]

    for i in range(0, 10):
        possibleQuestions += [["atomicNumber", i + 1, atomic[i]]]

    for i in range(0, 26):
        possibleQuestions += [["name", ascii_lowercase[i], letters[i]]]

    # turn number of positives into average element elimination
    for elem in possibleQuestions:
        posAnswerProb = float(
            elem[2]) / len(remainingElementDictionaries)
        negAnswerProb = 1 - posAnswerProb
        posAnswerNumberOfEliminatedResponses = len(
            remainingElementDictionaries) - elem[2]
        negAnswerNumberOfEliminatedResponses = elem[2]
        averageEliminatedResponses = (posAnswerProb * posAnswerNumberOfEliminatedResponses) + (
            negAnswerProb * negAnswerNumberOfEliminatedResponses)
        elem[2] = averageEliminatedResponses
    i2 = 0
    while(i2 < len(possibleQuestions)):
        if(possibleQuestions[i2][2] == 0):
            possibleQuestions.pop(i2)
        else:
            i2 += 1

    quickSort(possibleQuestions, 0, len(possibleQuestions) - 1)
    # print(possibleQuestions)
    if(questionsLeft > 1):
        idealQuestionNumber = len(remainingElementDictionaries) * \
            pow(1 / len(remainingElementDictionaries), 1 / questionsLeft)
        bestValueIndex = 0
        for i in range(0, len(possibleQuestions)):
            if(possibleQuestions[i][2] > idealQuestionNumber):
                if(abs(possibleQuestions[i][2] - idealQuestionNumber) < abs(possibleQuestions[i - 1][2] - idealQuestionNumber)):
                    bestValueIndex = i
                else:
                    bestValueIndex = i - 1
                break
    else:
        bestValueIndex = len(possibleQuestions) - 1

    allWithBestValue = [possibleQuestions[bestValueIndex]]
    for i in range(0, bestValueIndex):
        if(possibleQuestions[i][2] == possibleQuestions[bestValueIndex][2]):
            allWithBestValue += [possibleQuestions[i]]
    for elem in allWithBestValue:
        if(elem[0] == "name" and (len(elem[1]) > 1)):
            return elem[0], elem[1]
    priorities = ["exceptionToConfigRules", "electronConfig",
                  "period", "atomicNumber", "family", "name"]
    b = None
    for elem in priorities:
        for elem2 in allWithBestValue:
            if(elem2[0] == elem):
                b = elem
            if(b != None):
                break
        if(b != None):
            break
    if(b in priorities):
        i2 = 0
        while(i2 < len(allWithBestValue)):
            if(allWithBestValue[i2][0] != b):
                allWithBestValue.pop(i2)
            else:
                i2 += 1

    result = allWithBestValue[randint(0, len(allWithBestValue) - 1)]
    return result[0], result[1]


def getQuestion(category, param):
    if(category == "name"):
        if(len(param) > 1):
            return "Is your element " + str(param) + "?"
        else:
            return "Does your element's name contain a " + str(param) + "?"
    if(category == "exceptionToConfigRules"):
        return "Is your element an exception to the normal electron configuration rules?"
    if(category == "electronConfig"):
        return "Does your element contain " + str(param) + " in it's electron configuration?"
    if(category == "family"):
        return "Is your element in family " + str(param) + "?"
    if(category == "period"):
        return "Is your element in period " + str(param) + "?"
    if(category == "atomicNumber"):
        return "Does your element's atomic number contain a " + str(param) + "?"


def main():
    numOfQuestionsAsked = 0
    remainingElementDictionaries = []
    for i in range(0, len(elementNames)):
        atomicNum=i+1
        if(i>57):
            atomicNum+=14
        if(i>89):
            atomicNum+=14
        tempDic = {
            "name": elementNames[i],
            "electronConfig": atomicNumberToElectronConfig(i + 1),
            "exceptionToConfigRules": (periodicShapeFamily[i] == 6 or periodicShapeFamily[i] == 11),
            "transitionMetal": (periodicShapeFamily[i] in list(range(3, 13))),
            "atomicNumber": str(atomicNum),
            "family": periodicShapeFamily[i],
            "period": periodicShapePeriod[i]
        }
        if(i == 1):
            tempDic["family"] = 18
        remainingElementDictionaries.append(tempDic)


    print("Is your element a transition metal? y/n")
    numOfQuestionsAsked += 1
    remainingElementDictionaries = eliminate(
        remainingElementDictionaries, "transitionMetal", True, input() == "y")

    while(len(remainingElementDictionaries) > 1):
        print()
        print("Possible Elements:")
        for i in range(0, len(remainingElementDictionaries) - 1):
            print(remainingElementDictionaries[i]["name"], end=', ')
        print(remainingElementDictionaries[len(
            remainingElementDictionaries) - 1]["name"])
        print()
        questionCategory, questionParam = getIdealQuestion(
            AVGNUMBEROFQUESTIONS - numOfQuestionsAsked, remainingElementDictionaries)
        print(getQuestion(questionCategory, questionParam) + " y/n")
        remainingElementDictionaries = eliminate(
            remainingElementDictionaries, questionCategory, questionParam, input() == "y")
    print("Your element is: " + remainingElementDictionaries[0]["name"])


main()
