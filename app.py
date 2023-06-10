from flask import Flask, render_template, request
from recommend import recommend

app =  Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/input")
def input_sentence():
    return render_template('input.html')

# @app.route("/input", methods =['GET', 'POST'])
# def input_sentence():
#     if request.method == "GET":
#         rc = recommend()
#         return render_template('input.html')
#     elif request.method == "POST":
#         input = request.form['input']
#         rc.input_txt(input)
#         b, c, i, r = rc.search()
#         return render_template("")
    #     top = request.form['top']
    #     bottom = request.form['bottom']
    #     height = request.form['height']
    #     # 台形の計算
    #     answer = trapezoid_area(top, bottom, height)

    #     return render_template('calculation.html', result=answer)

@app.route("/result", methods =['GET', 'POST'])
def indicate_result():
    if request.method == "POST":
        rc = recommend()
        input = request.form['input']
        rc.input_txt(input)
        rc.search_bm25()
        rc.search_wrd()
        b, c, i, r = rc.search()
        return render_template('result.html', b_rslt=b, c_rslt=c, i_rslt=i, r_rslt=r)
    else:
        return render_template("noresult.html")

# @app.route("/",methods=['GET','POST'])
# def calculation():
#     if request.method == "GET":
#         return render_template('calculation.html')
#     elif request.method == "POST":
#         top = request.form['top']
#         bottom = request.form['bottom']
#         height = request.form['height']
#         # 台形の計算
#         answer = trapezoid_area(top, bottom, height)

#         return render_template('calculation.html', result=answer)
        

if __name__ == "__main__":
    app.run(debug=True)