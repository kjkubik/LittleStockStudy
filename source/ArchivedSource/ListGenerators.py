new_list = [x*5 for x in range(10)]
print(new_list)




# When using "with open" your file closes automatically. Finally is not needed.
try:
    with open("resources/StockPrices.csv") as f:
        # Do something with the file
        pass
except:
    print("file didn't open")
