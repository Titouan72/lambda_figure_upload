import json
import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
import numpy as np
import datetime
import boto3

def lambda_handler(event, context):
    
    np.random.seed(19680801)
    # figure
    rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
    loc = RRuleLocator(rule)
    formatter = DateFormatter('%m/%d/%y')
    date1 = datetime.date(1952, 1, 1)
    date2 = datetime.date(2004, 4, 12)
    delta = datetime.timedelta(days=100)
    
    dates = drange(date1, date2, delta)
    s = np.random.rand(len(dates))  # make up some random y values
    
    
    fig, ax = plt.subplots()
    plt.plot(dates, s, 'o')
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    
    # save & upload
    figFile = str(event.date)
    url = "/tmp/" + figFile + "_img.png"
    name = figFile + "_img.png"
    plt.savefig(url)
    client = boto3.client('s3')
    client.upload_file(url, testsavefigure, name)

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
