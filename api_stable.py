from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from scipy.optimize import curve_fit
from datetime import *
import numpy as np
import pandas as pd
import ast

app = Flask(__name__)
CORS(app) # <-- CORS is necessary for React.js's Axion to be able to use the methods in the api!
api = Api(app)

notes = {}

df = pd.read_csv("time_series_19-covid-Confirmed.csv", header=0)
x_val = 0;
countries = df['Country/Region'].unique()
#print(countries)
dictOfCountries = {}
#dictOfCountries = {i : countries[i] for i in range(0, len(countries))}
for i in range(0, len(countries)):
     dictOfCountries[countries[i]] = i
print(dictOfCountries)


listCountries = []
listCountriesSum = []
for i in range(0, len(countries)):
    temp = df[(df['Country/Region'] == countries[i])].drop(['Lat','Long'],axis=1)
    listCountries.append(temp)

    listCountriesSum.append(temp.sum(numeric_only=True).to_frame().T)
    listCountriesSum[i].insert(0, 'Country', [countries[i]], True)

print(listCountriesSum[25])
class Test(Resource):



    def put(self):

        # Parsing. View docs(https://flask-restful.readthedocs.io/en/latest/) if this isn't what you need.
        # parser.add_argument('list', action='append') lets flask know that list an argument that can hold 2+ pieces of data in this data :
        # put('http://localhost:5000/', data={"list" : ["When was Barack Obama's birthday?", "What is 10 plus 5 equal to?"]}).json()
        # With that, you have one piece of metadata associated with 2 or more peice of data(aka a list) that can be indexed
        # args is the main class here, and since list is the subclass(an arg of class args) of args, we can mention it freely
        # and access it like this : args.list. We can index by doing args.list[index]

        parser = reqparse.RequestParser()
        parser.add_argument('list', action='append')

        args = parser.parse_args()
        print(args.list)
        #@TODO Have to map contry name given by react to country name on dataset
        #Also have to map that to an index to parse to proper set using dictionary
        print("SFSDGSDf")
        args.list = ast.literal_eval(args.list[0])
        print(args.list)


        #     new_row = pd.DataFrame({"Country": countries[i]}, index=[0])
        #   listCountriesSum[i] = pd.concat([new_row, listCountriesSum[i]])

        #print(listCountries[0])
        #print(type(listCountriesSum[0]))
        #change inddex for country
        testin = dictOfCountries.get(args.list[1])
        # print(listCountriesSum[testin])
        # print(range(1, len(listCountriesSum[testin].columns)))

        print(listCountriesSum[testin])
        dates = list(range(1, len(listCountriesSum[testin].columns)))
        # print(dates)
        # print(listCountriesSum[testin].values.tolist()[0])
        # print(listCountriesSum[testin].values.tolist()[0][:1][0])
        # print(listCountriesSum[testin].values.tolist()[0][1:])
        name =listCountriesSum[testin].values.tolist()[0][:1][0]
        vals = listCountriesSum[testin].values.tolist()[0][1:]
        if(vals[10]-vals[0]<10):
          dates = dates[13:]
          vals = vals[13:]

        def sigmoid(x, L ,x0, k, b):
            y = L / (1 + np.exp(-k*(x-x0)))+b
            return y

        p0 = [max(vals), np.median(dates),1,min(vals)] # this is an mandatory initial guess
        try:
          popt, pcov = curve_fit(sigmoid, dates,vals,p0, method='dogbox',maxfev=5000)
        except RuntimeError:
          try:
            popt, pcov = curve_fit(sigmoid, dates,vals,p0, method='dogbox',maxfev=10000)
          except RuntimeError:
            try:
              popt, pcov = curve_fit(sigmoid, dates,vals,p0, method='dogbox',maxfev=50000)
            except:
              popt, pcov = curve_fit(sigmoid, dates,vals,p0, method='dogbox',maxfev=100000)

        approx_vals = sigmoid(dates, *popt)
        inflection_pt = round(popt[0] / (1+np.exp(-popt[2]*(900-popt[1]))) + popt[3])/2
        print(inflection_pt)
        # x = (np.log((-popt[0]/(popt[3]-inflection_pt)) + 1))/(-popt[2]) + popt[1]
        x_val = - (np.log((inflection_pt-popt[0]-popt[3])/(popt[3]-inflection_pt))/popt[0]) + popt[1]
        print(x_val)

        poi = inflection_pt
        # fi_data = [aggr,stat]
        dates1 = date(2020,1,22) + timedelta(days=x_val)
        # print(len(approx_vals.tolist())==len(vals))
        data = [name,dates, vals,approx_vals.tolist(), poi,str(dates1)]
        # data = [X,values]
        # data = [args.list[0]]
        print(data)
        z = {'output': data} # Formatting this is important. If you don't format it right,
        return z                                              # React won't get anything/ won't be able to index it.

    def push(self):
            parser = reqparse.RequestParser()
            parser.add_argument('list', action='append')

            args = parser.parse_args()
            print(args.list)
            args.list = ast.literal_eval(args.list[0])
            print(args.list)
            date_str = args.list[0]
            mt = int(date_str[:2])
            dy = int(date_str[3:4])
            yr = 2000 + int(date_str[6:])
            d0 = date(yr, mt, dy)

            d2 = date(2020,1,22) + timedelta(days=x_val)
            print(d2)
            # d1 = date(2020, 2, 12)
            delta = d2 - d0
            severity = 100-delta.days
            print("Severity", severity)

api.add_resource(Test, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
