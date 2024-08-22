import codecs
import os
import requests
import sys
from pyparsing import empty

testUrl = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
url = "https://docs.google.com/document/d/e/2PACX-1vShuWova56o7XS1S3LwEIzkYJA8pBQENja01DNnVDorDVXbWakDT4NioAScvP1OCX6eeKSqRyzUW_qJ/pub"

def download_file_from_google_drive(url, file_id, destination):
    session = requests.Session()

    response = session.get(url, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(url, params=params, stream=True)

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
        file.close()
        os.remove("DESTINATION_FILE_ON_YOUR_DISK")
        return document

def parse_file(doc):
    maxX = 0
    maxY = 0
    table = "<table"
    closeTable = "</table>"
    start = ">"
    end = "<"

    coords = [[' ' for _ in range(3)] for _ in range(1000)]

    doc = doc[doc.find(table):]
    doc = doc[:doc.find(closeTable)]

    counter = 0
    while doc != empty:
        counter += 1
        try:
            doc = doc[(doc.find(start) + 1):]
            while doc[0] == end and doc[0] != empty:
                doc = doc[(doc.find(start) + 1):]
        except IndexError:
            break

        match (counter % 3):
            case 1:
                xcoord = doc[0:doc.find(end)]
                coords[int(counter / 3)][counter % 3] = xcoord
            case 2:
                char = doc[0:doc.find(end)]
                coords[int(counter / 3)][counter % 3] = char
            case 0:
                ycoord = doc[0:doc.find(end)]
                coords[int((counter / 3) - 1)][(counter % 3)-3] = ycoord
    coords.pop(0)
    print_grid(coords)

def print_grid(coords):
    maxX = 100
    maxY = 10
    newGrid = [[' ' for _ in range(maxX)] for _ in range(maxY)]
    for row in coords:
        try:
            newGrid[int(row[0])][int(row[1])] = row[2]
        except ValueError:
            break
    countY = maxY - 1
    while (countY >= 0):
        countX = 0
        while (countX <= maxX - 1):
            print(newGrid[countY][countX], end = "")
            countX += 1
        print()
        countY -= 1


def main(url):
    if len(sys.argv) >= 3:
        file_id = sys.argv[1]
        destination = sys.argv[2]
    else:
        file_id = "TAKE_ID_FROM_SHAREABLE_LINK"
        destination = "DESTINATION_FILE_ON_YOUR_DISK"
    download_file_from_google_drive(url, file_id, destination)
    file = open_file(destination)
    parse_file(file)

if __name__ == "__main__":
    main(url)