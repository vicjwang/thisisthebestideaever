import pymongo, random, ast, bson

class DBManager:

    def __init__(self, local=False):
        if local:
            conn = pymongo.Connection()
            self._db = conn['bestidea']
        else:
            conn = pymongo.Connection("127.3.218.129", 27017)
            self._db = conn['bestidea']
            self._db.authenticate('admin', 'nULRUzxpLtJ4')

        self._idea_ids = self.load_idea_ids()

    def _clear_db(self):
        self._db.ideas.drop()
        self._db.companies.drop()
        self._db.industries.drop()

    def load_idea_ids(self):
        '''
        maps (company, industry) tuple to objectid
        '''
        ideas = self.get_ideas()
        pairs = [(x['company'], x['industry']) for x in ideas]
        ids = [x['_id'] for x in ideas]
        return dict(zip(pairs,ids))

    def get_companies(self):
        return list(self._db.companies.find())

    def get_industries(self):
        return list(self._db.industries.find())

    def get_ideas(self):
        return list(self._db.ideas.find())

    def add_company_to_db(self,company):
        c = {"company_name":company}
        company_id = self._db.companies.save(c)
        return company_id
     
    def add_industry_to_db(self, industry):
        i = {"industry_name":industry}
        industry_id = self._db.industries.save(i)
        return industry_id

    def add_idea_to_db(self, idea):
        idea_id = self._db.ideas.save(idea)
        return idea_id
     
    def upvote_idea(self, company, industry):
        
        idea_id = self._idea_ids.get((company, industry))
        print "idea_id is", idea_id
        idea = self._db.ideas.find_one({"_id":idea_id})
        print "idea is", idea
        num_votes = idea['votes'] + 1
        idea['votes'] = num_votes 
        self._db.ideas.save(idea)
        return idea

    def get_top_voted_ideas(self, n=5):
        ideas = self._db.ideas
        top = list(ideas.find().sort("votes"))
        top.reverse()
        return top[:n]

    def generate_random_idea(self):
        companies = self.get_companies()
        industries = self.get_industries()
        com_i = random.randint(0, len(companies)-1)
        ind_i = random.randint(0, len(industries)-1)
        company = companies[com_i].get('company_name')
        industry = industries[ind_i].get('industry_name')
        pair = (company, industry)
        print "idea_ids", self._idea_ids
        if pair in self._idea_ids:
            print "pair in idea_ids"
            idea_id = self._idea_ids[pair]
            idea = self._db.ideas.find_one(({"_id":idea_id}))
        else:
            print "pair not in idea_ids, should be here"
            idea = {"company":company, "industry":industry, "votes":0}
            idea_id = self.add_idea_to_db(idea)
            idea.update({'_id':idea_id})
            self._idea_ids[pair] = idea_id
        return idea
