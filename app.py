from flask import Flask, render_template, request
from recommend import recommend

app =  Flask(__name__)
rc = recommend()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/input")
def input_sentence():
    return render_template('input.html')

@app.route("/result", methods =['GET', 'POST'])
def indicate_result():
    if request.method == "POST":
        input = request.form['input']
        rc.input_txt(input)
        rc.search_bm25()
        rc.search_wrd()
        b, c, i, r = rc.search()
        return render_template('result.html', b_rslt=b, c_rslt=c, i_rslt=i, r_rslt=r)
    else:
        return render_template("noresult.html")        

if __name__ == "__main__":
    app.run(debug=True)