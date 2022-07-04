live_trade = False

asset = ["ETH"]
core  = [0.01]
base  = ["BTC"]
margin_percentage = 10

import os
import socket
import requests
import urllib3
from datetime import datetime
from termcolor import colored
from binance.client import Client
from binance.exceptions import BinanceAPIException
from apscheduler.schedulers.blocking import BlockingScheduler

# Get environment variables
api_key     = os.environ.get('p9xlE9TCFzgenwMcekmwwXI8b7YdMZ0T2FI4yqYU17RqbeXonUVQul54G9t3Qj2r')
api_secret  = os.environ.get('IsXznVY5tJnkpy7mD7LFHbSUiPyuGXRol7qG7E3geKeqYXhk6yQ7nMpNAbOfJS9U')
client      = Client(api_key, api_secret)

pair,round_off = [], []
for i in range(len(asset)):
    if len(base) > 1 : my_base_asset = base[i]
    else: my_base_asset = base[0]
    pair.append(asset[i] + base[0])

for coin in base:
    if coin == "USDT": decimal = 2
    elif coin == "BTC": decimal = 6
    elif coin == "ETH": decimal = 5
    elif coin == "BNB": decimal = 3
    else: decimal == 4
    round_off.append(decimal)

for i in range(len(pair)):
    
    # Auto Adjust FIXED or DYNAMIC variable
    if len(base) > 1 : my_base_asset = base[i]
    else: my_base_asset = base[0]
    if len(core) > 1 : my_core_number = core[i]
    else: my_core_number = core[0]
    if len(round_off) > 1 : my_round_off = round_off[i]
    else: my_round_off = round_off[0]

    # Retrieve Current Asset INFO
    asset_info      = client.get_symbol_ticker(symbol=pair[i])
    asset_price     = float(asset_info.get("price"))
    asset_balance   = float(client.get_asset_balance(asset=asset[i]).get("free"))

    # Computing for Trade Quantity
    current_holding = round(asset_balance * asset_price, my_round_off)
    change_percent  = round(((current_holding - my_core_number) / my_core_number * 100), 10)
    trade_amount    = round(abs(current_holding - my_core_number), my_round_off)

    # Output Console and Placing Order
    if (current_holding > my_core_number) and (abs(change_percent) > margin_percentage):
        if live_trade: client.order_market_sell(symbol=pair[i], quoteOrderQty=trade_amount)
        print(colored(asset_info, "green"))
        print(colored("Created at           : " + str(datetime.today().strftime("%d-%m-%Y @ %H:%M:%S")), "green"))
        print(colored("Prefix Core          : " + str(my_core_number) + " " + my_base_asset, "green"))
        print(colored("Current Core         : " + str(current_holding) + " " + my_base_asset, "green"))
        print(colored("Percentage Changed   : " + str(change_percent) + " %", "green"))
        print(colored("Action               : SELL " + str(trade_amount) + " " + my_base_asset + "\n", "green"))

    elif (current_holding < my_core_number) and (abs(change_percent) > margin_percentage):
        if live_trade: client.order_market_buy(symbol=pair[i], quoteOrderQty=trade_amount)
        print(colored(asset_info, "red"))
        print(colored("Created at           : " + str(datetime.today().strftime("%d-%m-%Y @ %H:%M:%S")), "red"))
        print(colored("Prefix Core          : " + str(my_core_number) + " " + my_base_asset, "red"))
        print(colored("Current Core         : " + str(current_holding) + " " + my_base_asset, "red"))
        print(colored("Percentage Changed   : " + str(change_percent) + " %", "red"))
        print(colored("Action               : BUY " + str(trade_amount) + " " + my_base_asset + "\n", "red"))

    else:
        print(asset_info)
        print("Created at           : " + str(datetime.today().strftime("%d-%m-%Y @ %H:%M:%S")))
        print("Prefix Core          : " + str(my_core_number) + " " + my_base_asset)
        print("Current Core         : " + str(current_holding) + " " + my_base_asset)
        print("Percentage Changed   : " + str(change_percent) + " %")
        print("Action               : Do Nothing\n")
