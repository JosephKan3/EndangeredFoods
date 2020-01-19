import json
import requests
from flask import Flask
from datetime import datetime
from expiryDate import checkExpiries, findExpiryTime

def readFile():
    with open('dataStorage.txt', 'r+', encoding="utf-8") as f:
        foodList = []
        for line in f:
            foodList.append(eval(line))
        return foodList

def removeFood(name, quantity):
    open("dataStorage.txt", "w", encoding="utf-8")
    with open('dataStorage.txt', 'r+', encoding="utf-8") as f:
        foodList = []
        for line in f:
            foodList.append(eval(line))
        for food in foodList:
            if food[0] == name:
                newQuant = int(food[2]) - quantity
                indexPos = foodList.index(food)
                if newQuant > 0:
                    foodList[indexPos] = [food[0], food[1], newQuant, food[3], food[4]]
                else:
                    del foodList[indexPos]
            else:
                continue
    o = open("dataStorage.txt", "w", encoding="utf-8")
    for food in foodList:
        o.write(str(food) + "\n")

def addFood(file):
    #[[name, date, quantity, calories]]
    currentFile = open("dataStorage.txt", "r+", encoding="utf-8")
    currentDataList = []
    tempDataList = []
    for entry in currentFile.readlines():
        finalList = []
        entryList = entry.split(",")
        for listPart in entryList:
            finalList.append(listPart.strip("[]\' \n"))  
        tempDataList.append(finalList)
        updateFile = open(str(file), "r", encoding="utf-8")
    updateData = json.load(updateFile)
    for food in updateData["entries"]:
        entry = [food["name"], food["date"], food["quantity"], food["calories"], food["pic"]]
        terminate = False
        for listValue in tempDataList:
            if entry[0] == listValue[0]:
                terminate = True
                break
            else:
                continue
        if terminate:
            continue
        else:
            currentDataList.append(entry)
    with open("dataStorage.txt", "a", encoding="utf-8") as myFile:
        for update in currentDataList:
            myFile.write(str(update)+"\n")

def expiryList():
    foodList = readFile() 
    outputDic = {'entries': []}
    for food in foodList:
        if checkExpiries(food[1]):
            entryDic = {'name': food[0], 'date': food[1], 'quantity': food[2], 'calories': food[3], 'pic': food[4]}
            outputDic['entries'].append(entryDic)
            jsonOut = json.dumps(outputDic)
    return(jsonOut)

def limitedTimeFoods():
    foodList = readFile()
    outputDic = {'entries': []}
    for food in foodList:
        if checkExpiries(food[1]):
            entryDic = {'name': food[0], 'timeLeft': 'Expired'}
        else:
            entryDic = {'name': food[0], 'timeLeft': findExpiryTime(food[1])}
        outputDic['entries'].append(entryDic)
        jsonOut = json.dumps(outputDic)
    return(jsonOut)

addFood("response3.txt")

#ingredients="apples,+pineapple" 
#I NEED THE INGREDIENTS IN THE ABOVE FORMAT
def getRecipe(ingredients):
    response = requests.get("https://api.spoonacular.com/recipes/findByIngredients?apiKey=50bc728be7ce4ce2a00c793ff7baa63e&ingredients="+ingredients+"&number=1&ignorePantry=true")
    recipeData=[response.json()[0]['title']]+[response.json()[0]['image']]+[response.json()[0]['usedIngredientCount']]
    recipeDataTheOtherHalf=[]
    for x in response.json()[0]['usedIngredients']:
        recipeDataTheOtherHalf+=[x['originalName']]
    recipeData+=[recipeDataTheOtherHalf]
    return recipeData
#IT WILL RETURN ['RECIPE NAME','IMAGE',#_OF_INGREDIENTS_USED,['INGREDIENTS1','INGREIDENT2']]
