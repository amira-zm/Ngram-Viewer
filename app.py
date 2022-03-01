from flask import Flask, render_template, flash, redirect, url_for, session, request, logging,url_for
import pandas as pd
import getngrams
import datetime


app = Flask(__name__)

# Import writer class from csv module
from csv import writer

# List




@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        form = request.form["nom"].lower()
        corpus =request.form["pets"]
        deb=request.form["deb"]
        end=request.form["fin"]

        ch1 = form + " --startYear="+deb+" --endYear=+"+end+" --corpus="+corpus
        List = [form.title(), deb,end, corpus,1]

        # Open our existing CSV file in append mode
        # Create a file object for this file
        with open('event.csv', 'a') as f_object:
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)

            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(List)

            # Close the file object
            f_object.close()

        getngrams.runQuery(ch1)

        return redirect(url_for('line', form=form ,corpus=corpus,deb=deb,end=end))

    return render_template("home.html")

@app.route('/favorite')
def fovorite():
    events= pd.read_csv ('event.csv')

    rec=events.groupby(events.columns.tolist()).size().reset_index().rename(columns={0: 'records'})
    records = rec.head(10)
    records.to_csv("ev.csv")




    return render_template("favorite.html",records=records)

@app.route('/line/<string:form>/<string:corpus>/<string:deb>/<string:end>')


def line(form,corpus,deb,end):
    list_date = []
    poster_path = "https://image.tmdb.org/t/p/original/"
    date = "1800-01-15"
    desc = ''
    author = ''
    img = ''
    genre = ''
    d=dict()
    imdb = []
    ch = form.replace(" ", "") + "-" + corpus + "-" + deb + "-" + end + "-3-caseSensitive.csv"
    fin = open(ch, 'r')
    ngrams = fin.readline().strip().split(',')[1:]

    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s) * 100)  # Make percentage
    fin.close()

    values = []
    labels = []
    for i in range(0, len(data_vals[i])):
        values.append(years[i])
        labels.append(data_vals[0][i])

    max_value = None

    for num in labels:
        if (max_value is None or num > max_value):
            max_value = num

    df = pd.read_csv("final.csv")
    ind=0
    for i in range(len(df)):
        chaine = df.iloc[i, 1][4:]
        d1=dict()
        if (form.title() == chaine.title()):
            print(form.title(), chaine.title())
            date = df.iloc[i, 2][4:]
            print(date)

            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            try:
                x = int(values.index(datem.year))
            except:
                x = 0
            print(datem.year, '++++++++++', deb, '+++++++++++', end)
            if (int(datem.year) <= int(end) and int(datem.year) >= int(deb)):
                list_date.append(x)
                print(list_date)
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", list_date)
            desc=(df.iloc[i, 14][4:])
            img=(df.iloc[i, 15][4:])
            author=(df.iloc[i, 9][4:])
            genre=(df.iloc[i, 11][4:])
            imdb=(df.iloc[i, 16][4:])
            d1["img"]=img
            d1["genre"] = genre
            d1["author"]=author
            d1["desc"] = desc
            d[ind]=d1
            ind+=1


    for i in range(len(labels)):
        labels[i] = (labels[i] * 100) / max_value
    resultantList = []

    for element in list_date:

        if element not in resultantList:
            resultantList.append(element)
    print(resultantList)

    return render_template('line_chart.html', title='Sharbooks Ngram', d=d,max=max_value, labels=values,values=labels,ngrams=ngrams[0],t=resultantList,corpus=corpus,deb=deb,end=end,img=img,desc=desc,author=author,genre=genre,imdb=imdb)

@app.route('/line/<string:form>/<string:corpus>/<string:deb>/<string:end>/<string:id>')

def line1(form,corpus,deb,end,id):
    list_date = []
    list_poster=[]
    list_overview=[]
    poster_path = "https://image.tmdb.org/t/p/original/"
    date = "1800-01-15"
    desc = ''
    author = ''
    img = ''
    genre = ''
    d = {}
    imdb = []
    ch = form.replace(" ", "") + "-" + corpus + "-" + deb + "-" + end + "-3-caseSensitive.csv"
    fin = open(ch, 'r')
    ngrams = fin.readline().strip().split(',')[1:]

    data_vals = [[] for ngram in ngrams]
    years = []
    for line in fin:
        sp = line.strip().split(',')
        years.append(int(sp[0]))
        for i, s in enumerate(sp[1:]):
            data_vals[i].append(float(s) * 100)  # Make percentage
    fin.close()

    values = []
    labels = []
    for i in range(0, len(data_vals[i])):
        values.append(years[i])
        labels.append(data_vals[0][i])

    max_value = None

    for num in labels:
        if (max_value is None or num > max_value):
            max_value = num

    df = pd.read_csv("final.csv")
    ind = 0
    for i in range(len(df)):
        chaine = df.iloc[i, 1][4:]
        d1 = {}
        if (form.title() == chaine.title()):
            print(form.title(), chaine.title())
            date = df.iloc[i, 2][4:]
            poster = (df.iloc[i, 17][4:])
            overview = (df.iloc[i, 18][4:])
            print(date)

            datem = datetime.datetime.strptime(date, "%Y-%m-%d")
            try:
                x = int(values.index(datem.year))
            except:
                x = 0
            print(datem.year, '++++++++++', deb, '+++++++++++', end)
            if (int(datem.year) <= int(end) and int(datem.year) >= int(deb)):
                list_date.append(x)
                list_poster.append(poster)
                list_overview.append(overview)
                print(list_date)
            print("liiiiiiiiiiiiiiiiiiiiiiiiiiiiiiste", list_date)
            desc = (df.iloc[i, 14][4:])
            img = (df.iloc[i, 15][4:])
            author = (df.iloc[i, 9][4:])
            genre = (df.iloc[i, 11][4:])
            imdb = (df.iloc[i, 16][4:])
            d1["img"] = img
            d1["genre"] = genre
            d1["author"] = author
            d1["desc"] = desc
            d[ind] = d1
            ind += 1

    for i in range(len(labels)):
        labels[i] = (labels[i] * 100) / max_value
    resultantList = []
    dict= {}

    for i in range(len(list_date)):
        dicti = {}
        if list_date[i] not in resultantList:
            resultantList.append(list_date[i])
            dicti["poster"]=list_poster[i]
            dicti["overview"] =list_overview[i]
            dict[list_date[i]]=dicti
    print(resultantList)

    return render_template('line_chart1.html', dict=dict,title='Sharbooks Ngram',d=d, max=max_value, labels=values,
                           values=labels,ngrams=ngrams[0],x=id,t=resultantList,corpus=corpus,deb=deb,end=end,desc=desc,img=img,author=author,genre=genre,imdb=imdb)



if __name__ == '__main__':
    app.run(port=5555,debug=True)
