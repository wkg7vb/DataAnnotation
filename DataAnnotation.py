#imports
import codecs
import os
import requests
import sys
from pyparsing import empty

testUrl = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
url = "https://docs.google.com/document/d/e/2PACX-1vShuWova56o7XS1S3LwEIzkYJA8pBQENja01DNnVDorDVXbWakDT4NioAScvP1OCX6eeKSqRyzUW_qJ/pub"

#obtain file from url
def download_file_from_google_drive(url, file_id, destination):
    session = requests.Session()

    response = session.get(URL, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def open_file(fileName):
    with codecs.open(fileName, 'r', "utf-8") as file:
        data = file.readlines()
        document = data[198]
        #print(document)
        file.close()
        os.remove("DESTINATION_FILE_ON_YOUR_DISK")
        return document

def parse_file(doc):
    i = doc.find("<table class") + 12
    doc = doc[i:]
    maxX = '0'
    maxY = '0'

    start = ">"
    end = "<"

    i = doc.find(start) + 1
    doc = doc[i:]

    while doc[0] == end:
        i = doc.find(start) + 1
        doc = doc[i:]
    xcoord = doc[0:doc.find(end)]
    i = doc.find(start) + 1
    doc = doc[i:]
    while doc[0] == end:
        i = doc.find(start) + 1
        doc = doc[i:]
    char = doc[0:doc.find(end)]
    i = doc.find(start) + 1
    doc = doc[i:]
    while doc[0] == end:
        i = doc.find(start) + 1
        doc = doc[i:]
    ycoord = doc[0:doc.find(end)]
    i = doc.find(start) + 1
    doc = doc[i:]

    coords = [[ycoord, xcoord, char]]

    while doc[0] != 'f':
        while doc[0] == end:
            i = doc.find(start) + 1
            doc = doc[i:]
        xcoord = doc[0:doc.find(end)]
        if int(xcoord) > int(maxX):
            maxX = xcoord
        i = doc.find(start) + 1
        doc = doc[i:]
        while doc[0] == end:
            i = doc.find(start) + 1
            doc = doc[i:]
        char = doc[0:doc.find(end)]
        i = doc.find(start) + 1
        doc = doc[i:]
        while doc[0] == end:
            i = doc.find(start) + 1
            doc = doc[i:]
        ycoord = doc[0:doc.find(end)]
        if ycoord > maxY:
            maxY = ycoord
        i = doc.find(start) + 1
        doc = doc[i:]

        coords.append([ycoord, xcoord, char])
    coords.pop(0)
    print(coords, "      ", maxX, maxY)
    print_grid(coords, int(maxX), int(maxY))
    return

def print_grid(coords, maxX, maxY):
    print(coords)
    newGrid = [[' ' for i in range(maxX + 1)] for j in range(maxY + 1)]
    for row in coords:
        newGrid[int(row[0])][int(row[1])] = row[2]
    countY = maxY
    while (countY >= 0):
        countX = 0
        while (countX <= maxX):
            print(newGrid[countY][countX], end = "")
            countX += 1
        print()
        countY -= 1


def main(testUrl):
    if len(sys.argv) >= 3:
        file_id = sys.argv[1]
        destination = sys.argv[2]
    else:
        file_id = "TAKE_ID_FROM_SHAREABLE_LINK"
        destination = "DESTINATION_FILE_ON_YOUR_DISK"
    download_file_from_google_drive(testUrl, file_id, destination)
    file = open_file(destination)
    parse_file(file)

if __name__ == "__main__":
    main()