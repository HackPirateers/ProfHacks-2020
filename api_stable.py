from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pandas as pd
import ast

app = Flask(__name__)
CORS(app) # <-- CORS is necessary for React.js's Axion to be able to use the methods in the api!
api = Api(app)

notes = {}

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
        args.list = ast.literal_eval(args.list[0])
        print(args.list)
        df = pd.read_csv("aslyum_by_country_origin2.csv")
        # fi = pd.read_csv()
        fi = pd.read_csv("Subcategory_Scores_FIW2017.csv")


        df = df[['cartodb_id', 'name', 'country_or', 'yr_2000',
               'yr_2001', 'yr_2002', 'yr_2003', 'yr_2004', 'yr_2005', 'yr_2006','yr_2007',
               'yr_2008', 'yr_2009', 'yr_2010', 'yr_2011', 'yr_2012', 'yr_2013',
               'yr_2014', 'yr_2015', 'yr_2016', 'yr_2017']]
        df.set_index("cartodb_id")


        df = df.T.fillna(df.mean(axis=1)).T
        if df['name'].str.contains(args.list[0]).any():
            x = df.loc[df["name"]==args.list[0]]
            print("name")
        elif df['country_or'].str.contains(args.list[0]).any():
            x = df.loc[df["country_or"]==args.list[0]]
            print("or")
        #x = df.loc[df["name"]==args.list[0]]
        # x = x.iloc[0]
        print(x)
        values = x.values.tolist()
        print("VALUES--->",values)
        values = values[0][3:]
        print("VALUES 2.0 --->",values)

        # X,y, year_subtract = preprocess(df, ccode1, ccode2)
        # years, totals = regression(X, y,year_su
        # btract)
        X = list(range(2000,2017))
        country_data = fi.loc[fi["Country"]==args.list[0]]
        aggr = country_data["Total Aggr"]
        aggr = int(aggr)
        stat = country_data["Status"]
        stat = stat.iloc[0]
        # fi_data = [aggr,stat]
        data = [X,values, aggr, stat]
        # data = [X,values]
        # data = [args.list[0]]
        z = {'output': data} # Formatting this is important. If you don't format it right,
        return z                                              # React won't get anything/ won't be able to index it.


api.add_resource(Test, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
