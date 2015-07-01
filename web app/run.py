from flask import Flask, request, render_template, redirect
import re
import happybase
import json
from app import views
app = Flask(__name__)

def create_individual_json(ID):

    connection = happybase.Connection('52.8.203.194')
    my_table = connection.table("rsvp_graph")

    nodes = []
    links = []

    dict_members = {}
    dict_edge = {}
    
    dict_members[ID] = 0
    index = 1
    nodes.append({"name":ID,"group":1})

    for key, data in my_table.scan(row_prefix = ID ):
        m = key.split("_")
        ID1 = unicode(m[0])
        ID2 = unicode(m[1])
        weight = 200/(float(data['f:count']) * float(data['f:count']))

        if ID1.isnumeric() and ID2.isnumeric() and weight < 300:
                if ID1 not in dict_members:
                        dict_members[ID1] = index
                        index = index + 1
                        nodes.append({"name":ID1,"group":2})
                if ID2 not in dict_members:
                        dict_members[ID2] = index
                        index = index + 1
                        nodes.append({"name":ID2 ,"group":2})
                if ID1+"_"+ID2 not in dict_edge and ID2+"_"+ID1 not in dict_edge:
                        dict_edge[ID1+"_"+ID2] = 1
                        links.append({"source":dict_members[ID1],"target":dict_members[ID2],"value" : weight})

    data = {"nodes": nodes , "links": links}

    with open('static/rsvpGraph.json', 'w') as outfile:
        json.dump(data, outfile)

def create_group_json(ID):

        connection = happybase.Connection('52.8.203.194')
        my_table = connection.table("members")
        dict_members = {}
        dict_edge = {}
        global index
        index = 0
        
        row = table.row(ID, columns=['cf'])        
        for key in row:
                newid = unicode(row[key])
                if newid not in dict_members and newid.isnumeric():
                        dict_members[newid] = index
                        index = index + 1
        nodes = []
        links = []

        for ID in dict_members.keys():
                addEdge(str(ID), links , dict_members , dict_active_members, dict_edge)

        for ID in dict_members.keys():
                nodes.append({"name":ID, "group":1})

        data = {"nodes": nodes , "links": links}

        with open('static/groupgraph.json', 'w') as outfile:
                json.dump(data, outfile)


def addEdge(ID, links, dict_members ,dict_active_members, dict_edge ):
        connection = happybase.Connection('52.8.203.194')
        my_table = connection.table("rsvp_graph")
        for key, data in my_table.scan(row_prefix = ID):
                m = key.split("_")
                ID1 = unicode(m[0])
                ID2 = unicode(m[1])
                weight = 75/(float(data['f:count']) * float(data['f:count']))
                if ID1 in dict_members and ID2 in dict_members:
                        if ID1+"_"+ID2 not in dict_edge and ID2+"_"+ID1 not in dict_edge:
                                dict_edge[ID1+"_"+ID2] = 1
                                links.append({"source":dict_members[ID1],"target":dict_members[ID2],"value" : weight})

@app.route("/")
def main():
        return render_template('form_submit.html')

@app.route("/slides")
def slides():
        return render_template('slides.html')

@app.route("/graph", methods = ['POST'])
def hello():
    ID = request.form['text']
    create_individual_json(ID)
    return render_template('graph.html')

@app.route("/group")
def group():
    return render_template('form_submit_group.html')

@app.route("/groupGraph", methods = ['POST'])
def groupgraph():
        ID = request.form['textbis']
        create_group_json(ID)
        return render_template("groupgraph.html")

if __name__ == "__main__":
    app.run(host ='0.0.0.0',debug = True )