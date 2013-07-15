from flask import Flask, render_template, request, redirect, url_for, jsonify
import dbmanager

app = Flask(__name__)

#local = True
local = False
if local:
    dbman = dbmanager.DBManager(True)
else:
    dbman = dbmanager.DBManager()

#dbman._clear_db()
companies_cache = set([x['company_name'] for x in dbman.get_companies()])
industries_cache = set([x['industry_name'] for x in dbman.get_industries()])

@app.route("/")
def home(idea=None):
    if not idea and dbman.get_companies() and dbman.get_industries():
        print "generating rando idea"
        idea = dbman.generate_random_idea()
    elif not idea:
        idea = {'company':'Company X', 'industry':'Industry Y', 'votes':"-0", "_id":"default"}
    top_ideas = dbman.get_top_voted_ideas()
    print "new idea", idea
    return render_template("home.html", main_idea=idea, top_ideas=top_ideas)

@app.route("/add_company", methods=['GET', 'POST'])
def add_company():
    '''
    AJAX call
    '''
    if request.method == 'POST':
        company = request.form['company']
        message = company + " already exists!"
        if company not in companies_cache:
            companies_cache.add(company)
            company_id = dbman.add_company_to_db(company)
            print "added", company, company_id
            message = "added " + company + "!"
        return jsonify(message=message)
    return redirect(url_for('home'))

@app.route("/add_industry", methods=['GET', 'POST'])
def add_industry():
    '''
    AJAX call
    '''
    if request.method == 'POST':
        # ajax call
        industry = request.form.get('industry')
        message = industry + " already exists!"
        if industry not in industries_cache:
            industries_cache.add(industry)
            industry_id = dbman.add_industry_to_db(industry)
            message = "added " + industry + "!"
            print "added", industry, industry_id
        return jsonify(message=message)
    return redirect(url_for('home'))

@app.route("/upvote", methods=['GET', 'POST'])
def upvote():
    '''
    AJAX call
    '''
    if request.method == "POST":
        print "ajax upvote post"
        company = request.form.get("company")
        industry = request.form.get("industry")
        votes = int(request.form.get("votes"))
        idea = dbman.upvote_idea(company, industry)
        print "upvoting", idea
        top_ideas = dbman.get_top_voted_ideas()
        for item in top_ideas:
            item["_id"] = unicode(item.get("_id"))
        return jsonify(votes=votes+1, top_ideas=top_ideas)
    return redirect(url_for('home'))

@app.route("/new_idea", methods=['GET', 'POST'])
def new_idea():
    '''
    AJAX call
    '''
    if request.method == "POST":
        print "ajax new idea"
        idea = dbman.generate_random_idea()
        _id = unicode(idea["_id"])
        print _id
        top_ideas = dbman.get_top_voted_ideas()
        for item in top_ideas:
            item["_id"] = unicode(item.get("_id"))
        return jsonify(company=idea["company"], industry=idea["industry"], votes=idea["votes"], _id=_id, top_ideas=top_ideas)
    return redirect(url_for('home'))
        
if __name__ == "__main__":
    app.run(debug=True)

